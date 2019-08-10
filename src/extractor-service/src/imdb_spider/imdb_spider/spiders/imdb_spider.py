import scrapy

from typing import List


def to_query_str(q):
    return '+'.join(q.split(' '))


def generate_imdb_queries(tv_series: List[str]):
    imdb_search_url = 'https://www.imdb.com/find?ref_=nv_sr_fn&q={}&s=all'
    return [imdb_search_url.format(to_query_str(t)) for t in tv_series]


class IMDbSpider(scrapy.Spider):
    name = "imdb"

    def start_requests(self):

        tv_series = ['Friends', 'Game of Thrones', 'Breaking Bad']
        start_urls = generate_imdb_queries(tv_series)
        for i, url in enumerate(start_urls):
            yield scrapy.Request(url=url,
                                 callback=self.parse,
                                 meta={'query_name': tv_series[i]})

    def parse(self, response):
        title_selector = '//*[@id="main"]/div/div[2]/table/tr[1]/td[2]/a'
        title_elem = response.xpath(title_selector).get()
        title = response.xpath(''.join([title_selector, '/text()'])).get()
        assert title.lower() == response.meta['query_name'].lower()

