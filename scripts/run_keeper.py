import logging
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

from colab_keeper import config
from colab_keeper.driver_manager import get_driver
from colab_keeper.colab_controller import run_notebook, create_and_run_copy

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def job():
    logging.info("Starting Colab keeper job: opening notebook %s", config.NOTEBOOK_URL)
    driver = get_driver(config.CHROME_USER_DATA_DIR, headless=config.HEADLESS, page_load_timeout=config.PAGE_LOAD_TIMEOUT)
    try:
        run_notebook(driver, config.NOTEBOOK_URL, keep_alive_minutes=config.KEEP_ALIVE_MINUTES, page_load_timeout=config.PAGE_LOAD_TIMEOUT)
    except Exception as e:
        logging.exception("Job failed: %s", e)
    finally:
        try:
            driver.quit()
        except Exception:
            pass
    logging.info("Job finished.")


def rotate_job():
    if not config.ENABLE_AUTO_COPY:
        logging.info("Auto copy disabled; skipping rotation job")
        return
    logging.info("Starting rotation job: creating new Colab copy from %s", config.NOTEBOOK_URL)
    driver = get_driver(config.CHROME_USER_DATA_DIR, headless=config.HEADLESS, page_load_timeout=config.PAGE_LOAD_TIMEOUT)
    try:
        create_and_run_copy(driver, config.NOTEBOOK_URL, copy_wait_seconds=config.COPY_NEW_TAB_WAIT, keep_alive_minutes=config.KEEP_ALIVE_MINUTES, page_load_timeout=config.PAGE_LOAD_TIMEOUT)
    except Exception as e:
        logging.exception("Rotation job failed: %s", e)
    finally:
        try:
            driver.quit()
        except Exception:
            pass
    logging.info("Rotation job finished.")


if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_job(job, 'interval', hours=config.INTERVAL_HOURS, next_run_time=datetime.now())
    logging.info("Scheduler started: interval %s hours", config.INTERVAL_HOURS)
    if config.ENABLE_AUTO_COPY:
        # schedule rotation copy job every COPY_INTERVAL_HOURS
        scheduler.add_job(rotate_job, 'interval', hours=config.COPY_INTERVAL_HOURS, next_run_time=datetime.now())
        logging.info("Rotation job scheduled: every %s hours", config.COPY_INTERVAL_HOURS)
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logging.info("Scheduler stopped.")
