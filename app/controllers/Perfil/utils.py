from . import db, datetime, timedelta, time


def converter_str_int(dt):
        hr = datetime.strptime(dt,'%H:%M:%S')

        return int(timedelta(hours=hr.hour,minutes=hr.minute,seconds=hr.second).total_seconds())