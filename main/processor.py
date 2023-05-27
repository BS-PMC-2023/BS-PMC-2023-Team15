from datetime import date

from database.models import Reservation, Student


def index(request):
# get all reservations that passed the current date and not returned
    if request.user.id is None:
        return dict()
    res = Reservation.objects.filter(date_to__lt=date.today(), returned=False)
    if request.user.username == "admin":
        return {'overdue': res.count(), "student": "admin"}
    student = Student.objects.get(email=request.user)
    return {'overdue': res.count(), "student": student}
