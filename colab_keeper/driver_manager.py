import undetected_chromedriver as uc

def get_driver(user_data_dir=None, headless=False, page_load_timeout=120):
    options = uc.ChromeOptions()
    if user_data_dir:
        options.add_argument(f"--user-data-dir={user_data_dir}")
    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1400,900")
    driver = uc.Chrome(options=options)
    driver.set_page_load_timeout(page_load_timeout)
    return driver
