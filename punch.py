# import sys
# from tornado.httpclient import AsyncHTTPClient,HTTPClient
# from tornado.ioloop import IOloop



# for i in range(20):

# 	http_client = AsyncHTTPClient()
# 	response = http_client.fetch("http://www.google.com/",)

# print response.code
# print response.request_time

# import grequests
# import time

# start_time = time.time()
# # Create a 10000 requests
# urls = ['http://www.google.co.il']*10000
# rs = (grequests.head(u) for u in urls)

# # Send them.
# grequests.map(rs)

# print time.time() - start_time # Result was: 9.66666889191

import sys
from tornado.httpclient import AsyncHTTPClient
from tornado.ioloop import IOLoop
import collections
import time



class AsyncClient(object):


    def __init__(self, ioloop,conn):
        self.max = conn
        self.ioloop = ioloop
        self.client = AsyncHTTPClient(max_clients=self.max)
        self.client.configure(None, defaults=dict(connect_timeout=20, request_timeout=float(120)))
        self.backlog = collections.deque()
        self.concurrent_requests = 0


    def __get_callback(self, function):  ##fixing this line
        def wrapped(*args, **kwargs):
            self.concurrent_requests -= 1
            self.try_run_request()
            return function(*args, **kwargs)
        return wrapped

    def try_run_request(self):
        while self.backlog and self.concurrent_requests < self.max:
            request, callback = self.backlog.popleft()
            self.client.fetch(request, callback=callback)
            self.concurrent_requests += 1

    def fetch(self, request, callback=None):
        wrapped = self.__get_callback(callback)

        self.backlog.append((request, wrapped))
        self.try_run_request()



class TornadoRun:
    def __init__(self,req,url,conn):

        self.req = req
        self.url = url
        self.conn = conn
        self.counter = collections.Counter()

    def handle_request(self, response):
        self.counter.update({str(response.code): 1})

        if not self.backlog.backlog and self.backlog.concurrent_requests == 0:
            IOLoop.instance().stop()


    def launch(self):

        self.ioloop = IOLoop.current()
        self.backlog = AsyncClient(self.ioloop,self.conn)

        for i in xrange(self.req):
            self.backlog.fetch(self.url,self.handle_request)

        self.ioloop.start()


def main(input):
    start_time = time.time()

    scraper = TornadoRun(int(input[2]),input[-1],int(input[4]))
    scraper.launch()

    elapsed_time = time.time() - start_time
    print('Process took %f seconds processed %d items.' % (elapsed_time, scraper.req))


if __name__ == "__main__":
    start = sys.argv
    main(start)