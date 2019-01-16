from wtforms.validators import ValidationError


class NumberRangeExclusive(object):
    """
    Validates that a number is of a minimum and/or maximum value, inclusive.
    This will work with any comparable number type, such as floats and
    decimals, not just integers.
    :param min:
        The minimum required value of the number. If not provided, minimum
        value will not be checked.
    :param max:
        The maximum value of the number. If not provided, maximum value
        will not be checked.
    :param message:
        Error message to raise in case of a validation error. Can be
        interpolated using `%(min)s` and `%(max)s` if desired. Useful defaults
        are provided depending on the existence of min and max.
    """

    def __init__(self, min=None, max=None, message=None):
        self.min = min
        self.max = max
        self.message = message

    def __call__(self, form, field):
        data = field.data
        if (
            data is None
            or (self.min is not None and data <= self.min)
            or (self.max is not None and data >= self.max)
        ):
            message = self.message
            if message is None:
                # we use %(min)s interpolation to support floats, None, and
                # Decimals without throwing a formatting exception.
                if self.max is None:
                    message = field.gettext("Number must be bigger than %(min)s.")
                elif self.min is None:
                    message = field.gettext("Number must be smaller than %(max)s.")
                else:
                    message = field.gettext(
                        "Number must be between %(min)s and %(max)s."
                    )

            raise ValidationError(message % dict(min=self.min, max=self.max))

class CompareToField(object):
    def __init__(self, fieldname, comparator, message=None):
        self.fieldname = fieldname
        self.comparator = comparator
        self.message = message

    def __call__(self, form, field):

        try:
            other = form[self.fieldname]
        except KeyError:
            raise ValidationError(
                field.gettext("Invalid field name '%s'.") % self.fieldname
            )

        if self.comparator not in [ '<', '<=', '>', '>=', '==' ]:
            raise ValidationError( "Invalid comparator '%s' speified." % self.comparator )
        elif (
            ( self.comparator == '<'  and not field.data <  other.data ) or
            ( self.comparator == '<=' and not field.data <= other.data ) or
            ( self.comparator == '>'  and not field.data >  other.data ) or
            ( self.comparator == '>=' and not field.data >= other.data ) or
            ( self.comparator == '==' and not field.data == other.data )
        ):
            message = self.message
            if message is None:
                message = "Must fulfill '%s' %s '%s'."%( field.label.text, self.comparator, other.label.text )
            raise ValidationError( message )

class SmallerThanField( CompareToField ):
    def __init__(self, fieldname, message=None):
        super( SmallerThanField, self ).__init__( fieldname, '<', message )

class SmallerOrEqualToField( CompareToField ):
    def __init__(self, fieldname, message=None):
        super( SmallerOrEqualToField, self ).__init__( fieldname, '<=', message )

class BiggerThanField( CompareToField ):
    def __init__(self, fieldname, message=None):
        super( BiggerThanField, self ).__init__( fieldname, '>', message )

class BiggerOrEqualToField( CompareToField ):
    def __init__(self, fieldname, message=None):
        super( BiggerOrEqualToField, self ).__init__( fieldname, '>=', message )

class EqualToField( CompareToField ):
    def __init__(self, fieldname, message=None):
        super( EqualToField, self ).__init__( fieldname, '==', message )

