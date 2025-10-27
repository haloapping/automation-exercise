import snoop
import configvar
from faker import Faker
from playwright.sync_api import sync_playwright, expect
from tests.contact import selector
from config import timestamp

@snoop
def test_contact_form(timestamp):
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
        expect(page).to_have_url(f"{configvar.URL}/")

        page.click(selector.CONTACT_US_MENU)
        expect(page.locator(selector.GET_IN_TOUCH_TXT)).to_be_visible()

        fake = Faker(locale="id_ID")
        page.fill(selector.NAME_INPUT_TXT, fake.name())
        page.fill(selector.EMAIL_INPUT_TXT, fake.email())
        page.fill(selector.SUBJECT_INPUT_TXT, "".join(fake.words(3)))
        page.fill(selector.YOUR_MESSAGE_INPUT_TXT, "".join(fake.words(20)))
        page.set_input_files(selector.UPLOAD_FILE_INPUT_FILE, "example.txt")
        page.click(selector.SUBMIT_BTN)

        page.pause()

        page.close()
        context.close()
        browser.close()
