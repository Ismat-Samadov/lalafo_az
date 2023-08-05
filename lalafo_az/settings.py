BOT_NAME = "lalafo_az"

SPIDER_MODULES = ["lalafo_az.spiders"]
NEWSPIDER_MODULE = "lalafo_az.spiders"

ROBOTSTXT_OBEY = True

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
