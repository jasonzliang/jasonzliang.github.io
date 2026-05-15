// Click "Jason Liang" in the nav to summon a Lorenz attractor.
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

  brand.addEventListener('click', (e) => {
    if (running) return;
    e.preventDefault();
    runAttractor(() => {
      const path = location.pathname;
      const onIndex = path === '/' || /(^|\/)index\.html?$/.test(path);
      if (!onIndex) window.location.href = brand.getAttribute('href');
    });
  });

  function runAttractor(done) {
    running = true;

    const veil = document.createElement('div');
    veil.style.cssText =
      'position:fixed;inset:0;background:radial-gradient(ellipse at center,' +
      'rgba(8,12,24,0.85),rgba(0,0,0,0.95));pointer-events:none;' +
      'z-index:9998;opacity:0;transition:opacity 0.4s ease';
    document.body.appendChild(veil);
    requestAnimationFrame(() => { veil.style.opacity = '1'; });

    const canvas = document.createElement('canvas');
    canvas.style.cssText =
      'position:fixed;inset:0;width:100vw;height:100vh;pointer-events:none;' +
      'z-index:9999;opacity:0;transition:opacity 0.4s ease';
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
    const cx = W / 2;
    const cy = H / 2 + Math.min(W, H) * 0.18;
    const scale = Math.min(W, H) / 38;

    const sigma = 10, rho = 28, beta = 8 / 3;
    const dt = 0.005;

    // Three trajectories with infinitesimally different initial conditions —
    // they diverge chaotically, which is the whole point of the attractor.
    const trails = [
      { x: 0.10, y: 0, z: 0, prev: null, hue: 200 },
      { x: 0.10001, y: 0, z: 0, prev: null, hue: 320 },
      { x: 0.09999, y: 0, z: 0, prev: null, hue: 80 }
    ];

    const TOTAL = 520;
    const FADE_START = TOTAL - 80;
    let frame = 0;

    function step() {
      for (let i = 0; i < 14; i++) {
        for (const t of trails) {
          const dx = sigma * (t.y - t.x) * dt;
          const dy = (t.x * (rho - t.z) - t.y) * dt;
          const dz = (t.x * t.y - beta * t.z) * dt;
          t.x += dx; t.y += dy; t.z += dz;
          const px = cx + t.x * scale;
          const py = cy + (t.z - 25) * scale;
          if (t.prev) {
            // Outer glow
            ctx.strokeStyle = `hsla(${t.hue % 360}, 100%, 65%, 0.18)`;
            ctx.lineWidth = 9;
            ctx.beginPath();
            ctx.moveTo(t.prev.x, t.prev.y);
            ctx.lineTo(px, py);
            ctx.stroke();
            // Mid stroke
            ctx.strokeStyle = `hsla(${t.hue % 360}, 95%, 62%, 0.55)`;
            ctx.lineWidth = 4;
            ctx.beginPath();
            ctx.moveTo(t.prev.x, t.prev.y);
            ctx.lineTo(px, py);
            ctx.stroke();
            // Bright core
            ctx.strokeStyle = `hsla(${t.hue % 360}, 100%, 88%, 0.95)`;
            ctx.lineWidth = 1.6;
            ctx.beginPath();
            ctx.moveTo(t.prev.x, t.prev.y);
            ctx.lineTo(px, py);
            ctx.stroke();
            t.hue += 0.5;
          }
          t.prev = { x: px, y: py };
        }
      }

      if (frame > FADE_START) {
        const o = Math.max(0, 1 - (frame - FADE_START) / 80);
        canvas.style.opacity = String(o);
        veil.style.opacity = String(o * 0.95);
      }

      frame++;
      if (frame < TOTAL) {
        requestAnimationFrame(step);
      } else {
        canvas.remove();
        veil.remove();
        running = false;
        if (done) done();
      }
    }
    step();
  }
})();
