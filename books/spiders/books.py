# -*- coding: utf-8 -*-
import scrapy


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["angel.co/space-travel"]
    start_urls = [
        'https://angel.co/space-travel',
    ]

    def parse(self, response):
        for book_url in response.css("div.results_holder > div.with_data.dts27.frs86._a._jm > div:first-of-type > div:first-of-type > div:first-of-type > div:first-of-type > div.text > div.name > a ::attr(href)").extract():
            yield scrapy.Request(response.urljoin(book_url), callback=self.parse_book_page)
        next_page = response.css("div.results_holder > div.with_data.dts27.frs86._a._jm > div.next > div:first-of-type > div:first-of-type > div:first-of-type > div.text > div.name > a ::attr(href)").extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_book_page(self, response):
        item = {}
        section1 = response.css("section.component_21156")
        item["name"] = section1.css("h1 ::text").extract_first()
        item['domain'] = response.css("li.websiteLink_b71b4 > a ::attr(href)").extract_first()
        yield item
