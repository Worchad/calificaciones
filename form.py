from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms.validators import DataRequired,EqualTo,Length

class FormCambioPassword(FlaskForm):
    txtPasswordActual = PasswordField('txtPasswordActual',validators=[DataRequired("Contraseña Actual es un campo obligatorio")])
    txtPasswordNueva  = PasswordField('txtPasswordNueva',validators=[DataRequired("Contraseña Nueva es un campo obligatorio"),EqualTo('txtPasswordConfirmacion',message="La contraseña nueva y la confirmación no coinciden"),Length(min=8,message="La longitud mínima debe ser de %(min)s carácteres")])
    txtPasswordConfirmacion = PasswordField('txtPasswordConfirmacion') 