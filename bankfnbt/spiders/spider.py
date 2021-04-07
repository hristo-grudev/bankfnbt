import json

import requests
import scrapy

from scrapy.loader import ItemLoader

from ..items import BankfnbtItem
from itemloaders.processors import TakeFirst


class BankfnbtSpider(scrapy.Spider):
	name = 'bankfnbt'
	start_urls = ['https://www.bankfnbt.com/wp-json/wp/v2/posts?per_page=420&offset=0']

	def parse(self, response):
		data = json.loads(response.text)
		for post in data:
			url = post['link']
			date = post['date']
			yield response.follow(url, self.parse_post, cb_kwargs={'date': date})

	def parse_post(self, response, date):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="zone content"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()

		item = ItemLoader(item=BankfnbtItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
