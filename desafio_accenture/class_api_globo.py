# -*- encoding: utf-8 -*-
from app import app
import class_response_globo as RESPONSE


class API:

    def __init__(self, endpoint='RESPONSE'):
        self.__endpoint = endpoint

    def execAPI(self):
        url = '/api/average_audience'
        pType = 'string'
        viewAPI = RESPONSE.RESPONSE.as_view( self.__endpoint )
        app.add_url_rule( url, defaults={'dt_ini': None, 'dt_fim': None, 'programa': None}, view_func=viewAPI,
                          methods=['GET', 'POST', 'PUT', 'DELETE'] )

        app.add_url_rule( url, view_func=viewAPI, methods=['GET', 'POST', 'PUT', 'DELETE'] )

        app.add_url_rule( f'{url}/data_inicial=<{pType}:dt_ini>/data_final=<{pType}:dt_fim>', view_func=viewAPI,
                          methods=['GET', 'POST', 'PUT', 'DELETE'] )

        app.add_url_rule( f'{url}/data_inicial=<{pType}:dt_ini>', view_func=viewAPI,
                          methods=['GET', 'POST', 'PUT', 'DELETE'] )

        app.add_url_rule( f'{url}/programa=<{pType}:programa>', view_func=viewAPI,
                          methods=['GET', 'POST', 'PUT', 'DELETE'] )



class REQUEST(API):
    def __init__(self, endpoint='RESPONSE'):
        super().__init__(endpoint)
        self.__endpoint = endpoint

    @property
    def endpoint(self):
        return self.__endpoint

    @endpoint.setter
    def endpoint(self, new_Endpoint):
        self.__endpoint = new_Endpoint
