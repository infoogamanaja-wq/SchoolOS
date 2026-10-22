from playwright.sync_api import sync_playwright
from pathlib import Path
import os,urllib.parse
out=Path(os.environ.get('SCHOOLOS_TEST_OUTPUT',str(Path(__file__).resolve().parents[1]/'docs/5.1.0/test-output')));out.mkdir(exist_ok=True);base=os.environ.get('SCHOOLOS_EXPERIENCE_BASE','http://127.0.0.1:8090/experience')+'/index.php';assert urllib.parse.urlsplit(base).hostname in ('127.0.0.1','localhost');n=0
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path=os.environ.get('SCHOOLOS_CHROMIUM','/usr/bin/chromium'),headless=True,args=['--no-sandbox']);page=browser.new_page(viewport={'width':1440,'height':1050});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(base+'?login=1');page.screenshot(path=str(out/'login-desktop.png'),full_page=True);assert page.locator('#xpFact').is_visible();original=page.locator('#xpFact').inner_text();page.locator('[data-fact-next]').click();assert page.locator('#xpFact').inner_text()!=original;n+=1
 page.locator('[data-fact-pause]').click();assert page.locator('[data-fact-pause]').get_attribute('aria-pressed')=='true';n+=1
 page.locator('[data-demo-role=schooladmin]').click();assert page.locator('input[name=email]').input_value()=='schooladmin@demo.schoolos.test';assert page.locator('#xpDemoMode').is_checked();n+=1
 page.locator('[data-show-password]').click();assert page.locator('input[name=password]').get_attribute('type')=='text';n+=1
 page.locator('button[name=login]').click();page.wait_for_url('**s=workspace');page.wait_for_timeout(700);assert page.locator('dialog').is_visible();page.locator('[data-next]').click();assert 'setup' in page.locator('#xpTourTitle').inner_text().lower();n+=1
 page.locator('.xp-tour-skip').click();assert not page.locator('dialog').is_visible();n+=1
 page.screenshot(path=str(out/'school-owner-desktop.png'),full_page=True);before=page.locator('[data-xp-clock]').inner_text();page.wait_for_timeout(1100);assert before!=page.locator('[data-xp-clock]').inner_text();n+=1
 page.locator('#themeToggle').click();page.screenshot(path=str(out/'school-owner-dark.png'),full_page=True);n+=1
 page.locator('[data-xp-tour]').first.click();count=0
 while page.locator('dialog').is_visible() and count<10:
  page.locator('[data-next]').click();page.wait_for_timeout(100);count+=1
 assert not page.locator('dialog').is_visible();page.reload();page.wait_for_timeout(600);assert not page.locator('dialog').is_visible();n+=1
 page.goto(base+'?s=welcome');assert page.locator('.xp-journey>li').count()==8 and page.locator('.xp-journey>li>a').count()==8;n+=1;page.screenshot(path=str(out/'onboarding-desktop.png'),full_page=True);page.goto(base+'?s=workspace');page.set_viewport_size({'width':390,'height':844});page.goto(base+'?s=workspace');page.wait_for_timeout(300);assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+2');page.screenshot(path=str(out/'school-owner-mobile.png'),full_page=True);n+=1
 page.goto(base+'?logout=1');page.locator('[data-demo-role=parent]').click();page.locator('button[name=login]').click();page.wait_for_timeout(700);page.locator('.xp-tour-skip').click();assert page.locator('#xpMetrics').inner_text().count('Demo')>=2;n+=1;page.screenshot(path=str(out/'parent-mobile.png'),full_page=True)
 page.goto(base+'?logout=1');page.goto(base+'?register=1');assert page.get_by_role('heading',name='Let your school thrive.').is_visible();page.locator('select[name=plan_id]').select_option('1');assert '25,000' in page.locator('#xpPlanSummary').inner_text();n+=1;page.locator('select[name=plan_id]').select_option('2');page.locator('select[name=cycle]').select_option('annual');assert page.locator('#xpLoginForm button[type=submit]').is_disabled();n+=1;page.locator('select[name=plan_id]').select_option('1');page.locator('select[name=cycle]').select_option('monthly');assert page.locator('#xpLoginForm button[type=submit]').is_enabled();n+=1;assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+2');page.screenshot(path=str(out/'registration-mobile.png'),full_page=True);n+=1
 assert not errors,errors;n+=1;browser.close()
print('Browser interactions:',n,'assertions passed.')
