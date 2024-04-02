from lxml.html import HtmlElement


def element(html: HtmlElement, xpath: str) -> HtmlElement | None:
    return html.xpath(xpath)[0] if html.xpath(xpath) else None

def elements(html: HtmlElement, xpath: str) -> list[HtmlElement | None]:
    return [*html.xpath(xpath)]