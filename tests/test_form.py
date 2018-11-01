# set encoding=utf-8
from django.forms import fields
from django.test import TestCase
from decimal import Decimal
import datetime
import mock
from django.utils import timezone
from constance.admin import ConstanceForm
from constance import config

class TestForm(TestCase):
    def test_form_field_types(self):

        f = ConstanceForm({})

        self.assertIsInstance(f.fields['INT_VALUE'], fields.IntegerField)
        self.assertIsInstance(f.fields['LONG_VALUE'], fields.IntegerField)
        self.assertIsInstance(f.fields['BOOL_VALUE'], fields.BooleanField)
        self.assertIsInstance(f.fields['STRING_VALUE'], fields.CharField)
        self.assertIsInstance(f.fields['UNICODE_VALUE'], fields.CharField)
        self.assertIsInstance(f.fields['DECIMAL_VALUE'], fields.DecimalField)
        self.assertIsInstance(f.fields['DATETIME_VALUE'],
                              fields.SplitDateTimeField)
        self.assertIsInstance(f.fields['TIMEDELTA_VALUE'],
                              fields.DurationField)
        self.assertIsInstance(f.fields['FLOAT_VALUE'], fields.FloatField)
        self.assertIsInstance(f.fields['DATE_VALUE'], fields.DateField)
        self.assertIsInstance(f.fields['TIME_VALUE'], fields.TimeField)

        # from CONSTANCE_ADDITIONAL_FIELDS
        self.assertIsInstance(f.fields['CHOICE_VALUE'], fields.ChoiceField)
        self.assertIsInstance(f.fields['EMAIL_VALUE'], fields.EmailField)

    @mock.patch("constance.admin.ConstanceForm.clean_version", lambda x: 'test')
    def test_form_save(self):
        old_conf = config.DATETIME_VALUE
        now = timezone.now()
        initial = {}
        data = {
            'FLOAT_VALUE': 3.1415926536,
            'BOOL_VALUE': True,
            'EMAIL_VALUE': 'test@example.com',
            'INT_VALUE': 1,
            'CHOICE_VALUE': 'yes',
            'TIME_VALUE': datetime.time(23, 59, 59),
            'DATE_VALUE': datetime.date(2010, 12, 24),
            'TIMEDELTA_VALUE': datetime.timedelta(days=1, hours=2, minutes=3),
            'LINEBREAK_VALUE': 'Spam spam',
            'DECIMAL_VALUE': Decimal('0.1'),
            'STRING_VALUE': 'Hello world',
            'UNICODE_VALUE': u'Rivière-Bonjour რუსთაველი',
            'LONG_VALUE': 123456,
            'DATETIME_VALUE_0': now.date(),
            'DATETIME_VALUE_1': now.time(),
            'version': 'test'
        }
        f = ConstanceForm(initial, data=data)
        self.assertTrue(f.is_valid(), msg=f.errors.as_data())
        f.save()
        self.assertEqual(config.DATETIME_VALUE, f.cleaned_data["DATETIME_VALUE"])
        config.DATETIME_VALUE = old_conf

