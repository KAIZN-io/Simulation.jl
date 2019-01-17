import namesgenerator
from wtforms.validators import InputRequired, NumberRange, Length
from flask_wtf import FlaskForm

from fields import BSDecimalField, BSIntegerField, BSRadioField, BSBooleanField, BSNumberInput, BSStringField, BSSelectField
from fields.validators import NumberRangeExclusive, BiggerOrEqualToField, BiggerThanField, SmallerThanField, IntegerList, Conditional


class SimulationForm(FlaskForm):
    class Meta:
        csrf = False

    name = BSStringField(
        label       = 'Name',
        description='Geben Sie Ihrer Simulation einen Namen, um sie später besser wiederzufinden.',
        default     = namesgenerator.get_random_name,
        validators = [
            InputRequired(),
            Length( min=3, max=30 ),
        ],
    )

    model = BSRadioField(
        label='Modell',
        description = 'Wählen Sie hier das gewünschte Simulationsmodell. \'Kombiniert\' ist das Modell zum Bachelor.',
        choices=[
            # links: was an mein Code geht; rechts: was auf der Webseite angezeigt wird
            ('combined_models', 'Kombiniert'),
            ('hog', 'Hog'),
            ('ion', 'Ion'),
            ('volume', 'Volume'),
        ],
        default     = 'combined_models'
    )

    start = BSIntegerField(
        label      = 'Start der Simulation',
        default    = 0,
        validators = [
            InputRequired(),
            NumberRange( min=0 ),
            SmallerThanField( 'stop' )
        ],
        widget     = BSNumberInput( min=0 )
    )
    stop = BSIntegerField(
        label      = 'Ende der Simulation',
        default    = 80,
        validators = [
            InputRequired(),
            NumberRange( min=0 ),
            BiggerThanField( 'start' )
        ],
        widget     = BSNumberInput( min=0, step=0.01 )
    )
    step_size = BSDecimalField(
        label      = 'Schrittgröße',
        default    = 0.1,
        validators = [
            InputRequired(),
            NumberRangeExclusive( min=0 )
        ],
        widget     = BSNumberInput( min=0.01, step=0.01 )
    )

    glucose_impulse_start = BSDecimalField(
        label      = 'Start des Glucoseimpuls',
        default    = 1,
        validators = [
            InputRequired(),
            NumberRange( min=0 ),
            SmallerThanField( 'glucose_impulse_stop' ),
            BiggerThanField( 'start' ),
            SmallerThanField( 'stop' ),
        ],
        widget=BSNumberInput(min=0, step=0.01)
    )
    glucose_impulse_stop = BSDecimalField(
        label      = 'Ende des Glucoseimpuls',
        default    = 13,
        validators = [
            InputRequired(),
            NumberRange( min=0 ),
            BiggerThanField( 'glucose_impulse_start' ),
            BiggerThanField( 'start' ),
            SmallerThanField( 'stop' ),
        ],
        widget=BSNumberInput(min=0, step=0.01)
    )

    nacl_impulse_start = BSDecimalField(
        label      = 'Start des NaCl-Impuls',
        default    = 30,
        validators = [
            Conditional(
                fieldname='model',
                value='hog',
                validators = [
                    InputRequired(),
                    NumberRange( min=0 ),
                    BiggerThanField( 'start' ),
                    SmallerThanField( 'stop' ),
                ],
            ),
        ],
        widget     = BSNumberInput( min=0, step=0.01 )
    )
    nacl_impulse_stop = BSDecimalField(
        label      = 'Ende des NaCl-Impuls',
        default    = 10,
        validators = [
            Conditional(
                fieldname='model',
                value='hog',
                validators = [
                    InputRequired(),
                    NumberRange( min=0 ),
                    BiggerThanField( 'start' ),
                    SmallerThanField( 'stop' ),
                ],
            ),
        ],
        widget     = BSNumberInput( min=0, step=0.01 )
    )
    hog_nacl_impulse = BSDecimalField(
        label      = 'NaCl Impuls',
        default    = 200,
        validators = [
            Conditional(
                fieldname='model',
                value='hog',
                validators = [
                    InputRequired(),
                    NumberRange( min=0 ),
                ],
            ),
        ],
        widget     = BSNumberInput( min=0, step=0.01 )
    )
    hog_signal_type = BSSelectField(
        label='Signaltyp',
        choices=[
            # links: was an mein Code geht; rechts: was auf der Webseite angezeigt wird
            ('1', 'one steady impulse'),
            ('2', 'single pulse of NaCl'),
            ('3', 'square pulses of NaCl'),
            ('4', 'up-staircase change of NaCl'),
        ],
        default     = 1
    )

    kcl_active = BSBooleanField(
        label = 'KCl',
        default = True,
    )
    kcl_amount = BSIntegerField(
        label = 'Menge',
        default = 100,
        validators = [
            Conditional(
                fieldname='kcl_active',
                value=True,
                validators = [
                    InputRequired(),
                    NumberRangeExclusive( min=0 ),
                ],
            ),
        ],
    )
    kcl_timing = BSStringField(
        label = 'Impulse',
        default = '30, 60, 100',
        validators = [
            Conditional(
                fieldname='kcl_active',
                value=True,
                validators = [
                    InputRequired(),
                    IntegerList(),
                ],
            ),
        ],
    )

    nacl_active = BSBooleanField(
        label = 'NaCl',
        default = False,
    )
    nacl_amount = BSIntegerField(
        label = 'Menge',
        default = 800,
        validators = [
            Conditional(
                fieldname='nacl_active',
                value=True,
                validators = [
                    InputRequired(),
                    NumberRangeExclusive( min=0 ),
                ],
            ),
        ],
    )
    nacl_timing = BSStringField(
        label = 'Impulse',
        default = '30',
        validators = [
            Conditional(
                fieldname='nacl_active',
                value=True,
                validators = [
                    InputRequired(),
                    IntegerList(),
                ],
            ),
        ],
    )

    sorbitol_active = BSBooleanField(
        label = 'Sorbitol',
        default = False,
    )
    sorbitol_amount = BSIntegerField(
        label = 'Menge',
        default = 1600,
        validators = [
            Conditional(
                fieldname='sorbitol_active',
                value=True,
                validators = [
                    InputRequired(),
                    NumberRangeExclusive( min=0 ),
                ],
            ),
        ],
    )
    sorbitol_timing = BSStringField(
        label = 'Impulse',
        default = '30',
        validators = [
            Conditional(
                fieldname='sorbitol_active',
                value=True,
                validators = [
                    InputRequired(),
                    IntegerList(),
                ],
            ),
        ],
    )
