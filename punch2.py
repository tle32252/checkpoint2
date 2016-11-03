# import sys
# from tornado.httpclient import AsyncHTTPClient
# from tornado.httpclient import HTTPRequest
# from tornado.ioloop import IOLoop
# import collections


# gn = {'P2Tag: ':"u5680913_u5781147","Connection: ": "keep-alive"}
# completed_request = collections.Counter()
# checkls = []

# if __name__ == '__main__':
#     strat=time.time()
#     requestN = int(sys.argv[2])
#     concurrent = sys.argv[4]
#     url = sys.argv[-1]

 
# http_client = AsyncHTTPClient(None, max_clients=concurrent)
# request = HTTPRequest(url,method="GET",headers=gn,request_timeout=float(60))
# for i in xrange(requestN):
#     http_client.fetch(request, handle_request)
#     checkls.append("a")
# IOLoop.instance().start()  

# elapsed = time.time() - start
# print elapsed 
    
# def handle_request(response):
#     global completed_request
#     global checkls
#     checkls.pop()
#     if len(checkls) == 0:
#         IOLoop.instance().stop()
#     completed_request.update({str(response.code):1})


# print "Completed requests: " + str(completed_request["200"])
# print "Failed requests: " + str(requestN - completed_request["200"])
# print "Total Request = " +str(requestN)
# print "eieieieei"
