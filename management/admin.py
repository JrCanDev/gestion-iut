from django.contrib import admin

# Register your models here.
from management.models import Year, Teacher, Promotion, Td, Tp, Subject, Sessions

admin.site.register(Year)
admin.site.register(Teacher)
admin.site.register(Promotion)
admin.site.register(Td)
admin.site.register(Tp)
admin.site.register(Subject)
admin.site.register(Sessions)