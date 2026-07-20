// Pages advanced-mode worker: /api/signup -> KV; legacy paths -> 301; everything else -> static assets.
export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // Legacy paths from the pre-redesign site.
    if (url.pathname === "/brief-2026-08" || url.pathname === "/brief-2026-08.html") {
      return Response.redirect(url.origin + "/", 301);
    }

    if (url.pathname === "/api/signup") {
      if (request.method !== "POST") return new Response("method not allowed", { status: 405 });
      let body;
      try { body = await request.json(); } catch { return new Response("bad json", { status: 400 }); }
      const email = (body.email || "").trim().slice(0, 200);
      const name = (body.name || "").trim().slice(0, 200);
      const address = (body.address || "").trim().slice(0, 300);
      if (!email || !email.includes("@")) return new Response("email required", { status: 400 });
      if (!env.SIGNUPS) return new Response("list unavailable", { status: 503 });
      const key = "signup:" + email.toLowerCase();
      const existing = await env.SIGNUPS.get(key, "json");
      await env.SIGNUPS.put(key, JSON.stringify({
        email, name, address,
        first: existing ? existing.first : new Date().toISOString(),
        last: new Date().toISOString(),
      }));
      if (!existing) await bumpCount(env, "signup"); // count distinct signups, no PII
      return new Response(JSON.stringify({ ok: true }), { headers: { "Content-Type": "application/json" } });
    }

    // Count-only engagement counter. Aggregate integers only: NO addresses, NO PII,
    // no IP storage. POST {event:"lookup"|"letter"} increments; GET returns totals.
    if (url.pathname === "/api/count") {
      if (!env.SIGNUPS) return json({ lookup: 0, letter: 0, signup: 0 });
      if (request.method === "GET") {
        const [lookup, letter, signup] = await Promise.all([
          readCount(env, "lookup"), readCount(env, "letter"), readCount(env, "signup"),
        ]);
        return json({ lookup, letter, signup });
      }
      if (request.method === "POST") {
        let body;
        try { body = await request.json(); } catch { return new Response("bad json", { status: 400 }); }
        const event = (body && body.event || "").trim();
        if (event !== "lookup" && event !== "letter") return new Response("bad event", { status: 400 });
        const n = await bumpCount(env, event);
        return json({ ok: true, event, count: n });
      }
      return new Response("method not allowed", { status: 405 });
    }

    return env.ASSETS.fetch(request);
  },
};

// KV has no atomic increment; read-modify-write is fine for a non-critical,
// count-only tally (a lost race under-counts by one, never leaks anything).
function json(obj) {
  return new Response(JSON.stringify(obj), { headers: { "Content-Type": "application/json" } });
}
async function readCount(env, event) {
  const v = parseInt(await env.SIGNUPS.get("count:" + event), 10);
  return Number.isFinite(v) ? v : 0;
}
async function bumpCount(env, event) {
  const n = (await readCount(env, event)) + 1;
  await env.SIGNUPS.put("count:" + event, String(n));
  return n;
}
