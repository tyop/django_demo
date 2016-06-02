from django.contrib import admin

# Register your models here.


from . import models

class ResourceAdmin(admin.ModelAdmin):
    list_display = ('student_name')


admin.site.register(models.Student)
admin.site.register(models.School)
admin.site.register(models.Classroom)


