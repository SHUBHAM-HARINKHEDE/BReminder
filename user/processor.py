from user.models import Birthday
import datetime
def birthays_this_month(request):
    today = datetime.date.today()
    return {'birthays_this_month': Birthday.objects.filter(dob__month=today.month,user=request.user)}