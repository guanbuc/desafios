# -*- encoding:utf-8 -*-


from simula_app import app
from simula_app.models.forms import ReporteIdTruncalesV2, GeneraIdTruncales, GeneraIdTruncalesV2
from simula_app.db.tables import DB
from flask import make_response, request, jsonify, render_template, redirect, url_for, Response
from flask.views import MethodView


class API_CID_RESPONSE:
    def __init__(self):
        self.index = 'API_alta'
        self.baja = 'API_baja'
        self.modification = 'API_modif'


    def ALTA(self):
        url = '/alta'
        pType = 'string'
        alta = API_RESPONSE.as_view(self.index, self.index)
        app.add_url_rule(url, defaults={'EQUIPO_A': None, 'PORT_A': None, 'EQUIPO_Z': None, 'PORT_Z': None, 'SI_ID': None}, view_func=alta, methods=['GET', 'POST', 'PUT', 'DELETE'])
        app.add_url_rule(url, view_func=alta, methods=['GET', 'POST', 'PUT', 'DELETE'])
        app.add_url_rule(f'{url}?csrf_token=<{pType}:csrf_toke>&EQUIPO_A=<{pType}:PORT_A>&EQUIPO_Z=<{pType}:EQUIPO_Z>&PORT_Z=<{pType}:PORT_Z>&SI_ID=<{pType}:SI_ID>', view_func=alta, methods=['GET', 'POST', 'PUT', 'DELETE'])

    def BAJA(self):
        url='/baja'
        pType='string'
        baja = API_RESPONSE.as_view(self.baja, self.baja)
        app.add_url_rule(url, defaults={'SI_ID_TRONCAL': None, 'SI_ID': None}, view_func=baja, methods=['GET', 'POST', 'PUT', 'DELETE'])
        app.add_url_rule(url, view_func=baja, methods=['GET', 'POST', 'PUT', 'DELETE'])
        app.add_url_rule(f'{url}?csrf_token=<{pType}:csrf_toke>&SI_ID_TRONCAL=<{pType}:SI_ID_TRONCAL>&SI_ID=<{pType}:SI_ID>', view_func=baja, methods=['GET', 'POST', 'PUT', 'DELETE'])

    def MODIF(self):
        url='/baja'
        pType='string'
        modif = API_RESPONSE.as_view(self.modification, self.modification)
        app.add_url_rule(url, defaults={'SI_ID_TRONCAL': None}, view_func=modif, methods=['GET', 'POST', 'PUT', 'DELETE'])
        app.add_url_rule(url, view_func=modif, methods=['GET', 'POST', 'PUT', 'DELETE'])
        app.add_url_rule(f'{url}?csrf_token=<{pType}:csrf_toke>&SI_ID_TRONCAL=<{pType}:SI_ID_TRONCAL>>', view_func=modif, methods=['GET', 'POST', 'PUT', 'DELETE'])


class API_RESPONSE(MethodView):
    def __init__(self, template_name):
        self.Main = {}
        self.template_name = template_name
        self.form = ReporteIdTruncalesV2()
        self.DB = DB()

    def get(self):
        if self.template_name == 'API_alta':
            self.Main = {}
            self.Main['EQUIPO_A'] = ((request.values['EQUIPO_A']).split('|')[0]).strip()
            self.Main['PORT_A'] = request.values['PORT_A']
            self.Main['TECNO_A'] = ((request.values['TECNO_A']).split('|')[1]).strip()
            self.Main['EQUIPO_Z'] = ((request.values['EQUIPO_Z']).split('|')[0]).strip()
            self.Main['PORT_Z'] = request.values['PORT_Z']
            self.Main['TECNO_Z'] = ((request.values['TECNO_Z']).split('|')[1]).strip()
            self.Main['SI_ID'] = request.values['SI_ID']
            self.Main['TYPE'] = self.template_name

            if self.DB.dqlStmt(self.Main):
                self.Main['TYPE'] = 'API_modif'

            self.DB.dmlStmt(self.Main)

            return make_response(jsonify(self.Main), 200)

        elif self.template_name == 'API_baja':
            self.Main = {}
            self.Main['SI_ID'] = request.values['SI_ID']
            self.Main['SI_ID_TRONCAL'] = request.values['SI_ID_TRONCAL']
            self.Main['TYPE'] = self.template_name

            self.Main = self.DB.dmlStmt(self.Main)

            return make_response(jsonify(self.Main), 200)

        elif self.template_name == 'API_modif':
            self.Main = {}
            self.Main['SI_ID_TRONCAL'] = request.values['SI_ID_TRONCAL']
            self.Main['TYPE'] = self.template_name
            self.form.DATOS.data = self.DB.dqlStmt(self.Main)

            return render_template('ReporteIDTruncalesV2.html', form=self.form, content=self.form.DATOS.data)

    def post(self):
        for Key in request.values:
            if Key == 'CAMBIO':
                self.Main = eval(request.values['DATOS'])
                self.Main['TYPE'] = 'API_modif'
                self.form = GeneraIdTruncales()
                self.form.EQUIPO_A.data = f"{self.Main['SI_EQUIPO_A']}|{self.Main['SI_TECNOLOGIA_A']}"
                self.form.PORT_A.data = f"{self.Main['SI_PORT_NAME_A']}"
                self.form.EQUIPO_Z.data = f"{self.Main['SI_EQUIPO_Z']}|{self.Main['SI_TECNOLOGIA_Z']}"
                self.form.PORT_Z.data = f"{self.Main['SI_PORT_NAME_Z']}"
                self.form.SI_ID.data = f"{self.Main['SI_ID']}"

                return render_template('GeneralDTruncales.html', form=self.form)

            elif Key == 'BAJA':
                self.Main['SI_ID'] = eval(request.values['DATOS'])['SI_ID']
                self.Main['SI_ID_TRONCAL'] = eval(request.values['DATOS'])['SI_ID_TRONCAL']
                self.form = GeneraIdTruncalesV2()
                self.form.SI_ID.data = self.Main['SI_ID']
                self.form.SI_ID_TRONCAL.data = self.Main['SI_ID_TRONCAL']

                return render_template('GeneralDTruncalesV2.html', form=self.form, content=self.Main)