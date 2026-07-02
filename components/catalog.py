from playwright.sync_api import Page
from allure import step


class Catalog:
    def __init__(self, page: Page):
        self.page = page

    def open_category(self, category_name):
        with step(f"Открыть категорию {category_name}"):
            self.page.locator(
                f'[class*="catalog-categories-card"][data-category-id="{category_name}"]'
            ).click()
