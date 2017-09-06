# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# 1.	Genre
# 2.	Director
# 3.	Actors
# 4.	Duration
# 5.	IMDB Rating
# 6.	Country
# 7.	Keywords
# 8.	Poster (Example: http://prntscr.com/g7uksm)
# 9.	Movie Trailer
# 10.	Movie Quality (TS, Cam, HD,etc)
# 11.	Link to stream movie


class MoviescraperItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    genre = scrapy.Field()
    actors = scrapy.Field()
    director = scrapy.Field()
    country = scrapy.Field()
    duration = scrapy.Field()
    imdb_rating = scrapy.Field()
    keywords = scrapy.Field()
    trailer = scrapy.Field()
    poster_url = scrapy.Field()
    movie_url = scrapy.Field()
    quality = scrapy.Field()
    pass
