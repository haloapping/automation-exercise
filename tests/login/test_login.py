import snoop
import pendulum
import os
import config
from faker import Faker
from playwright.sync_api import sync_playwright, expect
from tests.login import selector

os.makedirs("logs", exist_ok=True)
now = pendulum.now()
format_name = now.format("YYYY-MM-DD_HH-mm-ss")
snoop.install(out=f"logs/{format_name}.log")


@snoop
def test_login_correct():
    with sync_playwright() as p:
        # Config browser and context page
        browser = p.chromium.launch(headless=config.HEADLESS, slow_mo=config.SLOW_MO)
        context = browser.new_context(
            record_video_dir=f"screen-record/{format_name}",
            record_video_size={
                "width": config.VIDEO_WIDTH_SIZE,
                "height": config.VIDEO_HEIGHT_SIZE,
            },
        )

        # Trace activity
        context.tracing.start(screenshots=True, snapshots=True, sources=True)

        page = context.new_page()
        page.set_viewport_size(
            {
                "width": config.VIEW_PORT_WIDTH_SIZE,
                "height": config.VIEW_PORT_HEIGHT_SIZE,
            }
        )
        page.goto(config.URL)

        expect(page).to_have_title("Automation Exercise")

        # Sign Up Form
        page.click(selector.SIGNUP_LOGIN_MENU)
        expect(page.locator(selector.LOGIN_ACCOUNT_TXT)).to_be_visible()
        page.fill(selector.EMAIL_INPUT_TXT, "rahel@jamil.com")
        page.fill(selector.PASSWORD_INPUT_TXT, "4HptpQ@XsLcKuZX")
        page.click(selector.LOGIN_BTN)

        expect(page.locator(selector.LOGIN_AS_TXT)).to_be_visible()

        page.close()
        context.close()
        browser.close()


@snoop
def test_login_incorrect():
    with sync_playwright() as p:
        # Config browser and context page
        browser = p.chromium.launch(headless=config.HEADLESS, slow_mo=config.SLOW_MO)
        context = browser.new_context(
            record_video_dir=f"screen-record/{format_name}",
            record_video_size={
                "width": config.VIDEO_WIDTH_SIZE,
                "height": config.VIDEO_HEIGHT_SIZE,
            },
        )

        # Trace activity
        context.tracing.start(screenshots=True, snapshots=True, sources=True)

        page = context.new_page()
        page.set_viewport_size(
            {
                "width": config.VIEW_PORT_WIDTH_SIZE,
                "height": config.VIEW_PORT_HEIGHT_SIZE,
            }
        )
        page.goto(config.URL)

        expect(page).to_have_title("Automation Exercise")

        fake = Faker(locale="id_ID")

        # Sign Up Form
        page.click(selector.SIGNUP_LOGIN_MENU)
        expect(page.locator(selector.LOGIN_ACCOUNT_TXT)).to_be_visible()
        page.fill(selector.EMAIL_INPUT_TXT, fake.email())
        page.fill(
            selector.PASSWORD_INPUT_TXT,
            fake.password(
                length=8,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            ),
        )
        page.click(selector.LOGIN_BTN)

        expect(page.locator(selector.EMAIL_OR_PASSWORD_INCORRECT_TXT)).to_be_visible()

        page.close()
        context.close()
        browser.close()
