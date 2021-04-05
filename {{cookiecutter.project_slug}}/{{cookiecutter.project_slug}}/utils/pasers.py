def extract_links(element, a_xpath):
    links = element.xpath(a_xpath)
    for link in links:
        yield link.xpath("text()").extract_first(), link.xpath("@href").extract_first()