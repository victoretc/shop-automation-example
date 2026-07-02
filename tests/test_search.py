from marks import Pages
from components.header import Header


@Pages.open_main_page
def test_search(header: Header):
    header.search("test")
