from scrapy import log
from twisted.internet import defer
from twisted.internet.error import TimeoutError, DNSLookupError, ConnectionRefusedError, \
    ConnectionDone, ConnectError, ConnectionLost, TCPTimedOutError
from twisted.web.client import ResponseFailed
from scrapy.core.downloader.handlers.http11 import TunnelError


class RetryMiddleware(object):
    EXCEPTIONS_TO_RETRY = (defer.TimeoutError, TimeoutError, DNSLookupError,
                           ConnectionRefusedError, ConnectionDone, ConnectError,
                           ConnectionLost, TCPTimedOutError, ResponseFailed, IOError, TunnelError)

    def __init__(self):
        self.max_retry_times = 4
        self.retry_http_codes = [500, 502, 503, 504, 400, 404, 408]
        self.priority_adjust = -1

    def process_response(self, request, response, spider):
        if request.meta.get('dont_retry', False):
            return response
        if response.status in self.retry_http_codes:
            return self.retry_request(request, spider) or response
        return response

    def process_exception(self, request, exception, spider):
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY) \
                and not request.meta.get('dont_retry', False):
            return self.retry_request(request, spider)

    def retry_request(self, request, spider):
        retry_times = request.meta.get('retry_times', 0) + 1
        if retry_times < self.max_retry_times:
            msg = 'RetryMiddleware: Retrying %(request)s (failed %(retry_times)d times)' % \
                  {'request': request, 'retry_times': retry_times}
            log.msg(msg, level=log.DEBUG)
            retry_request = request.copy()
            retry_request.meta['retry_times'] = retry_times
            retry_request.dont_filter = True
            retry_request.priority = request.priority + self.priority_adjust
            # retry_request.meta['change_proxy'] = True
            return retry_request
        else:
            msg = 'RetryMiddleware: Gave up retrying %(request)s (failed %(retry_times)d times)' % \
                  {'request': request, 'retry_times': retry_times}
            log.msg(msg, level=log.INFO)