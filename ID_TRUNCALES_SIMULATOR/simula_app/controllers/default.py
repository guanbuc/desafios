# -*- encoding:utf-8 -*-


from flask import render_template
from flask.views import View
from simula_app import app
from simula_app.apis import API
from simula_app.models.forms import GeneraIdTruncales, ReporteIdTruncales


API.API_CID_RESPONSE().ALTA()
API.API_CID_RESPONSE().BAJA()
API.API_CID_RESPONSE().MODIF()


class API_CID_REQUEST(View):
    def __init__(self, template_name):
        self.Template_name = template_name

    def dispatch_request(self):
        if self .Template_name == 'index':
            formGeneraIdTruncales = GeneraIdTruncales()

            return render_template('GeneralDTruncales.html', form=formGeneraIdTruncales)

        else:
            formReporteIdTruncales = ReporteIdTruncales()

            return render_template('ReporteIDTruncales.html', form=formReporteIdTruncales)


app.add_url_rule('/modificacion', view_func=API_CID_REQUEST.as_view('/modificacion', 'modificacion'), methods=['GET', 'POST'])
app.add_url_rule('/index', view_func=API_CID_REQUEST.as_view('/index', 'index'), methods=['GET', 'POST'])