from django.db import models

from djmx.fields import DateField


class TimePeriod(models.Model):
    start_date = DateField()
    end_date = DateField(blank=True, null=True)

    class Meta:
        verbose_name = 'Time Period'
        verbose_name_plural = 'Time Periods'
        ordering = ('start_date', )

    def __unicode__(self):
        if self.end_date:
            return u'%s - %s' % (self.start_date.date, self.end_date.date)
        return self.start_date.date


class MyModel(models.Model):
    name = models.CharField(max_length=255)
    pub_date = DateField()

    class Meta:
        ordering = ('-pub_date', )

    def __unicode__(self):
        return u'%s: (published on %s)' % (self.name, self.pub_date.date)
