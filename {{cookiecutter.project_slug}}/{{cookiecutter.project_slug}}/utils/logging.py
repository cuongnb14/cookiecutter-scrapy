from scrapy import logformatter
import logging

DROPPEDMSG = u"Dropped: %(exception)s"


class CustomLogFormatter(logformatter.LogFormatter):
    def dropped(self, item, exception, response, spider):
        return {
            'level': logging.DEBUG,
            'msg': DROPPEDMSG,
            'args': {
                'exception': exception,
                'item': item,
            }
        }
