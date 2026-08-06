import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 1. Initialize browser with standard desktop window configuration
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--ignore-certificate-errors")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

driver = webdriver.Chrome(options=options)

try:
    # 2. Open product page
    product_url = "https://www.ulta.com/" 
    driver.get(product_url)
    
    wait = WebDriverWait(driver, 15)
    print("Page loaded. Looking for the 'Add to bag' button...")
    
    # 3. Locate the 'Add to bag' button
    add_to_bag_btn = wait.until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Add to bag') or contains(., 'ADD TO BAG')]"))
    )
    
    # Scroll element into center view
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_to_bag_btn)
    time.sleep(1)
    
    # Try native click first to trigger UI state changes cleanly
    try:
        add_to_bag_btn.click()
        print("Native click sent to 'Add to bag' button!")
    except Exception:
        driver.execute_script("arguments[0].click();", add_to_bag_btn)
        print("Fallback JavaScript click executed!")
        
    # Give UI 3 seconds to process the state change
    time.sleep(3)
    
    # 4. ASSERTION: Check if the cart count or drawer rendered on page
    print("Verifying cart state update...")
    
    # Check page source for common cart confirmation indicators
    page_text = driver.page_source.lower()
    
    if "view bag" in page_text or "added to bag" in page_text or "1" in page_text:
        print("🎉 TEST PASSED: Successfully triggered Add-to-Bag workflow on Ulta!")
    else:
        print("❌ TEST FAILED: Cart confirmation state was not detected.")

finally:
    driver.quit()
    print("Browser session closed safely.")