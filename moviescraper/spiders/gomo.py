# -*- coding: utf-8 -*-
import scrapy
from jsonfinder import jsonfinder
from moviescraper.items import MoviescraperItem
import logging as log

EMAIL_ADDRESS = 'nbnnbnkhadka@gmail.com'
PASSWORD = 'retypeas'


class GomoSpider(scrapy.Spider):
    name = 'gomo'
    allowed_domains = ['gomo.to']
    start_urls = ['http://gomo.to/login']
    alphabet_url = [
        '0-9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
        'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
    ]

    def parse(self, response):
        login_form = response.xpath('//form[@id="login-form"]')
        if login_form:
            log.warn('Login required')
            yield scrapy.FormRequest.from_response(
                response=response,
                formdata={'email': EMAIL_ADDRESS, 'password': PASSWORD},
                callback=self.parse
            )
            return
        else:
            for alphabet in self.alphabet_url:
                for pagination in range(1, 12):
                    current_url = 'http://gomo.to/library/%s?page=%s' % (alphabet, pagination)
                    yield scrapy.Request(current_url, callback=self.parse_library_page)

    def parse_library_page(self, response):
        library_divs = response.xpath('//div[contains(@class, "singleVideo")]')
        for each in library_divs:
            movie_detail_url = each.xpath('a/@href').extract()
            if movie_detail_url:
                yield scrapy.Request(movie_detail_url[0], callback=self.parse_movie_detail_page)

    def parse_movie_detail_page(self, response):
        item = MoviescraperItem()
        movie_name_from_url = response.url.split('gomo.to/movie/')
        item['name'] = response.xpath(
            '//div[contains(@class, "topdescriptiondesc")]/div[1]/h2/text()').extract()[0].strip()
        single_desciprion_details = response.xpath('//div[contains(@class, "single_desciprion_details")]')
        genre_actor = single_desciprion_details[0].xpath('ul/li')
        if genre_actor:
            genre = ';'.join(genre_actor[0].xpath('a/text()').extract())
            item['genre'] = genre
        if len(genre_actor) > 1:
            actor = ';'.join(genre_actor[1].xpath('a/text()').extract())
            item['actors'] = actor
        director_country = single_desciprion_details[1].xpath('ul/li')
        if director_country:
            director = ';'.join(director_country[0].xpath('a/text()').extract())
            item['director'] = director
        if len(director_country) > 1:
            country = ';'.join(director_country[1].xpath('a/text()').extract())
            item['country'] = country

        duration_quality = single_desciprion_details[2].xpath('ul/li')
        if duration_quality:
            duration = ';'.join(duration_quality[0].xpath('span/text()').extract())
            item['duration'] = duration
        if len(duration_quality) > 1:
            quality = ','.join(duration_quality[1].xpath('span/text()').extract())
            item['quality'] = quality

        imdb_rating = ';'.join(single_desciprion_details[3].xpath('ul/li/span/text()').extract())
        item['imdb_rating'] = imdb_rating
        url_css_bkgrd = response.xpath('//div[contains(@class, "right_descrition_play")]/@style').extract()
        if url_css_bkgrd:
            poster_url = str(url_css_bkgrd[0].split('url(')[-1]).replace(');', '')
            item['poster_url'] = poster_url

        trailer = ';'.join(response.xpath('//iframe[contains(@id, "iframe-trailer")]/@src').extract())
        item['trailer'] = trailer

        if movie_name_from_url:
            movie_name = movie_name_from_url[-1]
            watch_url = 'http://gomo.to/watch/movie/%s' % movie_name
            request = scrapy.Request(watch_url, callback=self.parse_movie_video_url)
            request.meta['item'] = item
            yield request

    def parse_movie_video_url(self, response):
        scripts = response.xpath('//script/text()')
        item = response.meta['item']
        for script in scripts:
            _script = script.extract()
            if 'playerInstance.setup' in _script:
                for _, __, obj in jsonfinder(_script, json_only=True):
                    for _obj in obj:
                        movie_url = _obj.get('file')
                        item['movie_url'] = movie_url.replace('\\', '')
        yield item
