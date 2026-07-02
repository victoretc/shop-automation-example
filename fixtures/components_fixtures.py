from playwright.sync_api import Page
from components.header import Header
from components.catalog import Catalog
import pytest


@pytest.fixture
def header(page: Page) -> Header:
    return Header(page)


@pytest.fixture
def catalog(page: Page) -> Catalog:
    return Catalog(page)
