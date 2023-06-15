from django.contrib import admin
from .models import Student, BookDetail, BookingOrder, BusinessSettings, MyUser
# Register your models here.


admin.site.register(Student)
admin.site.register(BookingOrder)
admin.site.register(BookDetail)
admin.site.register(BusinessSettings)
admin.site.register(MyUser)
