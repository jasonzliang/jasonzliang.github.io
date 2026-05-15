// Click "Jason Liang" in the nav to summon a Lorenz attractor.
// After the animation, the attractor opens a random paper or patent
// scraped live from publications.html.
// Reference: Liang, "Self-Transcendence: Achieving AGI via Chaotic Dynamics
// and Thermodynamic Attractors" (2025).

(function () {
  const css = [
    'color:#1a4d80;font:600 16px/1.4 Inter,sans-serif',
    'color:#555;font:italic 13px/1.6 Lora,serif',
    'color:#888;font:11px Inter,sans-serif'
  ];
  console.log('%cHello, fellow researcher.', css[0]);
  console.log('%cIntelligence is the attractor a system finds when it forgets it was searching.', css[1]);
  console.log('%cP.S. try clicking my name.', css[2]);

  const brand = document.querySelector('.brand');
  if (!brand) return;

  let running = false;

  // Resolve publications.html relative to whatever page we're on.
  const pubsUrl = new URL('publications.html', location.href).href;

  function fetchRandomLinks() {
    return fetch(pubsUrl, { cache: 'no-store' })
      .then(r => r.text())
      .then(html => {
        const doc = new DOMParser().parseFromString(html, 'text/html');
        return Array.from(doc.querySelectorAll('.pub-title'))
          .map(a => a.getAttribute('href'))
          .filter(href => href && /^https?:/i.test(href));
      })
      .catch(() => []);
  }

  brand.addEventListener('click', (e) => {
    if (running) return;
    e.preventDefault();
    // Kick off the fetch in parallel with the animation so the URL list
    // is ready (or already failed) by the time the attractor finishes.
    const linksPromise = fetchRandomLinks();
    runAttractor(async () => {
      const links = await linksPromise;
      if (links.length) {
        window.location.href = links[Math.floor(Math.random() * links.length)];
      } else {
        // Fallback: drop the visitor on the publications page.
        window.location.href = pubsUrl;
      }
    });
  });

  function runAttractor(done) {
    running = true;

    const veil = document.createElement('div');
    veil.style.cssText =
      'position:fixed;inset:0;background:radial-gradient(ellipse at center,' +
      'rgba(4,8,20,0.92),rgba(0,0,0,0.98));pointer-events:none;' +
      'z-index:9998;opacity:0;transition:opacity 0.35s ease';
    document.body.appendChild(veil);
    requestAnimationFrame(() => { veil.style.opacity = '1'; });

    const flash = document.createElement('div');
    flash.style.cssText =
      'position:fixed;inset:0;background:#fff;pointer-events:none;' +
      'z-index:10000;opacity:0;transition:opacity 0.5s ease';
    document.body.appendChild(flash);
    requestAnimationFrame(() => {
      flash.style.opacity = '0.85';
      setTimeout(() => { flash.style.opacity = '0'; }, 60);
      setTimeout(() => flash.remove(), 700);
    });

    const canvas = document.createElement('canvas');
    canvas.style.cssText =
      'position:fixed;inset:0;width:100vw;height:100vh;pointer-events:none;' +
      'z-index:9999;opacity:0;transition:opacity 0.35s ease';
    const dpr = window.devicePixelRatio || 1;
    const W = window.innerWidth;
    const H = window.innerHeight;
    canvas.width = W * dpr;
    canvas.height = H * dpr;
    document.body.appendChild(canvas);
    requestAnimationFrame(() => { canvas.style.opacity = '1'; });

    const ctx = canvas.getContext('2d');
    ctx.scale(dpr, dpr);
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';

    // Lorenz: x in ~[-22,22], z in ~[0,50]. Fit the full z range vertically
    // with margin so neither lobe clips.
    const margin = 60;
    const scale = Math.min((W - margin * 2) / 50, (H - margin * 2) / 55);
    const cx = W / 2;
    const cy = H / 2;

    const sigma = 10, rho = 28, beta = 8 / 3;
    const dt = 0.005;

    // Five trajectories with infinitesimally different initial conditions —
    // they diverge chaotically. Sensitive dependence on initial conditions.
    const baseHues = [200, 320, 80, 0, 160];
    const trails = baseHues.map((hue, i) => ({
      x: 0.1 + (i - 2) * 1e-5,
      y: 0,
      z: 0,
      prev: null,
      hue,
      sparks: []
    }));

    const TOTAL = 720;
    const FADE_START = TOTAL - 90;
    let frame = 0;

    // body shake during the loud phase
    const originalTransform = document.body.style.transform;

    function step() {
      // breathing background pulse
      const pulse = 0.92 + 0.08 * Math.sin(frame * 0.05);
      veil.style.opacity = String(pulse);

      // subtle screen shake while drawing
      if (frame < FADE_START) {
        const amp = 2.5;
        const sx = (Math.random() - 0.5) * amp;
        const sy = (Math.random() - 0.5) * amp;
        document.body.style.transform = `translate(${sx}px,${sy}px)`;
      }

      for (let i = 0; i < 18; i++) {
        for (const t of trails) {
          const dx = sigma * (t.y - t.x) * dt;
          const dy = (t.x * (rho - t.z) - t.y) * dt;
          const dz = (t.x * t.y - beta * t.z) * dt;
          t.x += dx; t.y += dy; t.z += dz;
          const px = cx + t.x * scale;
          const py = cy + (t.z - 25) * scale;
          if (t.prev) {
            // Layered glow — saturated colors, no near-white core.
            ctx.strokeStyle = `hsla(${t.hue % 360}, 100%, 50%, 0.08)`;
            ctx.lineWidth = 22;
            ctx.beginPath();
            ctx.moveTo(t.prev.x, t.prev.y);
            ctx.lineTo(px, py);
            ctx.stroke();

            ctx.strokeStyle = `hsla(${t.hue % 360}, 100%, 55%, 0.20)`;
            ctx.lineWidth = 11;
            ctx.beginPath();
            ctx.moveTo(t.prev.x, t.prev.y);
            ctx.lineTo(px, py);
            ctx.stroke();

            ctx.strokeStyle = `hsla(${t.hue % 360}, 100%, 60%, 0.55)`;
            ctx.lineWidth = 5;
            ctx.beginPath();
            ctx.moveTo(t.prev.x, t.prev.y);
            ctx.lineTo(px, py);
            ctx.stroke();

            ctx.strokeStyle = `hsla(${t.hue % 360}, 100%, 70%, 0.95)`;
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(t.prev.x, t.prev.y);
            ctx.lineTo(px, py);
            ctx.stroke();

            t.hue += 0.05;
          }
          t.prev = { x: px, y: py };
        }
      }

      // colored sparks at trail heads
      if (frame % 4 === 0) {
        for (const t of trails) {
          if (!t.prev) continue;
          ctx.fillStyle = `hsla(${t.hue % 360}, 100%, 60%, 0.55)`;
          ctx.beginPath();
          ctx.arc(t.prev.x, t.prev.y, 6 + Math.random() * 3, 0, Math.PI * 2);
          ctx.fill();
          ctx.fillStyle = `hsla(${t.hue % 360}, 100%, 75%, 0.95)`;
          ctx.beginPath();
          ctx.arc(t.prev.x, t.prev.y, 2.4, 0, Math.PI * 2);
          ctx.fill();
        }
      }

      if (frame > FADE_START) {
        const o = Math.max(0, 1 - (frame - FADE_START) / 90);
        canvas.style.opacity = String(o);
        veil.style.opacity = String(o * pulse);
        document.body.style.transform = originalTransform;
      }

      frame++;
      if (frame < TOTAL) {
        requestAnimationFrame(step);
      } else {
        canvas.remove();
        veil.remove();
        document.body.style.transform = originalTransform;
        running = false;
        if (done) done();
      }
    }
    step();
  }
})();
