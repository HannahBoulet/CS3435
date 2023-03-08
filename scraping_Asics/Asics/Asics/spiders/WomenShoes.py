import scrapy
import json
#Hannah Boulet
#https://scrapeops.io/python-scrapy-playbook/scrapy-pagination-guide/#3-using-a-websites-sitemap
#https://stackoverflow.com/questions/6682503/click-a-button-in-scrapy
#For this Lab I went through 600 items (had it capped so it doesnt take 1hr and a 1/2 ish to scrap over 1494 Items.
#I then decided to make the files print to the json line files by catergory, I was confused by the Men's Sportstyle Shoes
#but its a category on the ASICS website. It still includes womens shoes so some shoes were showing up in the Men's Sportstyle Shoes JL file.
#Then when I was going through the items I made sure to check whether the item was onsale or not.
#It was onsale I would do the redo the price to the sale price.
#There is 15 different categories from ASICS womens shoes.



class WomenshoesSpider(scrapy.Spider):
    name = "WomenShoes"
    allowed_domains = ["www.asics.com"]
    start_urls = [f"https://www.asics.com/us/en-us/womens-shoes/c/aa20200000/?start={i}&sz=24" for i in range(0, 576, 24)]



    def parse(self, response):
        links = response.css('a.product-tile__link::attr(href)').extract()
        for link in links:
            yield scrapy.Request(url=link, callback=self.parse_item)

    def parse_item(self,response):
        Title = response.xpath('normalize-space(//*[@id="pdpMain"]/div[1]/div[3]/div[1]/text())')
        if Title == '\n        Coming Soon\n    ':
            Title = response.xpath('normalize-space(//*[@id="pdpMain"]/div[1]/div[3]/h1/text())').get()
        else:
            Title = Title.get()

        onsale = response.xpath('//*[@id="pdpMain"]/div[1]/div[2]/div[1]/span[1]/span/text()')
        if onsale:
            onsale = onsale.get()
        else:
            onsale = "Not on sale"

        price = response.xpath('normalize-space(//*[@id="product-content"]/div[1]/div[2]/div[1]/span/text())')
        if onsale == "Sale":
            price = response.css('span.price-sales::text').get().strip()
        else:
            price = price.get()

        width = response.xpath('//*[@id="product-content"]/div[2]/div/ul/li[2]/h2/span/text()').get()

        Deal_link = response.xpath('normalize-space(//*[@id="product-hook-content-small"]/text())')

        if Deal_link:
            Deal_link = Deal_link.get()
        else:
            Deal_link = "No link!"

        image_link = response.css('meta[property = "og:image"]::attr(content)').extract()[0]

        coming_soon = response.xpath('//*[@id="pdpMain"]/div[1]/div[3]/div[1]/text()')
        if coming_soon:
            coming_soon = coming_soon.get()
        else:
            coming_soon = "This is an older shoe!"

        current_color = response.xpath('//*[@id="product-content"]/div[2]/div/ul/li[1]/h2/span/text()').get()
        product_class = response.xpath('//*[@id="product-content"]/div[1]/div[1]/span/text()').get()
        Style = response.css(".product-info-numbers span[itemprop='productID']::attr(data-masterid)").get()
        url = response.css('link[rel="canonical"]::attr(href)').get()

        Shoesdef= {
            'Title': Title,
            'Onsale': onsale,
            'Price': price,
            'Width': width,
            "Product Category": product_class,
            'Current Color': current_color,
            'Deal link': Deal_link,
            'Coming soon?': coming_soon,
            "Image link": image_link,
            'Style': Style,
            'Url': url
        }
        filename = f"{product_class}.jl"
        with open(filename, 'a') as f:
            f.write(json.dumps(Shoesdef) + '\n')
