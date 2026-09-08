import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 1. Initialize browser with flags
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--allow-running-insecure-content")
driver = webdriver.Chrome(options=options)

try:
    # 2. Open the live storefront URL
    base_url = "https://kikizcosmeticz.shop/"
    driver.get(base_url)

    wait = WebDriverWait(driver, 15)

    # 3. Click hamburger menu using aria-label
    print("Locating the mobile menu hamburger button...")
    hamburger_menu = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//summary[@aria-label='Menu']"))
    )
    hamburger_menu.click()
    print("Hamburger menu clicked! Drawer opened.")

    time.sleep(2)

    # 4. Locate the lip gloss link
    print("Scanning the open drawer for the Hydrating Lip Gloss link...")
    lip_gloss_link = wait.until(
        EC.presence_of_element_located((By.ID, "HeaderDrawer-hydrating-lip-gloss"))
    )

    # Use JavaScript click to bypass overlay interception! 🎯
    driver.execute_script("arguments[0].click();", lip_gloss_link)
    print(
        "Menu link clicked successfully via JavaScript! Waiting for page redirection..."
    )

    time.sleep(3)

    # 5. Grab the actual URL and run the assertion
    actual_url = driver.current_url
    expected_path = "/collections/hydrating-lip-gloss"

    print(f"Landed on URL: {actual_url}")

    if expected_path in actual_url:
        print(
            "🎉 TEST PASSED: Successfully navigated to the Hydrating Lip Gloss collection page!"
        )
    else:
        print("❌ TEST FAILED: Reached an unexpected layout or URL address.")

finally:
    driver.quit()
    print("Browser session closed safely.")
