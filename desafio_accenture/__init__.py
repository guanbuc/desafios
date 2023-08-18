# -*- encoding: utf-8 -*-
from class_audience_average_globo import *
import class_api_globo as API
import class_response_globo as RESPONSE
from app import app
import pandas as pd


#print('|'.join(i if 'query' in i else '' for i in dir(pd)))

#@app.route('/', methods=['GET'])
#def home():
#return dtf, 200


dtf = pd.DataFrame( {} )
clsRF = ASSEMBLER_DTF('./tvaberta_program_audience(1).csv', ',')
dtf = clsRF.averagingGroupDf()
clsRF = ASSEMBLER_DTF('./tvaberta_inventory_availability.csv(1).csv', ';')
clsRF.nwDtf = dtf

RESPONSE.dtf = clsRF.mergeDtf()

API.API().execAPI()

if __name__ == '__main__':
    app.run(debug=True)