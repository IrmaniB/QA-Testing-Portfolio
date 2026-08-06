import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 1. Initialize browser with anti-bot and notification settings
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--ignore-certificate-errors")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

# Block native Chrome geolocation prompts automatically
prefs = {
    "profile.default_content_setting_values.geolocation": 2
}
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(options=options)

try:
    # 2. Open direct product page
    product_url = "https://www.vikkiprints.com/products/pretty-things-inside-for-you-personalised-small-business-stickers-copy"
    driver.get(product_url)
    
    wait = WebDriverWait(driver, 20)
    print("Page loaded. Checking for Klaviyo promotional popup...")
    
    # Wait 4 seconds for the Klaviyo modal to trigger visually
    time.sleep(4)
    
    # 3. Dismiss Klaviyo promo popup using the EXACT inspected attributes!
    try:
        close_popup_btn = wait.until(
            EC.presence_of_element_located((
                By.XPATH, 
                "//button[@aria-label='Close dialog' or contains(@class, 'klaviyo-close-form')]"
            ))
        )
        driver.execute_script("arguments[0].click();", close_popup_btn)
        print("🎉 Successfully clicked the Klaviyo popup close button!")
    except Exception as e:
        print(f"No popup encountered or already cleared: {e}")

    time.sleep(2)

    # 4. Locate the custom text input area using its ID
    print("Locating the custom text area ('ymq-attrib-1')...")
    custom_text_area = wait.until(
        EC.presence_of_element_located((By.XPATH, "//textarea[@id='ymq-attrib-1' or contains(@name, 'ymq')]"))
    )
    
    # Scroll into view
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", custom_text_area)
    time.sleep(1)
    
    # 5. Prepare the 200-character test payload
    test_payload = "QA_TEST_" * 25  # Generates a 200-character test string
    print(f"Injecting test payload ({len(test_payload)} characters) into input field...")
    
    custom_text_area.clear()
    custom_text_area.send_keys(test_payload)
    
    # Extract the value actually accepted by the input DOM element
    actual_value = custom_text_area.get_attribute("value")
    print(f"Input field currently contains {len(actual_value)} characters.")
    
    # 6. Click 'Add to Cart'
    print("Clicking 'Add to cart' button...")
    add_to_cart_btn = wait.until(
        EC.presence_of_element_located((By.XPATH, "//button[@name='add' or contains(@id, 'ProductSubmitButton')]"))
    )
    
    driver.execute_script("arguments[0].click();", add_to_cart_btn)
    time.sleep(3)
    
    # 7. ASSERTION: Boundary Value Analysis Verification
    print("Evaluating Boundary Value Analysis (BVA) results...")
    
    if len(actual_value) > 30:
        print(f"🐛 BUG CONFIRMED (DEFECT LOGGED): Input field failed character boundary truncation!")
        print(f"   Expected: Max 30 chars or truncation | Actual: Accepted full {len(actual_value)} chars.")
        print("🎉 TEST COMPLETED: Defect scenario successfully reproduced and validated!")
    else:
        print(f"✅ PASS: Input field properly truncated string to {len(actual_value)} chars.")

finally:
    driver.quit()
    print("Browser session closed safely.")