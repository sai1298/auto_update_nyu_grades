from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def get_feedback_body(evaluation_shadow, wait, driver):
    """
    From an evaluation_shadow (in the top document), go down to the TinyMCE
    feedback editor iframe, switch into it, and return the <body id="tinymce"> element.
    NOTE: Caller is responsible for switching back to default_content() later.
    """
    # 1) <div slot="second"> inside evaluation_shadow
    secondary_div = wait.until(
        lambda d: evaluation_shadow.find_element(By.CSS_SELECTOR, "div[slot='second']")
    )

    # 2) <d2l-consistent-evaluation-right-panel-feedback> (shadow)
    feedback_host = secondary_div.find_element(
        By.CSS_SELECTOR,
        "d2l-consistent-evaluation-right-panel-feedback"
    )
    feedback_shadow = feedback_host.shadow_root

    # 3) <d2l-htmleditor> (shadow)
    html_editor = feedback_shadow.find_element(
        By.CSS_SELECTOR,
        "d2l-htmleditor"
    )
    html_editor_shadow = html_editor.shadow_root

    # 4) Walk down to the TinyMCE iframe
    flex_container = html_editor_shadow.find_element(
        By.CSS_SELECTOR,
        ".d2l-htmleditor-label-flex-container"
    )
    editor_container = flex_container.find_element(
        By.CSS_SELECTOR,
        ".d2l-htmleditor-container"
    )
    htmleditor_flex = editor_container.find_element(
        By.CSS_SELECTOR,
        ".d2l-htmleditor-flex-container"
    )
    editor = htmleditor_flex.find_element(
        By.CSS_SELECTOR,
        ".d2l-htmleditor-editor-container"
    )
    iframe = editor.find_element(By.CSS_SELECTOR, "iframe.tox-edit-area__iframe")

    # 5) Switch to iframe
    driver.switch_to.frame(iframe)

    # 6) Find TinyMCE <body>
    body = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "body#tinymce"))
    )
    return body


def get_template_primary_secondary(driver, timeout=20):
    """
    Return (grade_input, evaluation_shadow, ps) for the current evaluation page.

    - grade_input: <input> for numeric score (in top document context)
    - evaluation_shadow: shadow root used later to find feedback editor
    - ps: d2l-template-primary-secondary host (for footer lookups, etc.)
    """
    wait = WebDriverWait(driver, timeout)

    # 1) <d2l-consistent-evaluation>
    ce_host = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "d2l-consistent-evaluation"))
    )
    ce_shadow = ce_host.shadow_root

    # 2) <d2l-consistent-evaluation-page> (shadow)
    ce_page = ce_shadow.find_element(By.CSS_SELECTOR, "d2l-consistent-evaluation-page")
    ce_page_shadow = ce_page.shadow_root

    # 3) <d2l-template-primary-secondary> (shadow host)
    ps = ce_page_shadow.find_element(
        By.CSS_SELECTOR,
        "d2l-template-primary-secondary"
    )

    # 4) light DOM child: <div slot="secondary">
    secondary_div = wait.until(
        lambda d: ps.find_element(By.CSS_SELECTOR, "div[slot='secondary']")
    )

    # 5) <consistent-evaluation-right-panel> (shadow)
    right_panel = secondary_div.find_element(
        By.CSS_SELECTOR,
        "consistent-evaluation-right-panel"
    )
    right_panel_shadow = right_panel.shadow_root

    # 6) Inside that: <consistent-evaluation-right-panel-evaluation> (shadow)
    evaluation = right_panel_shadow.find_element(
        By.CSS_SELECTOR,
        "consistent-evaluation-right-panel-evaluation"
    )
    evaluation_shadow = evaluation.shadow_root

    # ---- GRADE INPUT PATH (stay in top-level context, no iframes yet) ----

    # 7) <d2l-consistent-evaluation-right-panel-grade-result> (shadow)
    grade_result = wait.until(
        lambda d: evaluation_shadow.find_element(
            By.CSS_SELECTOR,
            "d2l-consistent-evaluation-right-panel-grade-result"
        )
    )
    grade_result_shadow = grade_result.shadow_root

    # 8) <d2l-labs-grade-result-presentational> (shadow)
    presentational = grade_result_shadow.find_element(
        By.CSS_SELECTOR,
        "d2l-labs-grade-result-presentational"
    )
    presentational_shadow = presentational.shadow_root

    # 9) <d2l-labs-grade-result-numeric-score> (shadow)
    numeric_score = presentational_shadow.find_element(
        By.CSS_SELECTOR,
        "d2l-labs-grade-result-numeric-score"
    )
    numeric_score_shadow = numeric_score.shadow_root

    # 10) <d2l-input-number> (shadow)
    input_number = numeric_score_shadow.find_element(
        By.CSS_SELECTOR,
        "d2l-input-number"
    )
    input_number_shadow = input_number.shadow_root

    # 11) <d2l-input-text> (shadow)
    input_text = input_number_shadow.find_element(
        By.CSS_SELECTOR,
        "d2l-input-text"
    )
    input_text_shadow = input_text.shadow_root

    # 12) Finally: the container + input you want
    input_container = input_text_shadow.find_element(
        By.CSS_SELECTOR,
        "div.d2l-input-container"
    )
    grade_input = input_container.find_element(
        By.CSS_SELECTOR,
        "input.d2l-input"
    )

    # Return evaluation_shadow so we can use it later for feedback
    return grade_input, evaluation_shadow, ps


def get_save_publish_buttons(ps, wait):
    """Return (publish_btn, save_btn) inside the footer."""
    ce_host = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "d2l-consistent-evaluation"))
    )
    ce_shadow = ce_host.shadow_root

    # 2) <d2l-consistent-evaluation-page> (shadow)
    ce_page = ce_shadow.find_element(By.CSS_SELECTOR, "d2l-consistent-evaluation-page")
    ce_page_shadow = ce_page.shadow_root

    # 3) <d2l-template-primary-secondary> (shadow host)
    ps = ce_page_shadow.find_element(
        By.CSS_SELECTOR,
        "d2l-template-primary-secondary"
    )

    footer_div = wait.until(
        lambda d: ps.find_element(By.CSS_SELECTOR, "div[slot='footer']")
    )
    footer_host = footer_div.find_element(By.CSS_SELECTOR, "d2l-consistent-evaluation-footer")
    footer_shadow = footer_host.shadow_root

    # Publish
    publish_host = footer_shadow.find_element(
        By.CSS_SELECTOR, "d2l-button#consistent-evaluation-footer-publish"
    )
    publish_btn = publish_host.shadow_root.find_element(By.CSS_SELECTOR, "button")

    # Save draft
    save_host = footer_shadow.find_element(
        By.CSS_SELECTOR, "d2l-button#consistent-evaluation-footer-save-draft"
    )
    save_btn = save_host.shadow_root.find_element(By.CSS_SELECTOR, "button")

    return publish_btn, save_btn


def save_grades(driver, ps, wait, condition=True):
    """Click Save + Publish if condition=True."""
    if not condition:
        return

    # Ensure we are in the top-level document (NOT inside TinyMCE iframe)
    driver.switch_to.default_content()

    # Re-locate the buttons
    publish_btn, save_btn = get_save_publish_buttons(ps, wait)

    # Wait until the Save button is enabled/clickable
    wait.until(lambda d: save_btn.is_enabled())

    # Click Save Draft
    # driver.execute_script("arguments[0].click();", save_btn)
    
    driver.execute_script("arguments[0].click();", save_btn)
    time.sleep(7)

    return publish_btn, save_btn


# ============================================================
# UPDATE BOTH GRADE + FEEDBACK
def update_details(grade, feedback, driver, timeout=20):
    """
    Fill grade and feedback.
    - grade: number or string (score)
    - feedback: string (overall feedback text)
    """
    wait = WebDriverWait(driver, timeout)

    grade_input, evaluation_shadow, ps = get_template_primary_secondary(
        driver, timeout=timeout
    )

    # 2) Fill grade first (still in default content)
    if grade is not None and len(str(grade)) != 0:
        grade_input.clear()
        grade_input.send_keys(str(grade))

    # 3) Fill feedback (this will switch into the iframe)
    if feedback is None and len(feedback) == 0:
        feedback = ""
    feedback_body = get_feedback_body(evaluation_shadow, wait, driver)
    feedback_body.clear()
    feedback_body.send_keys(feedback)

    # 4) Save (and optionally publish)
    save_grades(driver, ps, wait, condition=True)

    # After we’re done, always go back to top
    driver.switch_to.default_content()

    return True
