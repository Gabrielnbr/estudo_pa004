import pickle
import pandas as pd
from flask import Flask, request, Response
from deploy_test import HealthInsurance
import logging

# loading model
# path = '/Users/meigarom.lopes/repos/pa004_health_insurance_cross_sell/health_insurance_cross-sell/'
model = pickle.load( open('E:/3_recursos/2_area/profissional/cursos/22_06.1 - PA004/src/models/lr_model.pkl', 'rb' ) )

log = logging.getLogger(__name__)

# initialize API
app = Flask( __name__ )

@app.route( '/predict', methods=['POST'] )
def health_insurance_predict():
    try:
        test_json = request.get_json()

        if test_json: # there is data
            if isinstance( test_json, dict ): # unique example
                test_raw = pd.DataFrame( test_json, index=[0] )
                
            else: # multiple example
                test_raw = pd.DataFrame( test_json, columns=test_json[0].keys() )
                
            # Instantiate  class
            pipeline = HealthInsurance()
            a = type(test_raw)
            log.info(f"{a}")
            # data cleaning
            df1 = pipeline.data_cleaning( test_raw )
            
            # feature engineering
            df2 = pipeline.fe( df1 )
            
            # data preparation
            df3 = pipeline.data_prep( df2 )
            
            # prediction
            df_response = pipeline.get_prediction( model, test_raw, df3 )
            
            return df_response
            
        else:
            return Response( '{}', status=200, mimetype='application/json' )
    except Exception as e:
        log.exception("{e}")

if __name__ == '__main__':
    app.run( '0.0.0.0', port=5000, debug=True)