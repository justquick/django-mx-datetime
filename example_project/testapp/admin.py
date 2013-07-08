from django.contrib import admin

from djmx.admin import mx_overrides, date_format

from .models import TimePeriod, MyModel


class TimePeriodAdmin(admin.ModelAdmin):
    formfield_overrides = mx_overrides
    list_display = ('__unicode__', 'start_date_formatted', 'end_date_formatted')
    list_filter = ('start_date', 'end_date')

    start_date_formatted = date_format('start_date')
    end_date_formatted = date_format('end_date')


class MyModelAdmin(admin.ModelAdmin):
    formfield_overrides = mx_overrides
    list_display = ('name', 'pub_date_formatted')
    list_filter = ('pub_date',)

    pub_date_formatted = date_format('pub_date')
    pub_date_formatted.short_description = 'Publication Date'


admin.site.register(TimePeriod, TimePeriodAdmin)
admin.site.register(MyModel, MyModelAdmin)
