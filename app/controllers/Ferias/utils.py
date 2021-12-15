from datetime import datetime

def html_date_to_timestamp(html_date, hour):
    return datetime.strptime(html_date + hour, '%Y-%m-%d%H:%M:%S').timestamp()