from datetime import datetime

def html_date_to_timestamp(html_date):
    return datetime.strptime(html_date, '%Y-%m-%d').timestamp()