from django.contrib import admin
from DSIApp.models import Student , log
# Register your models here.
class StudentAdmin(admin.ModelAdmin):
    list_display = ['Name','Age','Mob','Add','Email','Pass','Re_Pass']
admin.site.register(Student,StudentAdmin)

