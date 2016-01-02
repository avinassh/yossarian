from django.core.exceptions import ValidationError


def is_monday(date_object):
    if not date_object.isoweekday() == 1:
        raise ValidationError('Given date is not Monday')
