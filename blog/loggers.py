import logging
import datetime


class MyDbLogHandler(logging.Handler): # Inherit from logging.Handler
    def __init__(self):
        # run the regular Handler __init__
        logging.Handler.__init__(self)

    def emit(self, record):
        # instantiate the model
        try:
            #NOTE: need to import this here otherwise it causes a circular reference and doesn't work
            #  i.e. settings imports loggers imports models imports settings...
            from .models import SystemErrorLog
            logEntry = SystemErrorLog(level=record.levelname, message=record.message, timestamp=datetime.datetime.now())
            logEntry.save()
        except:
            pass

        return