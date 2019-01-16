from wtforms import DecimalField, RadioField
from wtforms.widgets.html5 import NumberInput


class BSNumberInput( NumberInput ):
    def __init__( self, step=None, min=None, max=None):
        super( BSNumberInput, self ).__init__( step=step, min=min, max=max )
        self.error_class = 'is-invalid'

    def __call__(self, field, **kwargs):
        if field.errors:
            c = kwargs.pop('class', '') or kwargs.pop('class_', '')
            kwargs['class'] = u'%s %s' % (self.error_class, c)
        return super(BSNumberInput, self).__call__(field, **kwargs)

class BSDecimalField( DecimalField ):
    widget = BSNumberInput()

class BSRadioField( RadioField ):
    pass
