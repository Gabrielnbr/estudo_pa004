import os
import pickle
import pandas as pd
from flask import Flask, request, Response
from healthinsurance.HealthInsurance import HealthInsurance
import logging

# loading model
model = pickle.load( open('models/lr_model.pkl', 'rb' ) )

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
        log.exception("Erro no /predict")
        return Response('{"error":"internal error"}', status=500, mimetype="application/json")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)