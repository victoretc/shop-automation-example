import logging
import pytest
import allure
from datetime import datetime
from pathlib import Path
from playwright.sync_api import ConsoleMessage
from helpers import MSK_TIMEZONE
from jinja2 import Environment, FileSystemLoader

# import re
from pytest import FixtureRequest

logger = logging.getLogger(__name__)


@pytest.fixture(scope="function", autouse=True)
def capture_console(request: FixtureRequest, page):
    # marker = request.node.get_closest_marker("console_error_exceptions")
    # patterns = marker.args[0] if marker else []

    console_messages = []

    def on_console(msg: ConsoleMessage):
        console_messages.append(msg)

    logger.info(
        "capture_console: accessing browser.page for test %s", request.node.nodeid
    )
    page.on("console", on_console)

    yield

    attach_console_message_to_allure(console_messages)
    # check_console_errors(console_messages, patterns)


# CONSOLE_ERROR_EXCEPTIONS = []


# def check_console_errors(
#     console_messages: list[ConsoleMessage] | None,
#     additional_console_error_exceptions=None,
# ):
#     if console_messages:
#         errors = [msg for msg in console_messages if msg.type.lower() == "error"]

#         if not errors:
#             return None

#         for error in errors:
#             if not any(
#                 re.search(pattern, error.text, re.IGNORECASE)
#                 for pattern in CONSOLE_ERROR_EXCEPTIONS
#                 + (additional_console_error_exceptions or [])
#             ):
#                 pytest.fail(
#                     f"Обнаружена критическая ошибка в консоли браузера ({error})"
#                 )


def attach_console_message_to_allure(console_messages: list[ConsoleMessage] | None):
    if console_messages:
        console_html_report = create_html_console_report(console_messages)
        allure.attach(
            console_html_report,
            name="console_report",
            attachment_type=allure.attachment_type.HTML,
        )


def create_html_console_report(console_messages: list[ConsoleMessage]):
    templates_path = Path(__file__).parent / "templates"
    env = Environment(loader=FileSystemLoader(templates_path))
    template = env.get_template("console_report.html")

    return template.render(
        logs=console_messages,
        generation_time=datetime.now(MSK_TIMEZONE).strftime("%Y-%m-%d %H:%M:%S"),
    )
