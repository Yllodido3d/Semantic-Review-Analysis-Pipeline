from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
from random import randint
import pandas as pd

# --- 1. SETUP & ANTI-DETECTION ---
options = Options()
# Prevents basic Selenium detection
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
# options.add_argument("--headless") # Use only when debugging is complete

driver = webdriver.Chrome(options=options)
driver.get("https://www.bestbuy.com/site/reviews/samsung-27-odyssey-fhd-ips-240hz-g-sync-gaming-monitor-black/6507926")

# Data structures
reviews_data = []
page_count = 1

# --- 2. MAIN LOOP: COLLECTION & PAGINATION ---
try:
    while True:
        print(f"\n--- Collecting Page {page_count} ---")

        # Scroll Logic (To ensure all 20 reviews load)
        reviews_on_previous_page = -1
        while True:
            # Get currently loaded review blocks on the current page
            review_blocks = driver.find_elements(
                By.CSS_SELECTOR, "div.review-item-content")

            if len(review_blocks) == reviews_on_previous_page:
                print(f"Scroll complete on page {page_count}.")
                break  # All reviews on this page have loaded

            reviews_on_previous_page = len(review_blocks)

            # Scroll down to load the next batch of reviews
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            sleep(1) # Short, human-like delay

        # --- EXTRACTION: Process reviews from the current page ---
        for block in review_blocks:
            try:
                review_text = block.find_element(
                    By.CSS_SELECTOR, "div.ugc-review-body").text
                reviews_data.append(review_text)
            except Exception:
                pass  # Skip blocks without text

        # --- ADVANCED EVASION: FORCED JAVASCRIPT CLICK ---
        try:
            # 1. Locate the Next button using a robust XPATH
            next_button = driver.find_element(
                By.XPATH, "//li[@class='inline page next']/a")

            # 2. Execute a JavaScript click (Bypasses 'disabled' state/overlay)
            driver.execute_script("arguments[0].click();", next_button)

            # 3. Wait for the new page to load (Human-like delay)
            sleep(randint(5, 7))
            page_count += 1

        except Exception:
            # If the Next button is not found, the collection is complete
            print(
                f"'Next Page' button not found on page {page_count}. COLLECTION ENDED.")
            break

except KeyboardInterrupt:
    # Captures Ctrl+C signal for safe shutdown
    print("\n🛑 Manual interruption detected! Saving collected data...")

finally:
    # --- SAFETY BLOCK: Ensures data is saved regardless of exit reason ---
    print("\n💾 Initiating safe data saving...")

    if len(reviews_data) > 0:
        df = pd.DataFrame(reviews_data, columns=['review_text'])
        df.drop_duplicates(inplace=True)
        df.to_csv('raw_reviews.csv', index=False)
        print(
            f"✅ Success! File 'raw_reviews.csv' saved with {len(df)} reviews.")
    else:
        print("⚠️ No data was collected to save.")

    driver.quit()