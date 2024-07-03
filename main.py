import streamlit as st
import pickle as pk
import json
import pandas as pd


    

def add_missing_columns(df,columns):
    print('add_missing')
    missing_columns = set(columns)-set(df.columns)
    for c in missing_columns:
        df[c]=0
    return df[columns]

def get_user_df(data):
    with open('feature_names.pickle', 'rb') as f:
        feature_names = pk.load(f)

    df = pd.DataFrame(data, index=[0])
    cat_col = ['fuel','seller_type','transmission','brand','model']
    df = pd.get_dummies(df,columns=cat_col)
    df = add_missing_columns(df,feature_names)
    return df

def main():

    with open('car_data.json', 'r') as f:
        car_data = json.load(f)
    
    with open('model.pickle', 'rb') as f:
        model = pk.load(f)



    st.set_page_config(
        layout="centered",
        page_title="Car Price",
        initial_sidebar_state="auto"
    )
    
    st.write(
        """
        # Car Price Prediction 
        # 🚗

        """
    )
    left, right = st.columns((2, 2))
    # sliders
    year = right.slider(
        'Year', min_value=car_data['year'][0], max_value=car_data['year'][1])
    km = right.slider(
        'KM driven', min_value=car_data['km_driven'][0], max_value=car_data['km_driven'][1])
    mileage = right.slider(
        'Mileage', min_value=car_data['mileage_kmpl'][0], max_value=car_data['mileage_kmpl'][1])
    engine = right.slider(
        'Engine CC', min_value=car_data['engine_cc'][0], max_value=car_data['engine_cc'][1])
    max_power = right.slider(
        'Max', min_value=car_data['max_power_bhb'][0], max_value=car_data['max_power_bhb'][1])

    # select box
    brand = left.selectbox('Brand', car_data['name'].keys())
    car_model = left.selectbox('Model', car_data['name'][brand])
    fuel = left.selectbox('Fuel', car_data['fuel'])
    transmission = left.selectbox('Transmission',car_data['transmission'])
    seller_type = left.selectbox('Seller', car_data['seller'])
    owner = left.selectbox('Owner', car_data['owner'])
    #user data
    data = {
        'year': year,
        'km_driven': km,
        'fuel': fuel,
        'seller_type': seller_type,
        'transmission': transmission,
        'owner': owner,
        'mileage_kmpl': mileage,
        'engine_cc': engine,
        'max_power_bhb': max_power,
        'brand': brand,
        'model': car_model
    }

    
 
    # df = pd.DataFrame(data, index=[0])
    # cat_col = ['fuel','seller_type','transmission','brand','model']
    # df = pd.get_dummies(df,columns=cat_col)
    # df = add_missing_columns(df,feature_names)

    button = st.button('Predict')
    
    if button:
        user_data = get_user_df(data)
        res = model.predict(user_data)
        st.write(f'Price:{int(res)} $')



if __name__ == "__main__":
    main()
