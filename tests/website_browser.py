#!/usr/bin/env python3
"""Exercise the public website and documentation in a real browser on loopback only."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import os,urllib.parse
base=os.getenv('SCHOOLOS_WEBSITE_BASE','http://127.0.0.1:8090/experience/index.php');assert urllib.parse.urlsplit(base).hostname in ('localhost','127.0.0.1')
out=Path(__file__).resolve().parents[1]/'docs/5.2.0/test-output';out.mkdir(parents=True,exist_ok=True)
n=0
def ok(v,msg):
 global n
 assert v,msg;n+=1;print('PASS',msg,flush=True)
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':1440,'height':1000},device_scale_factor=1)
 errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(base+'?home=1');ok(page.locator('h1').inner_text().find('flourish')>=0,'new website hero renders')
 page.screenshot(path=str(out/'website-desktop.png'),full_page=True)
 old=page.locator('#fun-fact').inner_text();page.locator('#next-fact').click();ok(page.locator('#fun-fact').inner_text()!=old,'academic fact control works')
 page.locator('[data-answer="4"]').click();ok('Try again' in page.locator('#quiz-result').inner_text(),'quiz explains incorrect answer');page.locator('[data-answer="6"]').click();ok('Exactly!' in page.locator('#quiz-result').inner_text(),'quiz explains correct arithmetic')
 for key in ['onboarding','parent','owner']:
  page.locator('[data-preview="'+key+'"]').click();ok(page.locator('[data-preview="'+key+'"]').get_attribute('aria-pressed')=='true' and key in page.locator('#dashboard-preview').get_attribute('src'),'dashboard snapshot selection '+key)
 for route in ['features','how-it-works','affiliate','documentation','about','contact','privacy','terms','cookies','affiliate-account']:
  response=page.goto(base+'?page='+route);ok(response.status==200 and page.locator('h1').count()==1,'populated public route '+route)
 page.goto(base+'?page=documentation');guides=page.locator('a[href^="?guide="]:not([href*="download"])').evaluate_all('(links)=>links.map(a=>a.getAttribute("href"))');ok(len(guides)==18,'eighteen role guides listed')
 for guide in guides:
  response=page.goto(base+guide);ok(response.status==200 and page.locator('.guide-section').count()>=2,'accessible online guide '+guide)
  pdf=page.request.get(base+guide+'&download=pdf');ok(pdf.status==200 and pdf.body().startswith(b'%PDF-1.4') and pdf.body().endswith(b'%%EOF') and 'attachment' in pdf.headers['content-disposition'],'downloadable valid PDF '+guide)
 response=page.goto(base+'?guide=../../config.php');ok(response.status==404,'download traversal rejected')
 response=page.goto(base+'?page=unknown');ok(response.status==404,'unknown public page returns 404')
 for width in [390,768]:
  page.set_viewport_size({'width':width,'height':844})
  for route in ['home','features','how-it-works','documentation','affiliate','privacy']:
   page.goto(base+('?home=1' if route=='home' else '?page='+route));ok(page.evaluate('document.documentElement.scrollWidth<=window.innerWidth'),'no horizontal overflow '+route+' '+str(width))
  page.goto(base+'?home=1');page.locator('.menu').click();ok(page.locator('.menu').get_attribute('aria-expanded')=='true' and page.locator('#webnav').is_visible(),'mobile menu opens '+str(width));page.keyboard.press('Escape');ok(page.locator('.menu').get_attribute('aria-expanded')=='false','Escape closes mobile menu '+str(width))
  if width==390:page.screenshot(path=str(out/'website-mobile.png'),full_page=True)
 page.emulate_media(reduced_motion='reduce');ok(page.locator('.math span').first.evaluate('(el)=>getComputedStyle(el).animationName')=='none','reduced-motion preference stops decorative animation')
 ok(not errors,'no browser JavaScript errors');browser.close()
print('Website browser:',n,'assertions passed.')
