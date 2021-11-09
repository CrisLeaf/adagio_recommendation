import scrapy
from data_scraper.items import DataScraperItem
from scrapy.loader import ItemLoader

class AdagioSpider(scrapy.Spider):
	name = "tes"
	start_urls = [
		"https://adagio.cl/collections/alergias",
#		"https://adagio.cl/collections/arabica",
#		"https://adagio.cl/collections/bella-luna"
	]

	def parse(self, response):
		#for product in response.xpath(".//li[@class='grid__item grid__item--collection-template-icedtea small--one-half medium-up--one-quarter']"):
		for product in response.xpath(".//li[contains(@class, 'grid__item grid__item--collection-template')]"):
			try:
				next_page = "https://adagio.cl" + product.xpath(".//div/a/@href").get()
			except:
				next_page = None
			if next_page is not None:
				yield response.follow(url=next_page, callback=self.parse_item)

	def parse_item(self, response):
		loader = ItemLoader(item=DataScraperItem(), selector=response)
		loader.add_xpath("name", ".//div[@class='product-single__meta']/h1/text()")
		loader.add_xpath("price", ".//span[@class='price-item price-item--regular']")
		loader.add_xpath("rating", ".//div[@class='product-single__meta']/div[@class='loox-rating']/@data-rating")
		loader.add_xpath("raters", ".//div[@class='product-single__meta']/div[@class='loox-rating']/@data-raters")
		loader.add_xpath("benefit", ".//div[@class='product-single__meta']/div[contains(@class, 'benefit')]")
		for index, _ in enumerate(response.xpath(".//div[@class='product-single__meta']/div[contains(@class, 'propiedad')]")):
			loader.add_xpath(f"property_{index+1}", f".//div[@class='product-single__meta']/div[contains(@class, 'propiedad')][{index+1}]")
		loader.add_xpath("format", ".//div[@class='selector-wrapper js product-form__item col-8 ml-n3']/select/option")
		loader.add_xpath("description", ".//div[contains(@class, 'adagio--product-description')]/div/p[@style='font-size: 16px;']")
		loader.add_xpath("ingredients", ".//div[contains(@class, 'adagio--product-description')]/div[2]/p[@style='font-size: 16px;']")
		loader.add_xpath("temperature", ".//div[contains(@class, 'adagio--product-description')]/div[4]/div[1]/div/div/div/div[2]/div[2]/div")
		loader.add_xpath("time", ".//div[contains(@class, 'adagio--product-description')]/div[4]/div[2]/div/div/div/div[2]/div[2]/div")
		loader.add_xpath("amount", ".//div[contains(@class, 'adagio--product-description')]/div[4]/div[3]/div/div/div/div[2]/div[2]/div")
		loader.add_xpath("link", "head/link[@rel='canonical']/@href")
		yield loader.load_item()