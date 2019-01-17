import namesgenerator
from wtforms import StringField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf import FlaskForm

from fields import BSDecimalField, BSRadioField, BSNumberInput
from fields.validators import NumberRangeExclusive, BiggerOrEqualToField, BiggerThanField, SmallerThanField


class SimulationForm( FlaskForm ):
    class Meta:
        csrf = False

    name = StringField(
        label       = 'Name',
        description = 'Geben Sie Ihrer Simulation einen Namen, um sie später besser wiederzufinden.',
        default     = namesgenerator.get_random_name
    )

    model = BSRadioField(
        label       = 'Modell',
        description = 'Wählen Sie hier das gewünschte Simulationsmodell. \'Kombiniert\' ist das Modell zum Bachelor.',
        choices     = [
            # links: was an mein Code geht; rechts: was auf der Webseite angezeigt wird
            ('combined_models', 'Kombiniert'),
            ('hog', 'Hog'),
            ('ion', 'Ion'),
            ('volume', 'Volume'),
        ],
        default='combined_models'
    )

    start = BSDecimalField(
        label      = 'Start der Simulation',
        default    = 0,
        validators = [ NumberRange( min=0 ), SmallerThanField( 'stop' ) ],
        widget     = BSNumberInput( min=0, step=0.01 )
    )
    stop = BSDecimalField(
        label      = 'Ende der Simulation',
        default    = 80,
        validators = [ NumberRange( min=0 ), BiggerThanField( 'start' ) ],
        widget     = BSNumberInput( min=0, step=0.01 )
    )
    step_size = BSDecimalField(
        label      = 'Schrittgröße',
        default    = 0.1,
        validators = [ NumberRangeExclusive( min=0 ) ],
        widget     = BSNumberInput( min=0.01, step=0.01 )
    )
    glucose_impulse_start = BSDecimalField(
        label      = 'Start des Glucoseimpuls',
        default    = 1,
        validators = [
            NumberRange( min=0 ),
            SmallerThanField( 'glucose_impulse_stop' ),
            BiggerThanField( 'start' ),
            SmallerThanField( 'stop' ),
        ],
        widget     = BSNumberInput( min=0, step=0.01 )
    )
    glucose_impulse_stop = BSDecimalField(
        label      = 'Ende des Glucoseimpuls',
        default    = 13,
        validators = [
            NumberRange( min=0 ),
            BiggerThanField( 'glucose_impulse_start' ),
            BiggerThanField( 'start' ),
            SmallerThanField( 'stop' ),
        ],
        widget     = BSNumberInput( min=0, step=0.01 )
    )

