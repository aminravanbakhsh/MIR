import click
from scrapy.crawler import CrawlerProcess

from crawler.crawler.spiders.papers_spider import PapersSpider
from hits.hits import HITS
from page_rank.page_rank import PageRank
from recommender.collaborative_filtering import find_most_similar_papers
from recommender.content_based import find_related_papers
from recommender.utils import create_user_vectors


def start_crawler():
    process = CrawlerProcess(settings={
        'LOG_ENABLED': True,
        'LOG_LEVEL': 'ERROR',
        'SPLASH_URL': 'http://localhost:8050/',
        'DUPEFILTER_CLASS': 'scrapy_splash.SplashAwareDupeFilter',
        'HTTPCACHE_STORAGE': 'scrapy_splash.SplashAwareFSCacheStorage',
        'DOWNLOADER_MIDDLEWARES': {
            'crawler.crawler.middlewares.CrawlerDownloaderMiddleware': 543,
            'scrapy_splash.SplashCookiesMiddleware': 723,
            'scrapy_splash.SplashMiddleware': 725,
            'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
        },
        'SPIDER_MIDDLEWARES': {
            'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
            'crawler.crawler.middlewares.CrawlerSpiderMiddleware': 543,
        },
        'ROBOTSTXT_OBEY': False,
    })
    process.crawl(PapersSpider)
    process.start()


def sort_by_page_rank(alpha):
    pr = PageRank('CrawledPapers.json', alpha)
    pr.calculate_page_rank()


def sort_by_hits(n):
    hits = HITS('CrawledPapers.json', n)
    top_authors = hits.calculate_hits()
    for i, (author, hit) in enumerate(top_authors):
        click.echo(f'{i + 1}. {author}')


def print_paper_ids(paper_ids):
    click.echo('Related paper ids:')
    for i, paper_id in enumerate(paper_ids):
        print(f'{i + 1}. {paper_id}')


def echo_related_paper_ids(user_id):
    with open('data.csv', 'r') as f:
        rows = [line.strip().split(',') for line in f.readlines()]

    paper_ids = find_related_papers(rows[0], create_user_vectors(rows[1:])[user_id - 1])
    print_paper_ids(paper_ids)


def echo_similar_papers_by_collaborative(n, user_id):
    print_paper_ids(find_most_similar_papers(user_id, n))


@click.group()
def main():
    pass


@main.command()
def crawl():
    start_crawler()


@main.command()
@click.argument('alpha', type=float)
def page_rank(alpha):
    sort_by_page_rank(alpha)


@main.command()
@click.argument('n', type=int)
def hits(n):
    sort_by_hits(n)


@main.command()
@click.argument('user-id', type=int)
def content_based(user_id):
    echo_related_paper_ids(user_id)


@main.command()
@click.argument('n', type=int)
@click.argument('user-id', type=int)
def collaborative(n, user_id):
    echo_similar_papers_by_collaborative(n, user_id)


main()
