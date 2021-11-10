import scrapy
from data_scraper.items import DataScraperItem
from scrapy.loader import ItemLoader

class AdagioSpider(scrapy.Spider):
	name = "tes"
	start_urls = [
		"https://adagio.cl/collections/alergias",
		"https://adagio.cl/collections/arabica",
		"https://adagio.cl/collections/bella-luna",
		"https://adagio.cl/collections/chocolates-y-otros",
		"https://adagio.cl/collections/desserts",
		"https://adagio.cl/collections/scary-collection",
		"https://adagio.cl/collections/iced-tea",
		"https://adagio.cl/collections/primavera",
		"https://adagio.cl/collections/resfrio-e-inmunidad",
		"https://adagio.cl/collections/signo-zodiacal",
		"https://adagio.cl/collections/new-in",
		"https://adagio.cl/collections/te-negro",
		"https://adagio.cl/collections/te-verde",
		"https://adagio.cl/collections/te-rojo",
		"https://adagio.cl/collections/te-blanco",
		"https://adagio.cl/collections/te-oolong",
		"https://adagio.cl/collections/te-amarillo",
		"https://adagio.cl/collections/te-matcha",
		"https://adagio.cl/collections/te-chai",
		"https://adagio.cl/collections/hierbas",
		"https://adagio.cl/collections/rooibos",
		"https://adagio.cl/collections/linea-master"
		"https://adagio.cl/collections/travel-mugs",
		"https://adagio.cl/collections/mugs-y-tazas",
		"https://adagio.cl/collections/preparacion",
		"https://adagio.cl/collections/tarros",
		"https://adagio.cl/collections/teteras",
		"https://adagio.cl/collections/accesorios-matcha",
		"https://adagio.cl/collections/new-in",
		"https://adagio.cl/collections/packs-hebras",
		"https://adagio.cl/collections/packs-teabags",
		"https://adagio.cl/collections/packs-accesorios-y-te",
		"https://adagio.cl/collections/chocolates-y-otros",
		"https://adagio.cl/collections/new-in",
		"https://adagio.cl/collections/matcha",
		"https://adagio.cl/collections/sale"
	]

	def parse(self, response):
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
		text = response.xpath(".//div[contains(@class, 'adagio--product-description')]/div/p[@style='font-size: 16px;']")
		try:
			loader.add_value("description_1", text[0].get())
		except:
			loader.add_xpath("description_1", ".//div[contains(@class, 'adagio--product-description')]/div/p[@style='font-size: 16px;']")
		try:			
			loader.add_value("description_2", text[1].get())
		except:
			loader.add_xpath("description_2", ".//div[contains(@class, 'adagio--product-description')]/div[2]/p[@style='font-size: 16px;']")
		loader.add_xpath("temperature", ".//div[contains(@class, 'adagio--product-description')]/div[4]/div[1]/div/div/div/div[2]/div[2]/div")
		loader.add_xpath("time", ".//div[contains(@class, 'adagio--product-description')]/div[4]/div[2]/div/div/div/div[2]/div[2]/div")
		loader.add_xpath("amount", ".//div[contains(@class, 'adagio--product-description')]/div[4]/div[3]/div/div/div/div[2]/div[2]/div")
		loader.add_xpath("link", "head/link[@rel='canonical']/@href")
		yield loader.load_item()