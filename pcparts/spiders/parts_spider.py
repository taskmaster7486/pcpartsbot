import scrapy


class PartsSpider(scrapy.Spider):
    name = "parts"
    start_urls = [
        'https://www.pcstudio.in/'
    ]
    category_selectors = [
        'menu-category1',
        'menu-category2',
        'menu-category3'
    ]

    def parse(self, response):

        for selectors in self.category_selectors:
            category_links = response.css('ul#{} li a'.format(selectors))

            yield from response.follow_all(category_links, self.parse_parts)

    def parse_parts(self, response):
        for parts in response.css('li.product'):
            yield {
                'name': parts.css('h2.woocommerce-loop-product__title::text').get(),
                'url': parts.css('a.woocommerce-loop-product__link::attr(href)').get(),
                'price': parts.css('span.woocommerce-Price-amount::text').get(),
                'tag': response.css('h1.archive-title::text').get()
            }
        next_link = response.css('nav.woocommerce-pagination li a.next')
        if next_link:
            yield response.follow(next_link[0], self.parse_parts)
