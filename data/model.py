import pickle
import pandas as pd
from joblib import dump
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

df = pd.read_csv('cars.csv')
df = df.drop_duplicates()

df['mileage'].fillna(df['mileage'].mode()[0], inplace=True)
df['engine'].fillna(df['engine'].mode()[0], inplace=True)
df['max_power'].fillna(df['max_power'].mode()[0], inplace=True)
df['torque'].fillna(df['torque'].mode()[0], inplace=True)
df['seats'].fillna(df['seats'].mode()[0], inplace=True)

df.rename(columns={'mileage': 'mileage_kmpl'}, inplace=True)
df['mileage_kmpl'] = df['mileage_kmpl'].astype(
    str).str.split(' ').str[0].astype(float)

df.rename(columns={'engine': 'engine_cc'}, inplace=True)
df['engine_cc'] = df['engine_cc'].astype(
    str).str.replace('CC', '').astype(float)

df.rename(columns={'max_power': 'max_power_bhb'}, inplace=True)
df['max_power_bhb'] = df['max_power_bhb'].astype(str).str.replace('bhp', '')
df['max_power_bhb'] = pd.to_numeric(df['max_power_bhb'], errors='coerce')

df['max_power_bhb'].fillna(df['max_power_bhb'].mode()[0], inplace=True)

df['torque'] = df['torque'].str.split('rpm').str[0]
df.drop(['torque'], axis=1, inplace=True)
df.drop(['seats'], axis=1, inplace=True)

df['owner'] = df['owner'].map({'First Owner': 1, 'Second Owner': 2,
                              'Third Owner': 3, 'Fourth & Above Owner': 4, 'Test Drive Car': 0, })

index_to_drop = df['selling_price'].idxmax()

# Drop the row
df = df.drop(index_to_drop)
df['brand'] = df['name'].apply(lambda x: x.split(' ')[0])
df['model'] = df['name'].apply(lambda x: ' '.join(x.split(' ')[1:]))
cat_col = ['fuel', 'seller_type', 'transmission', 'brand', 'model']
num_col = ['year', 'km_driven', 'mileage_kmpl',
           'engine_cc', 'max_power_bhb', 'owner',]
df = pd.get_dummies(df, columns=cat_col)

X = df.drop(['selling_price', 'name',], axis=1)
y = df['selling_price']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)


mse = mean_squared_error(y_test, y_pred)
r2_square = r2_score(y_test, y_pred)
print('R-squared:', r2_square)
print('Mean Squared Error:', mse)


with open('../model.pickle', 'wb') as f:
    pickle.dump(model, f)


feature_names = X.columns.tolist()
with open('../feature_names.pickle', 'wb') as f:
    pickle.dump(feature_names, f)