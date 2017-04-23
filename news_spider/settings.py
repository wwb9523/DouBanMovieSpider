# -*- coding: utf-8 -*-

# Scrapy settings for news_spider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'news_spider'

SPIDER_MODULES = ['news_spider.spiders']
NEWSPIDER_MODULE = 'news_spider..spiders'
DEFAULT_ITEM_CLASS = 'news_spider.items.NewsSpiderItem'

# DOWNLOADER_MIDDLEWARES = {
#     "news_spider.misc.middlewares.CustomUserAgentMiddleware": 401,
#     "news_spider.misc.middlewares.CustomCookieMiddleware": 701,
#     "news_spider.misc.middlewares.CustomHeadersMiddleware": 551,
# }

# DUPEFILTER_CLASS = "news_spider.misc.bloomfilter.BLOOMDupeFilter"
# DOWNLOADER_MIDDLEWARES = {
#     "news_spider.middleware.UserAgentMiddleware": 401,
#     # "weibo_spider.middleware.ProxyMiddleware": 402,
#     #"news_spider.middleware.CookiesMiddleware": 403,
# }

LOG_ENABLED = True
LOG_FILE = './news_spider/log/spider.log'
LOG_LEVEL = 'INFO'  # 日志级别
LOG_ENCODING = 'utf-8'
LOG_STDOUT = False
LOG_FORMAT = '%(asctime)s [%(name)s:%(module)s:%(funcName)s:%(lineno)s] %(message)s'

ITEM_PIPELINES = {
    'news_spider.pipelines.NewsPipeline': 1,
}
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'news_spider (+http://www.yourdomain.com)'

# Obey robots.txt rules
#ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 6

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 2
DEPTH_PRIORITY = 1
# SCHEDULER_DISK_QUEUE = "scrapy.squeue.PickleFifoDiskQueue"
# SCHEDULER_MEMORY_QUEUE = "scrapy.squeue.FifoMemoryQueue"
WEBSERVICE_ENABLED = False
TELNETCONSOLE_ENABLED = False
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 2
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'news_spider.middlewares.MyCustomSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'news_spider.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'news_spider.pipelines.SomePipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
