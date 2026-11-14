/* Actual-game runtime regression harness. No mocked graphics or replacement simulation.
 * Invoke after creating a planet: await StellaHarness.run(). Results are downloadable.
 * This intentionally changes the test planet. Do not use on a save you want unchanged.
 */
(function (root) {
  'use strict';
  const delay = ms => new Promise(resolve => setTimeout(resolve, ms));
  const assert = (condition, message) => { if (!condition) throw new Error(message); };
  async function run(options = {}) {
    const module = options.module || root.Module;
    const canvas = options.canvas || document.getElementById('canvas');
    const report = { schema: 1, started: new Date().toISOString(), status: 'running',
      scope: 'Actual WASM camera/land/tool state, with canvas captures. Not a visual-quality assertion.',
      viewport: { width: innerWidth, height: innerHeight, dpr: devicePixelRatio }, tests: [], captures: [] };
    const call = (name, ...args) => {
      const fn = module && module['_' + name];
      if (typeof fn !== 'function') throw new Error('Missing WASM export: ' + name);
      return fn(...args);
    };
    const capture = label => { try { report.captures.push({label, png:canvas.toDataURL('image/png')}); } catch (e) { report.captures.push({label,error:String(e)}); } };
    async function check(name, body) {
      try { const details = await body(); report.tests.push({name,status:'passed',details}); }
      catch (error) { report.tests.push({name,status:'failed',error:String(error)}); throw error; }
    }
    try {
      if (!module || module.failed || !module.started || typeof module._stella_camera_distance !== 'function' || call('stella_camera_distance') <= 0) {
        report.status = 'blocked'; report.reason = 'A running, rendered planet is required. Press Play and create a planet first. Graphics startup failure is not a passing test.';
        return report;
      }
      if (typeof module._stella_world_mode === 'function' && call('stella_world_mode') === 1) {
        report.status = 'blocked'; report.reason = 'This camera/plant/rabbit regression suite requires a disposable Sandbox planet. Origin has different habitat and tools; see the separate executed Origin model and graphics tests.';
        return report;
      }
      await check('live-render-surface', async () => {
        assert(canvas.width > 0 && canvas.height > 0, 'Canvas has no dimensions');
        assert(canvas.getContext('webgl2'), 'No live WebGL2 context');
        return {width:canvas.width,height:canvas.height};
      });
      await check('dry-land-focus', async () => {
        assert(call('stella_focus_land') === 1, 'No dry land found'); await delay(1000);
        assert(call('stella_test_pick', canvas.width / 2, canvas.height / 2) >= 0, 'Center-screen ray missed focused planet');
        const point = call('stella_selected_point'), water = call('stella_selected_water');
        assert(point >= 0 && water < 0.1, 'Focused selection is not dry land');
        capture('land-before-edit'); return {point,water,distance:call('stella_camera_distance')};
      });
      await check('zoom-in-and-out', async () => {
        const initial = call('stella_camera_distance'); call('stella_zoom', 2); await delay(1000);
        const near = call('stella_camera_distance'); assert(near < initial * 0.98, 'Zoom in did not materially change camera');
        capture('zoomed-in'); call('stella_zoom', -4); await delay(1000);
        const far = call('stella_camera_distance'); assert(far > near * 1.02, 'Zoom out did not materially change camera');
        capture('zoomed-out'); return {initial,near,far};
      });
      await check('touch-pinch-camera-and-input-isolation', async () => {
        assert(typeof root.createStellaTouchControls === 'function', 'Touch controller missing');
        call('stella_focus_land'); await delay(300);
        const mouseEvents = [];
        const input = root.createStellaTouchControls({
          mouse: (type,p,button) => { mouseEvents.push(type); canvas.dispatchEvent(new MouseEvent(type,{bubbles:true,...p,button,buttons:type==='mouseup'?0:button===2?2:1})); },
          zoom: steps => call('stella_zoom',steps)
        });
        const p=(id,x,y,type='pointerdown')=>({pointerId:id,pointerType:'touch',clientX:x,clientY:y,type,preventDefault(){}});
        const before=call('stella_target_distance');
        input.down(p(1,100,250)); input.down(p(2,200,250)); input.move(p(2,260,250,'pointermove'));
        const closer=call('stella_target_distance'); assert(closer<before, 'Pinch spread failed to zoom in');
        input.move(p(2,150,250,'pointermove'));
        const farther=call('stella_target_distance'); assert(farther>closer, 'Pinch close failed to zoom out');
        input.up(p(2,150,250,'pointerup')); input.move(p(1,110,260,'pointermove')); input.up(p(1,110,260,'pointerup'));
        assert(mouseEvents.length===0, 'Pinch accidentally sent a tool click');
        input.reset(); await delay(500); capture('touch-pinch');
        return {before,closer,farther,mouseEvents,input:'Production gesture controller + real WASM camera; physical Android touch not asserted'};
      });
      await check('plant-real-tile', async () => {
        call('stella_focus_land'); await delay(1000);
        const point = call('stella_selected_point'), before = call('stella_selected_vegetation');
        assert(call('stella_test_action', 3) === 1, 'Actual plant action rejected');
        const after = call('stella_selected_vegetation'); assert(after >= 0.34, 'Seedling vegetation not planted');
        await delay(100); capture('planted'); return {point,before,after};
      });
      await check('canvas-pointer-tool-gesture', async () => {
        call('stella_focus_land'); await delay(300);
        const rect = canvas.getBoundingClientRect();
        const columns = canvas.width >= 650 ? 7 : 4;
        const bw = (canvas.width - 16 - (columns - 1) * 6) / columns;
        async function gesture(x, y) {
          const clientX = rect.left + x / canvas.width * rect.width;
          const clientY = rect.top + y / canvas.height * rect.height;
          canvas.dispatchEvent(new MouseEvent('mousemove',{bubbles:true,clientX,clientY}));
          canvas.dispatchEvent(new MouseEvent('mousedown',{bubbles:true,clientX,clientY,button:0,buttons:1}));
          await delay(120);
          canvas.dispatchEvent(new MouseEvent('mouseup',{bubbles:true,clientX,clientY,button:0,buttons:0}));
          await delay(120);
        }
        // Land+ is toolbar slot 4 (not enum value). Exercise real canvas UI then surface input.
        await gesture(8 + (4 % columns) * (bw + 6) + bw/2, 58 + Math.floor(4/columns)*54 + 22);
        call('stella_test_pick',canvas.width/2,canvas.height/2);
        const before = call('stella_selected_elevation');
        await gesture(canvas.width/2,canvas.height/2);
        const after = call('stella_selected_elevation');
        assert(after > before,'Canvas toolbar/touch-equivalent mouse gesture failed to raise terrain');
        return {before,after,input:'Canvas mouse events through real UI; physical touch translation not asserted'};
      });
      await check('raise-real-terrain', async () => {
        const before = call('stella_selected_elevation');
        assert(call('stella_test_action', 5) === 1, 'Actual raise action rejected');
        const after = call('stella_selected_elevation'); assert(after > before, 'Terrain did not rise');
        return {before,after};
      });
      await check('reset-globe', async () => {
        const before = call('stella_camera_distance'); call('stella_reset_view'); await delay(1000);
        const after = call('stella_camera_distance'); assert(after > before, 'Globe reset failed to pull back');
        capture('whole-globe');
        const sky = call('stella_test_pick', 1, 1);
        assert(sky === -1, 'Corner sky incorrectly selected land');
        assert(call('stella_test_action', 3) === 0, 'Sky touch incorrectly modified a tile');
        return {before,after,sky};
      });
      report.status = 'passed';
    } catch (error) { report.status = 'failed'; report.reason = String(error); }
    finally { report.finished = new Date().toISOString(); root.StellaHarness.lastReport = report; }
    return report;
  }
  function download(report = root.StellaHarness.lastReport) {
    if (!report) throw new Error('Run the harness first');
    const link=document.createElement('a'); link.href=URL.createObjectURL(new Blob([JSON.stringify(report,null,2)],{type:'application/json'}));
    link.download='stella-gameplay-'+Date.now()+'.json'; link.click(); setTimeout(()=>URL.revokeObjectURL(link.href),1000);
  }
  root.StellaHarness = {run,download,lastReport:null};
})(globalThis);
