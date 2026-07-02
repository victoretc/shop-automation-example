import pytest

from playwright.sync_api import Page
from config import Settings
from pytest import TempPathFactory
from playwright.sync_api import BrowserContext
import allure
import structlog
import re
from pathlib import Path


logger = structlog.get_logger(__name__).bind(service="ui")


@pytest.fixture(scope="session")
def settings(load_env) -> Settings:
    return Settings()


@pytest.fixture(scope="function")
def browser_context_args(browser_context_args, tmp_path_factory: TempPathFactory):
    return {
        **browser_context_args,
        "record_video_dir": tmp_path_factory.mktemp("videos/"),
        "record_video_size": {"width": 1920, "height": 1080},
        "viewport": {"width": 1920, "height": 1080},
    }


pytest_plugins = [
    "fixtures.pages_fixtures",
    "fixtures.add_console_to_allure_fixtures",
    "fixtures.add_network_to_allure_fixtures",
    "fixtures.run_only_required_tests",
    "fixtures.attach_fixtures",
    "fixtures.components_fixtures",
]


SCREENSHOT_NAME_PATTERN = re.compile(r"^test-finished-\d+\.png$")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_teardown(item, nextitem):
    yield

    try:
        artifacts_dir = item.funcargs.get("output_path")
        if artifacts_dir:
            artifacts_dir_path = Path(artifacts_dir)
            if artifacts_dir_path.is_dir():
                for file in artifacts_dir_path.iterdir():
                    if file.is_file() and SCREENSHOT_NAME_PATTERN.match(file.name):
                        allure.attach.file(
                            str(file),
                            name=file.name,
                            attachment_type=allure.attachment_type.PNG,
                        )
    except Exception as e:
        print(f"Error taking screenshot: {e}")

    try:
        artifacts_dir = item.funcargs.get("output_path")
        if artifacts_dir:
            artifacts_dir_path = Path(artifacts_dir)

            if artifacts_dir_path.is_dir():
                for file in artifacts_dir_path.iterdir():
                    if file.is_file() and file.suffix == ".webm":
                        allure.attach.file(
                            file,
                            name=file.name,
                            attachment_type=allure.attachment_type.WEBM,
                        )

    except Exception as e:
        print(f"Error attaching video: {e}")


@pytest.fixture
def open_page(page: Page, block_images, block_fonts):
    def _open(url: str):
        page.goto(url)

    return _open


@pytest.fixture(autouse=True)
def block_images(context: BrowserContext):
    context.route("**/*.{png,jpg,jpeg,gif,webp,svg,ico}", lambda route: route.abort())
    yield


@pytest.fixture(autouse=True)
def block_fonts(context: BrowserContext):
    context.route("**/*.{woff,woff2,ttf,otf,eot}", lambda route: route.abort())
    yield
