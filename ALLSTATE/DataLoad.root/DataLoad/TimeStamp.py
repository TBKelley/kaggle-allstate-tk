import datetime as dt

class TimeStamp(object):
    """
    Encapulates TimeStamp processing.
    """
    def __init__(self, name=None):
        self.__startDateTime = dt.datetime.now()
        if (name is None):
            self.__name = ''
        else:
            self.__name = ' ' + name

    @property
    def StartDateTime(self):
        return self.__startDateTime

    @property
    def ElaspseSeconds(self):
        endDateTime = dt.datetime.now()
        startDateTime = self.__startDateTime
        seconds = (endDateTime - startDateTime).total_seconds()
        return seconds

    @property
    def Elaspse(self):
        seconds = self.ElaspseSeconds
        hours = int(seconds//3600)
        seconds -= hours*3600
        minutes = int(seconds//60)
        seconds -= minutes*60

        return '%0*d:%0*d:%f%s' % (2, hours, 2, minutes, seconds, self.__name) # 'HH:mm:ss.sss' + name

