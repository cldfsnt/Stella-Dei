/* Pointer gestures for the real WASM game. Also exported for deterministic tests. */
(function (root) {
  // Let the engine poll the pressed state on at least two frames. Cap the hold
  // so a backgrounded tab never retains an input indefinitely.
  function afterRenderedTap(callback) {
    if (typeof requestAnimationFrame !== 'function') return { timer: setTimeout(callback, 150) };
    const handle = { cancelled: false, frames: 0, minimumElapsed: false };
    const finish = () => { if (handle.cancelled) return; handle.cancelled = true; clearTimeout(handle.timer); clearTimeout(handle.minimum); cancelAnimationFrame(handle.frame); callback(); };
    const frame = () => { handle.frames++; if (handle.frames >= 2 && handle.minimumElapsed) finish(); else handle.frame = requestAnimationFrame(frame); };
    handle.minimum = setTimeout(() => { handle.minimumElapsed = true; if (handle.frames >= 2) finish(); }, 120);
    handle.timer = setTimeout(finish, 500); handle.frame = requestAnimationFrame(frame); return handle;
  }
  function cancelRenderedTap(handle) { handle.cancelled = true; clearTimeout(handle.timer); clearTimeout(handle.minimum); if (handle.frame !== undefined) cancelAnimationFrame(handle.frame); }
  function createTouchControls({ mouse, zoom, capture = () => {}, releaseCapture = () => {}, schedule = afterRenderedTap, cancel = cancelRenderedTap }) {
    const points = new Map();
    let mode = 'navigate', drag = null, start = null, pinching = false, pinchDistance = 0, tapTimer = null;
    const distance = () => { const [a, b] = [...points.values()]; return Math.hypot(a.clientX - b.clientX, a.clientY - b.clientY); };
    function finishMouse() { if (drag) mouse('mouseup', drag.point, drag.button); drag = null; if (tapTimer !== null) cancel(tapTimer); tapTimer = null; }
    function beginMouse(point, button) { finishMouse(); mouse('mousemove', point, button); mouse('mousedown', point, button); drag = { point, button }; }
    function reset() { finishMouse(); for (const id of points.keys()) releaseCapture(id); points.clear(); start = null; pinching = false; pinchDistance = 0; }
    function down(e) {
      if (e.pointerType === 'mouse') return;
      e.preventDefault();
      finishMouse();
      points.set(e.pointerId, { clientX: e.clientX, clientY: e.clientY }); capture(e.pointerId);
      if (points.size === 1) { start = { ...points.get(e.pointerId) }; pinching = false; }
      else { pinching = true; pinchDistance = distance(); start = null; }
    }
    function move(e) {
      if (!points.has(e.pointerId)) return;
      e.preventDefault(); const p = { clientX: e.clientX, clientY: e.clientY }; points.set(e.pointerId, p);
      if (points.size >= 2) {
        const next = distance();
        // stella_zoom scales altitude by 0.55^steps. Match the pinch ratio,
        // avoiding huge jumps when a finger briefly crosses its partner.
        if (pinchDistance > 12 && next > 12) zoom(Math.max(-0.8, Math.min(0.8, Math.log(pinchDistance / next) / Math.log(0.55))));
        pinchDistance = next; return;
      }
      // Keep the remaining finger inert until all fingers lift after a pinch.
      if (pinching || !start) return;
      if (!drag && Math.hypot(p.clientX - start.clientX, p.clientY - start.clientY) >= 8) beginMouse(start, mode === 'paint' ? 0 : 2);
      if (drag) { mouse('mousemove', p, drag.button); drag.point = p; }
    }
    function up(e) {
      if (!points.has(e.pointerId)) return;
      e.preventDefault(); const p = points.get(e.pointerId); points.delete(e.pointerId); releaseCapture(e.pointerId);
      if (drag) finishMouse();
      else if (!pinching && start && e.type !== 'pointercancel' && e.type !== 'lostpointercapture') {
        // Hold a tap over rendered frames so GLFW's polled buttons can see it.
        beginMouse(p, 0); tapTimer = schedule(() => { tapTimer = null; finishMouse(); }, 150);
      }
      start = null;
      if (points.size === 0) { pinching = false; pinchDistance = 0; }
      else if (points.size >= 2) pinchDistance = distance();
    }
    return { down, move, up, reset, setMode(value) { reset(); mode = value; }, state: () => ({ pointers: points.size, pinching, mode, mouseDown: !!drag }) };
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = { createTouchControls };
  else root.createStellaTouchControls = createTouchControls;
})(typeof window === 'undefined' ? globalThis : window);
