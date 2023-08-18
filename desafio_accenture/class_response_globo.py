# -*- encoding: utf-8 -*-
from flask import make_response, jsonify
from flask.views import MethodView
from sqlalchemy import create_engine
import pandas as pd


dtf = pd.DataFrame( {} )

class RESPONSE(MethodView):

    returnError = {'code':'404', 'message':'no data found!'}

    def get(self, **kwargs):
        SQL = 'select signal, program_code, available_time, weekday, average_audience as predicted_audience from average where 1 = 1 '
        programa = 'programa'
        dt_ini = 'dt_ini'
        dt_fim = 'dt_fim'
        engine = create_engine( 'sqlite:///:memory:' )
        dtf.to_sql('average', engine, index=False)

        try:
            SQL = f"{SQL}and program_code = '{kwargs[programa]}'" if programa in kwargs \
                else ((f"{SQL}and datetime(date) >= datetime('{kwargs[dt_ini]}') and datetime(date) <= datetime('{kwargs[dt_fim]}')")
                      if dt_ini in kwargs and dt_fim in kwargs else f"{SQL}and datetime(date) = datetime('{kwargs[dt_ini if dt_ini in kwargs else dt_fim]}')")

            results = pd.read_sql_query(SQL, engine)

            return make_response(results.to_json(orient='index'), 200)

        except KeyError as a:
            if a.args[0] in [programa, dt_ini, dt_fim]:
                results = pd.read_sql_query(SQL, engine)

                return make_response(results.to_json(orient='index'), 200)

            return make_response((jsonify(self.returnError)), 200)

    def post(self):
        return 'post'

    def delete(self):
        return 'delete'

    def put(self):
        return 'put'