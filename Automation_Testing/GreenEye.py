import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 1. Initialize browser options
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--ignore-certificate-errors")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

# Automatically block browser location prompts
prefs = {
    "profile.default_content_setting_values.geolocation": 2
}
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(options=options)

try:
    # 2. Open Green Eye Associates Homepage
    homepage_url = "https://greeneyeassociates.com/"
    driver.get(homepage_url)
    
    wait = WebDriverWait(driver, 25)
    print("Page loaded. Looking for the 'Request Appointment' card button...")
    
    time.sleep(3)
    
    # 3. Target the specific broken appointment button linking to scheduleyourexam.com
    broken_btn = wait.until(
        EC.presence_of_element_located((
            By.XPATH, 
            "//a[contains(@href, 'scheduleyourexam.com') or (contains(@class, 'x-btn') and contains(., 'Schedule Appointment'))]"
        ))
    )
    
    # Scroll into view
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", broken_btn)
    time.sleep(1)
    
    # Store current window handle before clicking
    original_tab = driver.current_window_handle
    
    # Click the broken appointment button
    print("Clicking the broken 'Schedule Appointment' button...")
    driver.execute_script("arguments[0].click();", broken_btn)
    time.sleep(4)
    
    # 4. Switch to the newly opened browser tab
    all_tabs = driver.window_handles
    for tab in all_tabs:
        if tab != original_tab:
            driver.switch_to.window(tab)
            print("Switched to the newly opened scheduling tab!")
            break
            
    time.sleep(3)
    
    # 5. ASSERTION: Check for error / cancellation indicators
    print("Evaluating page destination for defect indicators...")
    destination_url = driver.current_url
    page_text = driver.page_source.lower()
    
    print(f"Destination URL loaded: {destination_url}")
    
    if "cancelled" in page_text or "error" in page_text or "store cancelled" in page_text or "index.php" in destination_url:
        print("🐛 BUG CONFIRMED (DEFECT LOGGED): Broken scheduling CTA detected!")
        print(f"   Expected: Functional booking wizard | Actual: Target link loaded error state or canceled store.")
        print("🎉 TEST COMPLETED: Defect scenario successfully reproduced and validated!")
    else:
        print("✅ PASS: Scheduling portal rendered without visible error messages.")

finally:
    driver.quit()
    print("Browser session closed safely.")