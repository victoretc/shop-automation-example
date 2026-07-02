import pytest


class Pages:
    open_main_page = pytest.mark.usefixtures("open_main_page")
