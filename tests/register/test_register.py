import snoop
import pendulum
import os
import config
import random
from faker import Faker
from playwright.sync_api import sync_playwright, expect
from tests.register import selector

os.makedirs("logs", exist_ok=True)
now = pendulum.now()
format_name = now.format("YYYY-MM-DD_HH-mm-ss")
snoop.install(out=f"logs/{format_name}.log")


@snoop
def test_register():
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
        expect(page.locator(selector.NEWUSER_SIGNUP_TXT)).to_be_visible()
        page.fill(selector.NAME_INPUT_TXT, fake.user_name())
        page.fill(selector.EMAIL_INPUT_TXT, fake.email())
        page.click(selector.SIGNUP_BTN)

        # Account Information
        expect(page.locator(selector.ACCOUNT_INFO_HEADER_TXT)).to_be_visible()
        title = random.choice(["Mr", "Mrs"])
        if title == "Mr":
            page.click(selector.TITLE_MR_RB)
        else:
            page.click(selector.TITLE_MRS_RB)

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

        days = [str(i) for i in range(1, 32)]
        day = random.choice(days)
        page.select_option(selector.DATE_OF_BIRTH_DAY_DDL, day)

        months = [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ]
        month = random.choice(months)
        page.select_option(selector.DATE_OF_BIRTH_MONTH_DDL, month)

        years = [str(i) for i in range(1900, 2022)]
        year = random.choice(years)
        page.select_option(selector.DATE_OF_BIRTH_YEAR_DDL, year)

        page.click(selector.NEWSLETTER_CB)
        page.click(selector.SPECIAL_OFFERS_CB)

        # Address Information Form
        expect(page.locator(selector.ADDRESS_INFO_HEADER_TXT)).to_be_visible()
        page.fill(selector.FIRST_NAME_INPUT_TXT, fake.first_name())
        page.fill(selector.LAST_NAME_INPUT_TXT, fake.last_name())
        page.fill(selector.COMPANY_INPUT_TXT, fake.company())
        page.fill(selector.ADDRESS1_INPUT_TXT, fake.address())
        page.fill(selector.ADDRESS2_INPUT_TXT, fake.address())
        countries = [
            "India",
            "United States",
            "Canada",
            "Australia",
            "Israel",
            "New Zealand",
            "Singapore",
        ]
        page.select_option(selector.COUNTRY_DDL, random.choice(countries))
        page.fill(selector.STATE_INPUT_TXT, fake.state())
        page.fill(selector.CITY_INPUT_TXT, fake.city_name())
        page.fill(selector.ZIPCODE_INPUT_TXT, fake.postcode())
        page.fill(selector.MOBILE_NUMBER_INPUT_TXT, fake.phone_number())
        page.click(selector.CREATE_ACCOUNT_BTN)

        expect(page.locator(selector.ACCOUNT_CREATED_TXT)).to_be_visible()

        page.click(selector.CONTINUE_BTN)

        expect(page.locator(selector.LOGIN_AS_TXT)).to_be_visible()

        page.click(selector.DELETE_ACCOUNT_MENU)

        expect(page.locator(selector.ACCOUNT_DELETED_TXT)).to_be_visible()

        page.close()
        context.close()
        browser.close()
