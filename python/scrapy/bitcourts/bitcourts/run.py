import os
import logging
import logging.handlers
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
#from spiders.BitcourtNewsSpider import BitcourtNewsSpider
#from spiders.BitcourtAuctionSpider import BitcourtAuctionSpider
from spiders.BitcourtResultSpider import BitcourtResultSpider
from datetime import date
from japanera import Japanera, EraDate
import re
import mojimoji

settings = get_project_settings()
process  = CrawlerProcess(settings)

process.crawl(BitcourtResultSpider)
process.start()
