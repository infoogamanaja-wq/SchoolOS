from pathlib import Path
from playwright.sync_api import sync_playwright
import os
base=os.getenv('SCHOOLOS_WEBSITE_BASE','http://127.0.0.1:8090/experience/index.php');out=Path(__file__).resolve().parents[1]/'docs/5.2.1/test-output';out.mkdir(parents=True,exist_ok=True);n=0

def ok(v,m):
 global n
 assert v,m;n+=1;print('PASS',m,flush=True)
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);context=browser.new_context(viewport={'width':1440,'height':1000},color_scheme='light');page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(base+'?home=1');ok(page.locator('[data-schoolos-logo]').first.inner_text()=='✳','shared public logo mark')
 before=page.locator('.math span').first.evaluate('(el)=>getComputedStyle(el).transform');page.wait_for_timeout(600);after=page.locator('.math span').first.evaluate('(el)=>getComputedStyle(el).transform');ok(before!=after,'education doodles actually move over time')
 first=page.locator('#hero-word').inner_text();page.wait_for_timeout(4400);ok(page.locator('#hero-word').inner_text()!=first,'headline rotates through inspiring text')
 page.locator('.web-motion').click();word=page.locator('#hero-word').inner_text();page.wait_for_timeout(4500);ok(page.locator('#hero-word').inner_text()==word,'pause stops automatic text rotation');ok(page.locator('.math span').first.evaluate('(el)=>getComputedStyle(el).animationPlayState')=='paused','pause stops decorative motion');page.reload();ok(page.locator('.web-motion').get_attribute('aria-pressed')=='true','motion preference survives reload');page.locator('.web-motion').click()
 page.locator('.web-theme').click();ok(page.locator('html').get_attribute('data-theme')=='dark','night theme button works');page.reload();ok(page.locator('html').get_attribute('data-theme')=='dark','night preference survives reload');page.goto(base+'?page=features');ok(page.locator('html').get_attribute('data-theme')=='dark','night preference applies across public pages');ok(page.locator('body').evaluate('(el)=>getComputedStyle(el).backgroundColor')=='rgb(16, 29, 26)','night background uses dark surface')
 page.goto(base+'?home=1');page.locator('.cards article').first.hover();page.wait_for_timeout(400);ok(page.locator('.cards article').first.evaluate('(el)=>getComputedStyle(el,":before").opacity')=='1','cards respond to pointer hover with spotlight');ok(page.locator('.cards article').first.evaluate('(el)=>getComputedStyle(el).borderTopColor')=='rgb(188, 223, 145)','hover border highlights in night theme')
 data=page.evaluate('window.SchoolOSChallenges');ok(len(data)==36 and len({c['question'] for c in data})==36,'36 distinct challenge questions');ok(len({c['topic'] for c in data})==6,'six academic and digital topics');ok(all(c['correct'] in c['options'] and len(c['options'])==len(set(c['options'])) and c['explanation'] for c in data),'every challenge has valid options, answer and explanation')
 seen=set()
 for i in range(36):
  question=page.locator('#quiz-question').inner_text();ok(question not in seen,'challenge deck avoids repeats '+str(i+1));seen.add(question);c=next(c for c in data if c['question']==question);button=page.locator('.quiz-answers button').filter(has_text=c['correct']);button=next(b for b in page.locator('.quiz-answers button').all() if b.inner_text()==c['correct']);button.click();ok(c['explanation'] in page.locator('#quiz-result').inner_text(),'correct feedback '+str(i+1));page.locator('#next-challenge').click()
 ok('36 discoveries solved' in page.locator('#quiz-score').inner_text(),'score counts unique solved questions');
 for topic in sorted({c['topic'] for c in data}):
  page.locator('#quiz-topic').select_option(topic);seen_topic=set()
  for _ in range(6):
   question=page.locator('#quiz-question').inner_text();seen_topic.add(question);ok(next(c for c in data if c['question']==question)['topic']==topic,'topic filter '+topic);page.locator('#next-challenge').click()
  ok(len(seen_topic)==6,'topic deck has six different questions '+topic)
 for width in [360,390,768,1024]:
  page.set_viewport_size({'width':width,'height':844});page.goto(base+'?home=1');ok(page.evaluate('document.documentElement.scrollWidth<=innerWidth'),'no horizontal overflow '+str(width));ok(page.locator('.web-theme').is_visible(),'theme switch accessible '+str(width));page.locator('#quiz-topic').select_option('Digital skills');page.locator('.quiz').scroll_into_view_if_needed();ok(page.evaluate('document.documentElement.scrollWidth<=innerWidth'),'long answer controls fit '+str(width))
 page.set_viewport_size({'width':1440,'height':1000});page.goto(base+'?home=1');
 for y in range(0,page.evaluate('document.documentElement.scrollHeight'),650):page.evaluate('(y)=>window.scrollTo(0,y)',y);page.wait_for_timeout(100)
 page.wait_for_timeout(800);page.evaluate('scrollTo(0,0)');page.screenshot(path=str(out/'website-night-desktop.png'),full_page=True);page.locator('.web-theme').click();page.screenshot(path=str(out/'website-day-desktop.png'),full_page=True)
 page.set_viewport_size({'width':390,'height':844});page.locator('.web-theme').click();page.screenshot(path=str(out/'website-night-mobile.png'),full_page=True)
 page.emulate_media(reduced_motion='reduce');ok(page.locator('.math span').first.evaluate('(el)=>getComputedStyle(el).animationName')=='none','reduced motion disables doodle animation');ok(page.locator('.reveal-ready').first.evaluate('(el)=>getComputedStyle(el).opacity')=='1','reduced motion preserves visible content')
 # Authentication and dashboard share the same platform mark; school-specific branding is separate.
 page.goto(base+'?login=1');ok(page.locator('[data-schoolos-logo]').first.inner_text()=='✳','login brand matches public site');page.locator('[data-demo-role=schooladmin]').click();page.locator('button[name=login]').click();page.wait_for_url('**s=workspace');ok(page.locator('.sidehead [data-schoolos-logo]').inner_text()=='✳','dashboard brand matches public site');ok(page.locator('html').get_attribute('data-theme')=='dark','saved website theme carries into dashboard')
 ok(not errors,'no JavaScript browser errors');browser.close()
print('Interactive website:',n,'assertions passed.')
