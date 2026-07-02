from marks import Pages
from components.catalog import Catalog
from components.header import Header
from config import Settings
from playwright.sync_api import expect
from allure import step


@Pages.open_main_page
def test_search(catalog: Catalog, header: Header, page, settings: Settings):
    header.open_catalog()
    catalog.open_category("Автоаксессуары")
    with step("Проверить, что открылась страница catalogue/avtoaksessuary/"):
        expect(page).to_have_url(settings.base_url + "catalogue/avtoaksessuary/")
