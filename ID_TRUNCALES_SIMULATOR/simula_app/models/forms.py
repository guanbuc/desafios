# -*- encoding: utf-8 -*-


from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, SubmitField
from wtforms.validators import DataRequired


class GeneraIdTruncales(FlaskForm):
    EQUIPO_A = StringField('EQUIPO_A', validators=[DataRequired()])
    PORTA_A = StringField('PORTA_A', validators=[DataRequired()])
    EQUIPO_Z = StringField('EQUIPO_Z', validators=[DataRequired()])
    PORTA_Z = StringField('PORTA_Z', validators=[DataRequired()])


class ReporteIdTruncales(FlaskForm):
    SI_ID_TRONCAL = StringField('SI_ID_TRONCAL', validators=[DataRequired()])


class ReporteIdTruncalesV2(FlaskForm):
    BAJA = SubmitField('BAJA')
    CAMBIO = SubmitField('CAMBIO')
    DATOS = HiddenField('DATOS')


class GeneraIdTruncalesV2(FlaskForm):
    SI_ID_TRONCAL = HiddenField('SI_ID_TRONCAL')
    SI_ID = HiddenField('SI_ID')