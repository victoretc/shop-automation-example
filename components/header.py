from playwright.sync_api import Page
from allure import step


class Header:
    def __init__(self, page: Page):
        self.page = page
        self.search_input = page.locator('//input[@type="search"]')
        self.search_button = page.locator('//*[contains(@class, "search-submit")]')
        self.catalog_button = page.locator('//*[contains(@class, "catalog-button")]')

    def search(self, text):
        with step(f"Ввести текст {text} в поле поиска"):
            self.search_input.fill(text)
        with step("Кликнуть на кнопку поиска"):
            self.search_button.click()

    def open_catalog(self):
        with step("Открыть каталог"):
            self.catalog_button.click()
