# encoding=utf-8
import random
#from cookies import cookies
from user_agents import agents
# from proxies import proxy


class UserAgentMiddleware(object):
    """ 换User-Agent """

    def process_request(self, request, spider):
        agent = random.choice(agents)
        request.headers["User-Agent"] = agent


# class CookiesMiddleware(object):
#     """ 换Cookie """
#
#     def process_request(self, request, spider):
#         cookie = random.choice(cookies)
#         request.cookies = cookie

# class ProxyMiddleware(object):
#     """ 换IP """
#
#     def process_request(self, request, spider):
#         IP = random.choice(proxy)
#         request.meta['proxy'] = "http://%s" % IP
