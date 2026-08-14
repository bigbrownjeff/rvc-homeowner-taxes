// Pages advanced-mode worker: privacy-safe signup APIs, clean URLs, and static assets.

const CLEAN_PAGE_ASSETS = {
  "/": "/index.html",
  "/breakeven": "/breakeven.html",
  "/calculator": "/calculator.html",
  "/coverage": "/coverage.html",
  "/deck": "/deck.html",
  "/fiscal-math": "/fiscal-math.html",
  "/governance": "/governance.html",
  "/governance-options": "/governance-options.html",
  "/privacy": "/privacy.html",
  "/reconcile": "/reconcile.html",
  "/redraw-evidence": "/redraw-evidence.html",
  "/validation": "/validation.html",
  "/voices": "/voices.html",
  "/voices-library": "/voices-library.html",
};

const LEGACY_PAGE_ROUTES = {
  "/brief-2026-08": "/",
  "/brief-2026-08.html": "/",
  "/index.html": "/",
  "/breakeven.html": "/breakeven",
  "/calculator.html": "/calculator",
  "/coverage.html": "/coverage",
  "/deck.html": "/deck",
  "/fiscal-math.html": "/fiscal-math",
  "/governance.html": "/governance",
  "/governance-options.html": "/governance-options",
  "/privacy.html": "/privacy",
  "/reconcile.html": "/reconcile",
  "/redraw-evidence.html": "/redraw-evidence",
  "/validation.html": "/validation",
  "/voices.html": "/voices",
  "/voices-library.html": "/voices-library",
};

// Short, copyable campaign links for Wave 3 outreach. These are deliberately
// fixed mappings: they do not forward arbitrary query parameters or retain
// visitor identifiers. Keep unknown /go/* paths as real 404s.
const CAMPAIGN_ROUTES = {
  "/go/email": { source: "email", medium: "email" },
  "/go/linkedin": { source: "linkedin", medium: "social" },
  "/go/bsky": { source: "bsky", medium: "social" },
  "/go/threads": { source: "threads", medium: "social" },
  "/go/x": { source: "x", medium: "social" },
  "/go/facebook": { source: "facebook", medium: "social" },
};
const CAMPAIGN_NAME = "wave-3-2026";
const SIGNUP_SOURCES = new Set([
  "signup-strip:direct",
  "signup-strip:email",
  "signup-strip:linkedin",
  "signup-strip:bsky",
  "signup-strip:threads",
  "signup-strip:x",
  "signup-strip:facebook",
]);

const COUNT_EVENTS = new Set(["lookup", "letter_copied", "contact_opened", "sent_confirmed"]);
const ACTION_KEYS = new Set(["", "fed", "sen", "asm", "cty", "vil"]);
const MAX_JSON_BYTES = 2048;
const textEncoder = new TextEncoder();

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (CAMPAIGN_ROUTES[url.pathname]) {
      return serveCampaignRedirect(url, CAMPAIGN_ROUTES[url.pathname]);
    }
    if (url.pathname.startsWith("/go/")) return plain("not found", 404);

    if (LEGACY_PAGE_ROUTES[url.pathname]) {
      return Response.redirect(new URL(LEGACY_PAGE_ROUTES[url.pathname], url.origin).toString(), 301);
    }

    if (url.pathname === "/api/signup") return handleSignup(request, env, url);
    if (url.pathname === "/api/unsubscribe") return handleUnsubscribe(request, env, url);
    if (url.pathname === "/api/count") return handleCount(request, env, url);
    if (url.pathname.startsWith("/api/")) return plain("not found", 404);

    if (CLEAN_PAGE_ASSETS[url.pathname]) {
      if (request.method !== "GET" && request.method !== "HEAD") return plain("method not allowed", 405);
      return serveNamedPage(request, env, url);
    }

    // Pages advanced mode can otherwise turn a missing navigation into index.html.
    // Treat routes that look like pages as true 404s before asking the asset binding.
    if (looksLikeMissingPage(url.pathname)) return serveNotFound(request, env, url);

    const asset = await env.ASSETS.fetch(request);
    // A missing static file can also arrive from Pages as the landing HTML. Do not
    // let that become a soft 404 for robots, sitemap typos, or old links.
    if (asset.status === 404 || isHtml(asset)) return serveNotFound(request, env, url);
    return asset;
  },
};

function serveCampaignRedirect(url, campaign) {
  const destination = new URL("/", url.origin);
  destination.searchParams.set("utm_source", campaign.source);
  destination.searchParams.set("utm_medium", campaign.medium);
  destination.searchParams.set("utm_campaign", CAMPAIGN_NAME);
  return new Response(null, {
    status: 302,
    headers: {
      Location: destination.toString(),
      "Cache-Control": "no-store",
      "Referrer-Policy": "strict-origin-when-cross-origin",
    },
  });
}

async function handleSignup(request, env, url) {
  if (request.method !== "POST") return plain("method not allowed", 405);
  if (!env.SIGNUPS) return plain("list unavailable", 503);

  const parsed = await parseSameOriginJson(request, url);
  if (parsed.error) return parsed.error;
  const body = parsed.body;
  if (honeypotFilled(body)) return json({ ok: true });

  const email = normalizeEmail(body.email);
  if (!isValidEmail(email)) return json({ ok: false, error: "valid email required" }, { status: 400 });
  if (body.consent !== true) return json({ ok: false, error: "explicit consent required" }, { status: 400 });
  if (await rateLimited(env, request, "signup", 600)) {
    return json({ ok: false, error: "please wait before trying again" }, { status: 429, headers: { "Retry-After": "600" } });
  }

  const key = await signupKey(email);
  const legacyKey = "signup:" + email;
  try {
    const [modern, legacy] = await Promise.all([
      env.SIGNUPS.get(key, "json"),
      env.SIGNUPS.get(legacyKey, "json"),
    ]);
    const existing = modern || legacy;
    const now = new Date().toISOString();
    // The update list deliberately stores only what is needed to send updates.
    // In particular, incoming name and address fields are ignored and never written.
    await env.SIGNUPS.put(key, JSON.stringify({
      email,
      source: cleanSource(body.source),
      consentAt: now,
      first: existing && existing.first ? existing.first : now,
      last: now,
    }));
    if (legacy) await env.SIGNUPS.delete(legacyKey);
    if (!existing) await changeCount(env, "signup", 1);
  } catch (err) {
    console.error("signup KV write failed", err);
    return plain("signup storage error, try again", 500);
  }

  return json({ ok: true });
}

async function handleUnsubscribe(request, env, url) {
  if (request.method !== "POST") return plain("method not allowed", 405);
  if (!env.SIGNUPS) return plain("list unavailable", 503);

  const parsed = await parseSameOriginJson(request, url);
  if (parsed.error) return parsed.error;
  const body = parsed.body;
  if (honeypotFilled(body)) return json({ ok: true });

  const email = normalizeEmail(body.email);
  if (!isValidEmail(email)) return json({ ok: false, error: "valid email required" }, { status: 400 });
  if (await rateLimited(env, request, "unsubscribe", 600)) {
    return json({ ok: false, error: "please wait before trying again" }, { status: 429, headers: { "Retry-After": "600" } });
  }

  const key = await signupKey(email);
  const legacyKey = "signup:" + email;
  try {
    const [modern, legacy] = await Promise.all([
      env.SIGNUPS.get(key),
      env.SIGNUPS.get(legacyKey),
    ]);
    if (modern !== null || legacy !== null) {
      await Promise.all([env.SIGNUPS.delete(key), env.SIGNUPS.delete(legacyKey)]);
      await changeCount(env, "signup", -1);
    }
  } catch (err) {
    console.error("unsubscribe KV delete failed", err);
    return plain("unsubscribe storage error, try again", 500);
  }

  // Do not reveal whether an address was subscribed.
  return json({ ok: true });
}

async function handleCount(request, env, url) {
  if (!env.SIGNUPS) return json(emptyCounts());
  if (request.method === "GET") {
    try {
      const [lookup, legacyLetter, letterCopied, contactOpened, sentConfirmed, signup] = await Promise.all([
        readCount(env, "lookup"),
        readCount(env, "letter"),
        readCount(env, "letter_copied"),
        readCount(env, "contact_opened"),
        readCount(env, "sent_confirmed"),
        readCount(env, "signup"),
      ]);
      return json({
        lookup,
        letter_copied: legacyLetter + letterCopied,
        contact_opened: contactOpened,
        sent_confirmed: sentConfirmed,
        signup,
      });
    } catch (err) {
      console.error("count KV read failed", err);
      return plain("count storage error", 500);
    }
  }
  if (request.method !== "POST") return plain("method not allowed", 405);

  const parsed = await parseSameOriginJson(request, url);
  if (parsed.error) return parsed.error;
  const body = parsed.body;
  if (honeypotFilled(body)) return json({ ok: true });
  const event = cleanString(body.event, 40);
  const action = cleanString(body.action, 12);
  if (!COUNT_EVENTS.has(event) || !ACTION_KEYS.has(action)) return plain("bad event", 400);
  if (await rateLimited(env, request, "event:" + event + ":" + action, 600)) {
    return json({ ok: true, rateLimited: true });
  }

  try {
    const count = await changeCount(env, event, 1);
    return json({ ok: true, event, count });
  } catch (err) {
    console.error("count KV write failed", err);
    return plain("count storage error", 500);
  }
}

function looksLikeMissingPage(pathname) {
  if (pathname === "/404.html") return true;
  const leaf = pathname.split("/").pop() || "";
  return !leaf.includes(".") || pathname.endsWith(".html");
}

async function serveNamedPage(request, env, url) {
  // Pages already maps a clean page route such as /calculator to calculator.html.
  // Asking its asset binding for calculator.html makes Pages redirect back to the
  // clean route, which would turn the internal asset lookup into a redirect loop.
  const response = await env.ASSETS.fetch(request);
  return response.status === 404 ? serveNotFound(request, env, url) : injectBeacon(response);
}

async function serveNotFound(request, env, url) {
  const notFoundUrl = new URL(url);
  // Pages resolves /404 to the static 404.html asset. Requesting the file name
  // directly returns its automatic clean-URL redirect with an empty body.
  notFoundUrl.pathname = "/404";
  notFoundUrl.search = "";
  const page = await env.ASSETS.fetch(new Request(notFoundUrl, request));
  const headers = new Headers(page.headers);
  headers.delete("content-length");
  headers.set("Cache-Control", "no-store");
  const response = new Response(request.method === "HEAD" ? null : page.body, {
    status: 404,
    headers,
  });
  return injectBeacon(response);
}

async function parseSameOriginJson(request, url) {
  const origin = request.headers.get("Origin");
  if (!origin || origin !== url.origin) return { error: plain("same-origin request required", 403) };
  const contentType = (request.headers.get("Content-Type") || "").toLowerCase();
  if (!contentType.startsWith("application/json")) return { error: plain("application/json required", 415) };
  const declaredLength = Number(request.headers.get("Content-Length") || 0);
  if (declaredLength > MAX_JSON_BYTES) return { error: plain("request too large", 413) };

  let raw;
  try {
    raw = await request.text();
  } catch {
    return { error: plain("bad json", 400) };
  }
  if (textEncoder.encode(raw).byteLength > MAX_JSON_BYTES) return { error: plain("request too large", 413) };
  try {
    const body = JSON.parse(raw);
    if (!body || typeof body !== "object" || Array.isArray(body)) throw new Error("bad body");
    return { body };
  } catch {
    return { error: plain("bad json", 400) };
  }
}

function normalizeEmail(value) {
  return cleanString(value, 254).toLowerCase();
}

function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function cleanSource(value) {
  const source = cleanString(value, 120);
  return SIGNUP_SOURCES.has(source) ? source : "signup-strip:direct";
}

function cleanString(value, max) {
  return typeof value === "string" ? value.trim().slice(0, max) : "";
}

function honeypotFilled(body) {
  return typeof body.website === "string" && body.website.trim() !== "";
}

async function signupKey(email) {
  return "signup:" + await sha256(email);
}

async function rateLimited(env, request, scope, ttlSeconds) {
  const ip = request.headers.get("CF-Connecting-IP");
  if (!ip) return false; // Local development and tests do not receive this Cloudflare header.
  const key = "rate:" + scope + ":" + await sha256(ip);
  try {
    if (await env.SIGNUPS.get(key)) return true;
    await env.SIGNUPS.put(key, "1", { expirationTtl: ttlSeconds });
    return false;
  } catch (err) {
    // A rate-limit failure must not turn a valid consent request into a false success.
    console.error("rate limit KV failure", err);
    return false;
  }
}

async function sha256(value) {
  const digest = await crypto.subtle.digest("SHA-256", textEncoder.encode(value));
  return Array.from(new Uint8Array(digest), (byte) => byte.toString(16).padStart(2, "0")).join("");
}

function emptyCounts() {
  return { lookup: 0, letter_copied: 0, contact_opened: 0, sent_confirmed: 0, signup: 0 };
}

function json(obj, init = {}) {
  const headers = new Headers(init.headers || {});
  headers.set("Content-Type", "application/json; charset=utf-8");
  headers.set("Cache-Control", "no-store");
  headers.set("X-Content-Type-Options", "nosniff");
  return new Response(JSON.stringify(obj), { status: init.status || 200, headers });
}

function plain(message, status) {
  return new Response(message, {
    status,
    headers: { "Cache-Control": "no-store", "X-Content-Type-Options": "nosniff" },
  });
}

function isHtml(response) {
  return (response.headers.get("content-type") || "").includes("text/html");
}

// Single insertion point for the Cloudflare Web Analytics beacon: every static
// HTML asset flows through the asset fallback above, so rewriting the head
// covers every served page without touching each site/*.html file individually.
const BEACON = "<!-- Cloudflare Web Analytics -->" +
  "<script type='module' src='https://static.cloudflareinsights.com/beacon.min.js' " +
  "data-cf-beacon='{\"token\": \"21d68181640646a5882a541e90f8be0f\"}'></script>" +
  "<!-- End Cloudflare Web Analytics -->";
function injectBeacon(response) {
  if (!isHtml(response)) return response;
  return new HTMLRewriter()
    .on("head", { element(el) { el.append(BEACON, { html: true }); } })
    .transform(response);
}

async function readCount(env, event) {
  const value = parseInt(await env.SIGNUPS.get("count:" + event), 10);
  return Number.isFinite(value) ? Math.max(0, value) : 0;
}

async function changeCount(env, event, delta) {
  // KV has no atomic increment. This is a count-only, non-critical tally: a
  // race may undercount, but it cannot expose personal data or label a copy as a send.
  const next = Math.max(0, (await readCount(env, event)) + delta);
  await env.SIGNUPS.put("count:" + event, String(next));
  return next;
}
