from flask_wtf import FlaskForm
from wtforms import PasswordField,StringField,IntegerField,SelectField,SelectField,BooleanField
from wtforms.validators import DataRequired,EqualTo,Length

class FormCambioPassword(FlaskForm):
    txtPasswordActual = PasswordField('txtPasswordActual',validators=[DataRequired("Contraseña Actual es un campo obligatorio")])
    txtPasswordNueva  = PasswordField('txtPasswordNueva',validators=[DataRequired("Contraseña Nueva es un campo obligatorio"),EqualTo('txtPasswordConfirmacion',message="La contraseña nueva y la confirmación no coinciden"),Length(min=8,message="La longitud mínima debe ser de %(min)s carácteres")])
    txtPasswordConfirmacion = PasswordField('txtPasswordConfirmacion')

class FormRegistroPersona(FlaskForm):
    txtPrimerNombre = StringField('txtPrimerNombre',validators=[DataRequired("Primer Nombre es un campo obligatorio"),Length(max=30,message="La longitud máxima del campo Primer Nombre debe ser de %(max)s carácteres")])
    txtSegundoNombre = StringField('txtSegundoNombre',validators=[Length(max=30,message="La longitud máxima del campo Segundo Nombre debe ser de %(max)s carácteres")])
    txtPrimerApellido = StringField('txtPrimerApellido',validators=[DataRequired("Primer Nombre es un campo obligatorio"),Length(max=50,message="La longitud máxima del campo Primer Apellido debe ser de %(max)s carácteres")])
    txtSegundoApellido = StringField('txtSegundoApellido',validators=[Length(max=30,message="La longitud máxima del campo Segundo Apellido debe ser de %(max)s carácteres")])
    txtNroCedula = IntegerField('txtNroCedula',validators=[DataRequired("Nro. de Cédula es un campo obligatorio")])
    txtFechaNacimiento = StringField('txtFechaNacimiento')
