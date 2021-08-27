import json
import os

import scrapy
from scrapy.http import Response as ScrapyResponse
from scrapy_splash import SplashRequest

from .splash_scripts import click_on_topics_show_more
from ..constants import PAPER_BASE_URL


class PapersSpider(scrapy.Spider):
    name = 'papers'

    def __init__(self):
        super(PapersSpider, self).__init__()
        self.crawled_ids = {}
        self.papers = []

    def get_splash_request(self, url):
        return SplashRequest(url=url, callback=self.parse, endpoint='execute', args={
            'wait': 4,
            'lua_source': click_on_topics_show_more,
        })

    def start_requests(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(current_dir, 'start_urls.txt'), 'r') as f:
            urls = [url.strip() for url in f.readlines()]
        for url in urls:
            yield self.get_splash_request(url)

    @staticmethod
    def _extract_authors(response: ScrapyResponse):
        authors = response.xpath(
            '//div[@class="name-section"]//div[@class="author-item au-target"]'
            '/a[contains(@class, "au-target") and '
            'contains(@class, "author") and'
            'contains(@class, "link")]/text()'
        ).getall()
        for i in range(len(authors)):
            try:
                if authors[i].index('and ') == 0:
                    authors[i] = authors[i][4]
            except ValueError:
                pass

        return authors

    def extract_paper_data(self, response: ScrapyResponse):
        titles_section_strings = response.xpath('//h1[@class="name"]/text()').getall()
        if len(titles_section_strings) < 3:
            return None
        title = titles_section_strings[2].strip()

        related_topics = [r.lower for r in response.xpath(
            '//div[@class="topics"]//div[contains(@class, "text") and contains(@class, "au-target")]/text()'
        ).getall()]

        citation_count_str = response.xpath(
            '//div['
            'contains(@class, "ma-statistics-item") and '
            'contains(@class, "au-target") and '
            'contains(@aria-label, "Citations")'
            ']//div[@class="count"]/text()'
        ).get()
        citation_count = citation_count_str.strip() if citation_count_str else 0

        reference_count_str = response.xpath(
            '//div['
            'contains(@class, "ma-statistics-item") and '
            'contains(@class, "au-target") and '
            'contains(@aria-label, "References")'
            ']//div[@class="count"]/text()'
        ).get()
        reference_count = reference_count_str.strip() if reference_count_str else 0

        reference_links = response.xpath(
            '//div[@class="results"]//a[contains(@class, "title") and contains(@class, "au-target")]/@href'
        ).getall()
        references = [link.split('/')[1] for link in reference_links]

        return {
            'id': response.url.split('/')[-1],
            'title': title,
            'abstract': response.xpath('//div[@class="name-section"]/p/text()').get(),
            'date': response.xpath('//span[@class="year"]/text()').get(),
            'authors': self._extract_authors(response),
            'related_topics': related_topics,
            'citation_count': citation_count,
            'reference_count': reference_count,
            'references': references,
        }

    def parse(self, response: ScrapyResponse, **kwargs):
        paper_data = self.extract_paper_data(response)
        if paper_data is None:
            return
        self.papers.append(paper_data)
        self.crawled_ids[paper_data['id']] = True

        print(len(self.papers))
        if len(self.papers) >= 2000:
            with open('CrawledPapers.json', 'w') as f:
                json.dump(self.papers, f)
            exit()

        for reference_id in paper_data['references'][:10]:
            if reference_id not in self.crawled_ids:
                yield self.get_splash_request(f'{PAPER_BASE_URL}{reference_id}')
