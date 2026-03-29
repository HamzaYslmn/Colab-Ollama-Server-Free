import logging
import time
import traceback
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

log = logging.getLogger(__name__)


def run_notebook(driver, notebook_url, keep_alive_minutes=290, page_load_timeout=120):
    driver.get(notebook_url)
    wait = WebDriverWait(driver, page_load_timeout)
    try:
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    except Exception:
        pass
    # short pause to let Colab UI initialize
    time.sleep(5)

    # Try the keyboard shortcut Ctrl+F9 (Colab "Run all")
    try:
        ActionChains(driver).key_down(Keys.CONTROL).send_keys(Keys.F9).key_up(Keys.CONTROL).perform()
    except Exception:
        try:
            # Best-effort JS fallback: try to click a run-all element if available
            run_all_js = """
            var runAll = document.querySelector('[command="runtime.run-all"]') || document.querySelector('colab-run-all-button');
            if (runAll) runAll.click();
            """
            driver.execute_script(run_all_js)
        except Exception:
            pass

    # brief wait for runtime to start
    time.sleep(10)

    # Keep the session alive by periodic interactions
    end_time = time.time() + keep_alive_minutes * 60
    while time.time() < end_time:
        try:
            driver.execute_script("window.focus();")
            driver.execute_script("document.body.click();")
            driver.execute_script("window.scrollBy(0,50);window.scrollBy(0,-50);")
        except Exception:
            # ignore intermittent failures and keep trying
            traceback.print_exc()
        time.sleep(60)


def create_and_run_copy(driver, notebook_url, copy_wait_seconds=30, keep_alive_minutes=290, page_load_timeout=120):
    """Open the given notebook URL, attempt to click 'Save a copy in Drive', switch to the new copy and run it.

    This is a best-effort UI automation; Colab UI changes may require selector updates.
    """
    log.info("Opening source notebook to create a Drive copy: %s", notebook_url)
    driver.get(notebook_url)
    wait = WebDriverWait(driver, page_load_timeout)
    try:
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    except Exception:
        pass
    time.sleep(5)

    start_handles = list(driver.window_handles)

    # Try direct JS: find any visible element whose text contains 'Save a copy in Drive' and click it
    try:
        js_click = """
        var phrases = ['Save a copy in Drive', 'Save a copy to Drive', 'Save a copy'];
        for (var i=0;i<phrases.length;i++){
            var s = phrases[i];
            var nodes = Array.from(document.querySelectorAll('*')).filter(function(n){
                try{ return n.innerText && n.innerText.trim().includes(s); }catch(e){ return false; }
            });
            if(nodes.length){ nodes[0].click(); return 'clicked'; }
        }
        return 'not-found';
        """
        res = driver.execute_script(js_click)
        log.debug("direct save-copy click result: %s", res)
    except Exception:
        log.exception("JS direct click failed")

    # If not found, try opening the File menu (best-effort)
    try:
        opened = driver.execute_script("var n=Array.from(document.querySelectorAll('*')).find(x=>x.innerText&&x.innerText.trim()==='File'); if(n){n.click(); return 1;} var m=Array.from(document.querySelectorAll('*')).find(x=>x.innerText&&x.innerText.trim()==='Dosya'); if(m){m.click(); return 1;} return 0;")
        log.debug("tried opening File menu: %s", opened)
        time.sleep(1)
        # try again to click menu item text
        res2 = driver.execute_script("var nodes = Array.from(document.querySelectorAll('*')).filter(function(n){try{return n.innerText&& (n.innerText.includes('Save a copy in Drive')||n.innerText.includes('Save a copy to Drive')||n.innerText.includes('Save a copy'));}catch(e){return false;}}); if(nodes.length){nodes[0].click(); return 'clicked';} return 'not-found';")
        log.debug("menu-item click attempt: %s", res2)
    except Exception:
        log.exception("File menu automation failed")

    # Wait a little for a new tab/window to appear (Colab may open the copy in a new tab)
    new_handle = None
    for i in range(copy_wait_seconds):
        handles = driver.window_handles
        if len(handles) > len(start_handles):
            new_handle = [h for h in handles if h not in start_handles][0]
            log.info("Detected new window/tab for copy: switching")
            driver.switch_to.window(new_handle)
            break
        time.sleep(1)

    # If no new tab, assume current tab was replaced or copy saved in place
    try:
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    except Exception:
        pass

    # Now run the notebook in whichever tab we have
    try:
        log.info("Running the copied notebook: %s", driver.current_url)
        run_notebook(driver, driver.current_url, keep_alive_minutes=keep_alive_minutes, page_load_timeout=page_load_timeout)
    except Exception:
        log.exception("Failed to run copied notebook")
