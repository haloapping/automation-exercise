import snoop
import configvar
from playwright.sync_api import sync_playwright, expect
from tests.logout import selector
from config import timestamp


@snoop
def test_logout(timestamp):
    with sync_playwright() as p:
        # Config browser and context page
        browser = p.chromium.launch(headless=configvar.HEADLESS, slow_mo=configvar.SLOW_MO)
        context = browser.new_context(
            record_video_dir=f"screen-record/{timestamp}",
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

        expect(page).to_have_title("Automation Exercise")

        # Sign Up Form
        page.click(selector.SIGNUP_LOGIN_MENU)
        expect(page.locator(selector.LOGIN_ACCOUNT_TXT)).to_be_visible()
        page.fill(selector.EMAIL_INPUT_TXT, "rahel@jamil.com")
        page.fill(selector.PASSWORD_INPUT_TXT, "4HptpQ@XsLcKuZX")
        page.click(selector.LOGIN_BTN)

        expect(page.locator(selector.LOGIN_AS_TXT)).to_be_visible()

        page.click(selector.LOGOUT_MENU)

        expect(page).to_have_url("https://automationexercise.com/login")

        page.close()
        context.close()
        browser.close()
