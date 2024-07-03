import pandas as pd
import json

df = pd.read_csv('./data/cars.csv')

df.rename(columns={'mileage': 'mileage_kmpl'}, inplace=True)
df['mileage_kmpl'] = df['mileage_kmpl'].astype(
    str).str.split(' ').str[0].astype(float)

df.rename(columns={'engine': 'engine_cc'}, inplace=True)
df['engine_cc'] = df['engine_cc'].astype(
    str).str.replace('CC', '').astype(float)

df.rename(columns={'max_power': 'max_power_bhb'}, inplace=True)
df['max_power_bhb'] = df['max_power_bhb'].astype(str).str.replace('bhp', '')

df['max_power_bhb'] = pd.to_numeric(df['max_power_bhb'], errors='coerce')
df['owner'] = df['owner'].map({'First Owner': 1, 'Second Owner': 2,
                              'Third Owner': 3, 'Fourth & Above Owner': 4, 'Test Drive Car': 0, })


df['brand'] = df['name'].apply(lambda x: x.split(' ')[0])
df['model'] = df['name'].apply(lambda x: ' '.join(x.split(' ')[1:]))
df['brand'].unique()


cars_name = df.groupby('brand')['model'].unique().to_dict()

for key in cars_name:
    cars_name[key] = cars_name[key].tolist()

fuel = df['fuel'].unique().tolist()
transmission = df['transmission'].unique().tolist()
owner = df['owner'].unique().tolist()
years = [int(df['year'].min()), int(df['year'].max())]
km_driven = [int(df['km_driven'].min()), int(df['km_driven'].max())]
engine_cc = [df['engine_cc'].min(), df['engine_cc'].max()]
max_power_bhb = [float(df['max_power_bhb'].min()),
                 float(df['max_power_bhb'].max())]
mileage = [float(df['mileage_kmpl'].min()), float(df['mileage_kmpl'].max())]
seller = df['seller_type'].unique().tolist()

data = {
    'name': cars_name,
    'fuel': fuel,
    'transmission': transmission,
    'owner': owner,
    'year': years,
    'km_driven': km_driven,
    'engine_cc': engine_cc,
    'max_power_bhb': max_power_bhb,
    'mileage_kmpl': mileage,
    'seller': seller,
}

with open('car_data.json', 'w') as f:
    json.dump(data, f)
