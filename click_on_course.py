from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from lab_grades import *



def click_first_go_to_evaluation(driver, timeout=20):
    wait = WebDriverWait(driver, timeout)

    # ---------- STRATEGY 1: Click the <a> with title "Go to Evaluation for ..." ----------
    # This avoids shadow DOM completely and is often enough.
    try:
        link = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "(//a[contains(@title,'Go to Evaluation')])[1]")
            )
        )
        link.click()
        return
    except TimeoutException:
        pass
    except Exception:
        pass

    # ---------- STRATEGY 2: d2l-button-subtle with text="Go to Evaluation" (host attr) ----------
    # Uses the custom element attribute, then enters its shadow root.
    try:
        host = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "d2l-button-subtle[text='Go to Evaluation']")
            )
        )
        shadow = host.shadow_root
        inner_btn = shadow.find_element(By.CSS_SELECTOR, "button")
        inner_btn.click()
        return
    except TimeoutException:
        pass
    except Exception:
        pass

    # ---------- STRATEGY 3: Specific ID of that button-subtle host (z_be in your HTML) ----------
    # If ID changes in other rows, this is only for the row you showed.
    try:
        host = wait.until(
            EC.presence_of_element_located((By.ID, "z_be"))
        )
        shadow = host.shadow_root
        inner_btn = shadow.find_element(By.CSS_SELECTOR, "button")
        inner_btn.click()
        return
    except TimeoutException:
        pass
    except Exception:
        pass

    # ---------- STRATEGY 4: Iterate over ALL d2l-button-subtle and match visible text ----------
    # More generic: find all, open shadow roots, look for "Go to Evaluation"
    try:
        hosts = wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "d2l-button-subtle")
            )
        )
        for h in hosts:
            try:
                sroot = h.shadow_root
                btn = sroot.find_element(By.CSS_SELECTOR, "button")
                txt = btn.text.strip()
                # e.g. "Go to Evaluation" or contains it
                if "Go to Evaluation" in txt:
                    btn.click()
                    return
            except Exception:
                continue
    except TimeoutException:
        pass
    except Exception:
        pass

    # ---------- STRATEGY 5: Use JavaScript to click the first matching element ----------
    # 5a. Try the <a> with title containing "Go to Evaluation"
    try:
        js = """
        const link = document.querySelector("a[title*='Go to Evaluation']");
        if (link) { link.click(); return true; }
        return false;
        """
        if driver.execute_script(js):
            return
    except Exception:
        pass

    # 5b. Try the d2l-button-subtle[text='Go to Evaluation'] via JS + shadow DOM
    try:
        js = """
        const host = document.querySelector("d2l-button-subtle[text='Go to Evaluation']");
        if (host && host.shadowRoot) {
            const btn = host.shadowRoot.querySelector("button");
            if (btn) { btn.click(); return true; }
        }
        return false;
        """
        if driver.execute_script(js):
            return
    except Exception:
        pass

    # If we got here, every strategy failed
    raise Exception("Could not click 'Go to Evaluation' using any strategy.")



def brightspace_search(driver, text, timeout=20):
    wait = WebDriverWait(driver, timeout)
    try:
        search_host = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "d2l-input-search.d2l-search-simple-wc-input")
            )
        )
    except TimeoutException:
        raise Exception("Could not find <d2l-input-search> host")

    # 2) Enter its shadow root
    try:
        shadow1 = search_host.shadow_root
    except Exception:
        raise Exception("Selenium shadow_root not available. Make sure you're on Selenium 4+.")
    
    # 3) Inside, find d2l-input-text
    try:
        d2l_input_text = shadow1.find_element(By.CSS_SELECTOR, "d2l-input-text")
        shadow2 = d2l_input_text.shadow_root
    except Exception:
        raise Exception("Failed to access d2l-input-text inside shadow DOM")

    # 4) Inside that, find the real <input>
    try:
        search_box = shadow2.find_element(
            By.CSS_SELECTOR,
            "input.d2l-input"  # placeholder='Search For…' is optional
        )
    except Exception:
        # Fallback: more generic
        try:
            search_box = shadow2.find_element(By.CSS_SELECTOR, "input[type='search']")
        except Exception:
            raise Exception("Could not locate the inner <input> in Brightspace search")

    # 5) Type into it
    search_box.click()
    search_box.clear()
    search_box.send_keys(text)
    search_box.send_keys(Keys.ENTER)
    
    click_first_go_to_evaluation(driver, timeout=20)
    time.sleep(5)
   