import pickle
import pandas as pd
import json
import sklearn

with open('my_model.pk', 'rb') as model_file:
  my_model = pickle.load(model_file)

zip_code_df = pd.read_csv('median_income_by_zip_code.csv')

with open('states.json') as states_file:
  states_dict = json.load(states_file)

def predict(data):
  prediction_dataframe = pd.DataFrame({
    'state': [data['state']],
    'zipcode': [int(data['zipcode'])],
    'homeType': [data['homeType']],
    'livingArea': [float(data['livingArea'])],
    'bedrooms': [int(data['bedrooms'])],
    'bathrooms': [int(data['bathrooms'])],
    'lotArea': [float(data['lotArea'])]
  })
  prediction_dataframe['homeType'] = prediction_dataframe['homeType'].astype(pd.CategoricalDtype(categories=['SINGLE_FAMILY', 'CONDO', 'TOWNHOUSE', 'MULTI_FAMILY']))
  prediction_dataframe['state'] = prediction_dataframe['state'].astype(pd.CategoricalDtype(categories=states_dict.keys()))

  prediction_dataframe = pd.get_dummies(prediction_dataframe, columns=['homeType'])

  prediction_dataframe = pd.merge(prediction_dataframe, zip_code_df, how='left', left_on='zipcode', right_on='zip_code')

  prediction_dataframe['median_income'].fillna(prediction_dataframe['median_income'].mean(), inplace=True)

  prediction_dataframe.drop(['zipcode', 'zip_code'], axis=1, inplace=True)

  prediction_dataframe = pd.get_dummies(prediction_dataframe, columns=['state'])

  prediction_dataframe = prediction_dataframe[['bathrooms', 'bedrooms', 'livingArea', 'lotArea', 'homeType_CONDO',
       'homeType_MULTI_FAMILY', 'homeType_SINGLE_FAMILY', 'homeType_TOWNHOUSE',
       'median_income', 'state_AK', 'state_AL', 'state_AR', 'state_AZ',
       'state_CA', 'state_CO', 'state_CT', 'state_DC', 'state_DE', 'state_FL',
       'state_GA', 'state_HI', 'state_IA', 'state_ID', 'state_IL', 'state_IN',
       'state_KS', 'state_KY', 'state_LA', 'state_MA', 'state_MD', 'state_ME',
       'state_MI', 'state_MN', 'state_MO', 'state_MS', 'state_MT', 'state_NC',
       'state_ND', 'state_NE', 'state_NH', 'state_NJ', 'state_NM', 'state_NV',
       'state_NY', 'state_OH', 'state_OK', 'state_OR', 'state_PA', 'state_RI',
       'state_SC', 'state_SD', 'state_TN', 'state_TX', 'state_UT', 'state_VA',
       'state_VT', 'state_WA', 'state_WI', 'state_WV', 'state_WY']]

  price_prediction = my_model.predict(prediction_dataframe)

  return int(price_prediction[0])