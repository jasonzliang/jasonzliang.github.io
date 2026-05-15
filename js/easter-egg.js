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
    const canvas = document.createElement('canvas');
    canvas.style.cssText =
      'position:fixed;inset:0;width:100vw;height:100vh;pointer-events:none;' +
      'z-index:9999;opacity:0;transition:opacity 0.5s ease';
    const dpr = window.devicePixelRatio || 1;
    const W = window.innerWidth;
    const H = window.innerHeight;
    canvas.width = W * dpr;
    canvas.height = H * dpr;
    document.body.appendChild(canvas);
    requestAnimationFrame(() => { canvas.style.opacity = '1'; });

    const ctx = canvas.getContext('2d');
    ctx.scale(dpr, dpr);
    const cx = W / 2;
    const cy = H / 2 + Math.min(W, H) * 0.15;
    const scale = Math.min(W, H) / 60;

    const sigma = 10, rho = 28, beta = 8 / 3;
    const dt = 0.005;
    let x = 0.1, y = 0, z = 0;
    let prev = null;
    let hue = 200;

    const TOTAL = 360;
    const FADE_START = TOTAL - 60;
    let frame = 0;

    function step() {
      for (let i = 0; i < 10; i++) {
        const dx = sigma * (y - x) * dt;
        const dy = (x * (rho - z) - y) * dt;
        const dz = (x * y - beta * z) * dt;
        x += dx; y += dy; z += dz;
        const px = cx + x * scale;
        const py = cy + (z - 25) * scale;
        if (prev) {
          ctx.strokeStyle = `hsla(${hue % 360}, 75%, 60%, 0.55)`;
          ctx.lineWidth = 1.3;
          ctx.beginPath();
          ctx.moveTo(prev.x, prev.y);
          ctx.lineTo(px, py);
          ctx.stroke();
          hue += 0.35;
        }
        prev = { x: px, y: py };
      }

      if (frame > FADE_START) {
        canvas.style.opacity = String(Math.max(0, 1 - (frame - FADE_START) / 60));
      }

      frame++;
      if (frame < TOTAL) {
        requestAnimationFrame(step);
      } else {
        canvas.remove();
        running = false;
        if (done) done();
      }
    }
    step();
  }
})();
