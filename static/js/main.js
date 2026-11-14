/* Department breakdown chart — draws onto #deptChart via Canvas 2D.
   Reads data from window.__DEPT_DATA__ (set inline in dashboard.html). */
document.addEventListener("DOMContentLoaded", () => {
  const canvas = document.getElementById("deptChart");
  if (!canvas) return;

  const data = window.__DEPT_DATA__ || [];
  const ctx = canvas.getContext("2d");

  // Handle high-DPI screens so the chart isn't fuzzy
  const dpr = window.devicePixelRatio || 1;
  const cssW = canvas.clientWidth || 640;
  const cssH = 280;
  canvas.width  = cssW * dpr;
  canvas.height = cssH * dpr;
  canvas.style.width  = cssW + "px";
  canvas.style.height = cssH + "px";
  ctx.scale(dpr, dpr);

  if (data.length === 0) {
    ctx.fillStyle = "#94a3b8";
    ctx.font = "13px Inter, system-ui, sans-serif";
    ctx.textAlign = "center";
    ctx.fillText("No departments yet", cssW / 2, cssH / 2);
    return;
  }

  const paddingLeft   = 110;   // room for department names
  const paddingRight  = 60;    // room for value labels
  const paddingTop    = 12;
  const paddingBottom = 12;
  const rowH          = (cssH - paddingTop - paddingBottom) / data.length;
  const barH          = Math.min(rowH - 12, 26);
  const maxCount      = Math.max(...data.map(d => d.count), 1);
  const chartW        = cssW - paddingLeft - paddingRight;

  let t = 0;
  const duration = 500;

  function draw(progress) {
    ctx.clearRect(0, 0, cssW, cssH);

    data.forEach((d, i) => {
      const y = paddingTop + i * rowH + (rowH - barH) / 2;
      const fullW = (d.count / maxCount) * chartW;
      const w = fullW * progress;

      // Department label
      ctx.fillStyle = "#334155";
      ctx.font = "500 13px Inter, system-ui, sans-serif";
      ctx.textAlign = "right";
      ctx.textBaseline = "middle";
      ctx.fillText(d.name, paddingLeft - 14, y + barH / 2);

      // Bar background
      ctx.fillStyle = "#f1f5f9";
      roundRect(ctx, paddingLeft, y, chartW, barH, barH / 2);
      ctx.fill();

      // Bar fill
      const grad = ctx.createLinearGradient(paddingLeft, 0, paddingLeft + w, 0);
      grad.addColorStop(0, "#6366f1");
      grad.addColorStop(1, "#4f46e5");
      ctx.fillStyle = grad;
      roundRect(ctx, paddingLeft, y, Math.max(w, 2), barH, barH / 2);
      ctx.fill();

      // Value label
      ctx.fillStyle = "#0f172a";
      ctx.font = "600 13px Inter, system-ui, sans-serif";
      ctx.textAlign = "left";
      ctx.fillText(d.count, paddingLeft + w + 10, y + barH / 2);
    });
  }

  function roundRect(c, x, y, w, h, r) {
    c.beginPath();
    c.moveTo(x + r, y);
    c.arcTo(x + w, y, x + w, y + h, r);
    c.arcTo(x + w, y + h, x, y + h, r);
    c.arcTo(x, y + h, x, y, r);
    c.arcTo(x, y, x + w, y, r);
    c.closePath();
  }

  function animate(now) {
    if (!t) t = now;
    const p = Math.min((now - t) / duration, 1);
    draw(p);
    if (p < 1) requestAnimationFrame(animate);
  }

  requestAnimationFrame(animate);
});