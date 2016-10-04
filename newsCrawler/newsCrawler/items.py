from scrapy import Item, Field
from scrapy.loader.processors import TakeFirst


class NewsItem(Item):
    url = Field(
        output_processor=TakeFirst()
    )
    title = Field(
        output_processor=TakeFirst()
    )
    type = Field(
        output_processor=TakeFirst()
    )
