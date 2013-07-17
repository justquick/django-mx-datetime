from django.conf import settings

BC = getattr(settings, 'MX_DATETIME_BC', 'BC')
AD = getattr(settings, 'MX_DATETIME_AD', 'AD')
