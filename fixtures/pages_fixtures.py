from config import Settings
import pytest


@pytest.fixture()
def open_main_page(settings: Settings, open_page):
    open_page(settings.base_url)
