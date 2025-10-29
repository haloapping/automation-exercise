import snoop
import configvar
import os
from playwright.sync_api import sync_playwright, expect
from tests.testcases import selector
from conftest import TIMESTAMP

os.makedirs("logs", exist_ok=True)
snoop.install(out=f"logs/{TIMESTAMP}.log")


@snoop
def test_testcases():
    with sync_playwright() as p:
        # Config browser and context page
        browser = p.chromium.launch(
            headless=configvar.HEADLESS, slow_mo=configvar.SLOW_MO
        )
        context = browser.new_context(
            record_video_dir=f"screen-record/{TIMESTAMP}",
            record_video_size={
                "width": configvar.VIDEO_WIDTH_SIZE,
                "height": configvar.VIDEO_HEIGHT_SIZE,
            },
        )

        # Trace activity
        context.tracing.start(screenshots=True, snapshots=True, sources=True)

        page = context.new_page()
        page.set_viewport_size(
            {
                "width": configvar.VIEW_PORT_WIDTH_SIZE,
                "height": configvar.VIEW_PORT_HEIGHT_SIZE,
            }
        )
        page.goto(configvar.URL)

        expect(page).to_have_url(f"{configvar.URL}/")

        page.click(selector.TEST_CASES_MENU)

        expect(page).to_have_url("https://automationexercise.com/test_cases")

        page.close()
        context.close()
        browser.close()
