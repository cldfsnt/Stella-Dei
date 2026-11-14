from pathlib import Path
import json,asyncio
from playwright.async_api import async_playwright
root=Path(__file__).resolve().parents[1];web=root/'repo/web';out=root/'results';out.mkdir(exist_ok=True)
# Production shell HTML/CSS/handlers, with no WASM loader. Mocked read-only API
# below supplies deterministic diagnostic content; this is not game-engine QA.
s=(web/'shell.html').read_text().replace('{{{ SCRIPT }}}','').replace('{{{SCRIPT}}}','');(web/'qa-shell.html').write_text(s)
async def main():
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage'],env={'TMPDIR':str(root/'cache')})
  results=[]
  for width,height in [(320,700),(390,700),(640,360)]:
   page=await browser.new_page(viewport={'width':width,'height':height},device_scale_factor=1)
   await page.goto((web/'qa-shell.html').as_uri())
   await page.evaluate('''()=>{
     window.perfEnables=[];Module.started=true;Module.failed=false;document.body.classList.add('playing');document.getElementById('cover').hidden=true;
     Module._stella_speed_snapshot=()=>1;Module._stella_performance_snapshot=()=>1;
     Module._stella_performance_enable=x=>{perfEnables.push(x);return 1};
     Module.ccall=name=>JSON.stringify(name==='stella_speed_snapshot'?{requested:86400,achieved:18000,paused:false,step:1440,steps_last_frame:1}:{enabled:true,cells:40962,frames:60,ticks:61,physics_frames:60,frame_avg_ms:92.3,frame_max_ms:191.1,frame_p95_ms:130,long_frames:60,physics_avg_ms:22.4,physics_max_ms:47.1,render_cpu_avg_ms:68,render_cpu_max_ms:156.6,stage_sum_ms:[100,1000,2000,300],stage_max_ms:[12,40,60,15],render_context:{world:'origin',map:'normal',stable_daylight:true,orbit:true,animals:0,camera_valid:true,camera_radius:5400,planet_radius:5000,canvas_width:390,canvas_height:700,scene_width:390,scene_height:700,bloom_passes:0}});
   }''')
   await page.locator('#more-toggle').click();await page.locator('#speed-toggle').click();await page.locator('#performance-details summary').click()
   await page.wait_for_timeout(50)
   assert await page.evaluate('perfEnables.at(-1)')==1
   await page.locator('#speed-sheet').evaluate('(e)=>e.scrollTop=e.scrollHeight')
   await page.wait_for_timeout(50)
   bounds=await page.evaluate('''()=>{const box=id=>{const r=document.getElementById(id).getBoundingClientRect();return {left:r.left,right:r.right,top:r.top,bottom:r.bottom,width:r.width,height:r.height}};const d=document.getElementById('speed-sheet'),b=box('close-speed');return {dialog:box('speed-sheet'),close:b,heading:document.querySelector('#speed-sheet .sheet-heading').getBoundingClientRect().toJSON(),scroll:d.scrollTop,overflow:d.scrollWidth-d.clientWidth,hit:document.elementFromPoint((b.left+b.right)/2,(b.top+b.bottom)/2).id}}''')
   assert bounds['scroll']>0,bounds
   assert bounds['close']['top']>=bounds['dialog']['top'] and bounds['close']['bottom']<=bounds['dialog']['bottom'],bounds
   assert bounds['close']['width']>=44 and bounds['close']['height']>=44 and bounds['hit']=='close-speed',bounds
   assert bounds['overflow']<=1,bounds
   await page.screenshot(path=str(out/f'speed-bottom-{width}x{height}.png'))
   await page.locator('#close-speed').click();await page.wait_for_timeout(20)
   assert await page.evaluate('perfEnables.at(-1)')==0
   await page.locator('#more-toggle').click();await page.locator('#speed-toggle').click()
   assert await page.locator('#speed-sheet').evaluate('(e)=>e.scrollTop')==0
   assert not await page.locator('#performance-details').evaluate('(e)=>e.open')
   await page.locator('#performance-details summary').click();await page.wait_for_timeout(20);await page.keyboard.press('Escape');await page.wait_for_timeout(20)
   assert not await page.locator('#speed-sheet').evaluate('(e)=>e.open')
   assert await page.evaluate('perfEnables.at(-1)')==0
   results.append({'viewport':[width,height],'bottom_bounds':bounds,'close_reopen_escape_pass':True})
   await page.close()
  await browser.close();(out/'browser.json').write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2))
asyncio.run(main())
