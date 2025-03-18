from datetime import datetime

date=datetime.now()
def current_date(request):
    return {'date':date}