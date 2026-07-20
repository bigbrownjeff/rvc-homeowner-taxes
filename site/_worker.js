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
      return new Response(JSON.stringify({ ok: true }), { headers: { "Content-Type": "application/json" } });
    }

    return env.ASSETS.fetch(request);
  },
};
