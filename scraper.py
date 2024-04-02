from lxml.html import HtmlElement


def element(html: HtmlElement, xpath: str) -> HtmlElement | None:
    return html.xpath(f".{xpath}")[0] if html.xpath(xpath) else None

def elements(html: HtmlElement, xpath: str) -> list[HtmlElement | None]:
    return [*html.xpath(f".{xpath}")]

def contains_string(element: HtmlElement, target: str):
    if target in (element.text or ''):
        return True
    for child in element.iterchildren():
        if contains_string(child, target):
            return True
    return False