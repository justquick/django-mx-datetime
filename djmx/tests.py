from datetime import date
from mx.DateTime import Date, today

import django
from django.test import TestCase
from django.db import models
from django import forms
from django.core.serializers import serialize, deserialize
from django.core.exceptions import ValidationError
try:
    from json import loads
except ImportError:
    from django.utils.simplejson import loads

from .fields import DateField
from .admin import date_format
from .forms import DateField as DateFormField
from .widgets import AdminDateWidget


class Model(models.Model):
    date = DateField(unique=True)
    today = DateField(auto_now=True, blank=True, null=True)

    def __unicode__(self):
        return self.date.date


class Form(forms.ModelForm):
    date = DateFormField(widget=AdminDateWidget())

    class Meta:
        model = Model


class DateTest(TestCase):
    dates = (
        Date(2001, 8, 3),
        Date(2001, 9, 3),
        Date(-2001, 8, 3),
        date(1888, 1, 27),
        '1.1.4004 BCE'
    )
    count = len(dates)

    def setUp(self):
        self.today = int(today(12).jdn)
        for d in self.dates:
            Model.objects.create(date=d)

    def _assertQuerysetEqual(self, qs, values):
        """
        Reimplements assertQuerysetEqual for older versions of Django
        """
        try:
            return self.assertQuerysetEqual(qs, values, str, False)
        except (AttributeError, TypeError):
            for obj in qs:
                self.assert_(str(obj) in values)

    def test_created(self):
        self.assertEqual(Model.objects.count(), self.count)

    def test_today(self):
        self.assertEqual(list(Model.objects.values_list('today', flat=True)),
                         [self.today] * self.count)

    def test_filter(self):
        self._assertQuerysetEqual(Model.objects.filter(date='2001-9-3'), ['2001-09-03'])

    def test_in_lookup(self):
        self.assertEqual(Model.objects.filter(date__in=self.dates).count(), self.count)

    def test_gt_lookup(self):
        self._assertQuerysetEqual(Model.objects.filter(date__gt='1.1.4004 BC'),
                                  ['2001-08-03', '2001-09-03', '-2001-08-03', '1888-01-27'])

    def test_gte_lookup(self):
        self._assertQuerysetEqual(Model.objects.filter(date__gte='1.1.4004 BC'),
                                  ['2001-08-03', '2001-09-03', '-2001-08-03', '1888-01-27', '-4003-01-01'])

    def test_lt_lookup(self):
        self._assertQuerysetEqual(Model.objects.filter(date__lt='2001-08-03'),
                                  ['-2001-08-03', '1888-01-27', '-4003-01-01'])

    def test_lte_lookup(self):
        self._assertQuerysetEqual(Model.objects.filter(date__lte='2001-08-03'),
                                  ['2001-08-03', '-2001-08-03', '1888-01-27', '-4003-01-01'])

    def test_invalid_lookup(self):
        if django.VERSION[:2] != (1, 1):
            self.assertRaises(ValueError, Model.objects.filter, date__year=2011)
            self.assertRaises(ValueError, Model.objects.filter, date__month=8)
            self.assertRaises(ValueError, Model.objects.filter, date__day=3)
            self.assertRaises(ValueError, Model.objects.filter, date__week_day=5)

    def test_ordering(self):
        self.assertEqual([str(m) for m in Model.objects.order_by('date')],
                         ['-4003-01-01', '-2001-08-03', '1888-01-27', '2001-08-03', '2001-09-03'])
        self.assertEqual([str(m) for m in Model.objects.order_by('-date')],
                         ['2001-09-03', '2001-08-03', '1888-01-27', '-2001-08-03', '-4003-01-01'])

    def test_serialize(self):
        data = loads(serialize('json', Model.objects.filter(date='1.1.4004 BCE')))
        self.assertEqual(data[0]['fields']['date'], u'258995')

    def test_deserialize(self):
        data = '[{"pk": 99, "model": "djmx.model", "fields": {"date": "25800"}}]'
        obj = deserialize('json', data).next().object
        self.assertEqual(obj.pk, 99)
        self.assertEqual(obj.date.year, -4642)
        self.assertEqual(obj.date.month, 7)
        self.assertEqual(obj.date.day, 15)
        self.assertEqual(obj.date.hour, 12)

    def test_form(self):
        form = Form({'date': 'January 1 2000'})
        self.assertTrue(form.is_valid())
        obj = form.save()
        self.assertEqual(obj.today.jdn, self.today)
        self.assertEqual(unicode(obj), '2000-01-01')

    def test_date_format(self):
        attr = 'some_date_attr'
        method = date_format('some_date_attr')
        self.assertEqual(method.admin_order_field, attr)
        self.assertEqual(method.short_description, 'Some Date Attr')

        class MockModel(object):
            some_date_attr = self.dates[0]

        self.assertEqual(method(None, MockModel()), '2001-08-03')

    def test_garbage(self):
        self.assertRaises(ValidationError, Model.objects.create, date='adsfasdfsdf')
