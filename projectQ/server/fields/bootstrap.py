from wtforms import FloatField, IntegerField, RadioField, BooleanField, StringField, SelectField
from wtforms.widgets import TextInput
from wtforms.widgets.html5 import NumberInput


class BSNumberInput( NumberInput ):
    def __call__(self, field, **kwargs):
        if field.errors:
            c = kwargs.pop('class', '') or kwargs.pop('class_', '')
            kwargs['class'] = u'%s %s' % ( 'is-invalid', c )
        return super(BSNumberInput, self).__call__(field, **kwargs)

class BSTextInput( TextInput ):
    def __call__(self, field, **kwargs):
        if field.errors:
            c = kwargs.pop('class', '') or kwargs.pop('class_', '')
            kwargs['class'] = u'%s %s' % ( 'is-invalid', c )
        return super(BSTextInput, self).__call__(field, **kwargs)

class BSFloatField( FloatField ):
    widget = BSNumberInput( step='any' )

class BSIntegerField( IntegerField ):
    widget = BSNumberInput()

class BSStringField( StringField ):
    widget = BSTextInput()

class BSRadioField( RadioField ):
    pass

class BSBooleanField( BooleanField ):
    pass

class BSSelectField( SelectField ):
    pass

