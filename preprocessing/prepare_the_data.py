from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import OrdinalEncoder
from sklearn.impute import SimpleImputer
from pandas.plotting import scatter_matrix
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.model_selection import train_test_split
from zlib import crc32
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import pandas as pd
import tarfile
import urllib.request


def load_housing_data():
    tarball_path = Path("datasets/housing.tgz")
    if not tarball_path.is_file():
        Path("datasets").mkdir(parents=True, exist_ok=True)
        url = "https://github.com/ageron/data/raw/main/housing.tgz"
        urllib.request.urlretrieve(url, tarball_path)
        with tarfile.open(tarball_path) as housing_tarball:
            housing_tarball.extractall(path="datasets")
    return pd.read_csv(Path("datasets/housing/housing.csv"))


# cleaning the data
housing = load_housing_data()

housing["income_cat"] = pd.cut(housing["median_income"],
                               bins=[0., 1.5, 3.0, 4.5, 6., np.inf],
                               labels=[1, 2, 3, 4, 5])

strat_split = StratifiedShuffleSplit(
    n_splits=1, test_size=0.2, random_state=42)
for train_index, test_index in strat_split.split(housing, housing["income_cat"]):
    strat_train_set = housing.loc[train_index]
    strat_test_set = housing.loc[test_index]

housing = strat_train_set.drop("median_house_value", axis=1)
housing_labels = strat_train_set["median_house_value"].copy()

housing.dropna(subset=["total_bedrooms"], inplace=True)
housing.drop("total_bedrooms", axis=1)
median = housing["total_bedrooms"].median()
housing["total_bedrooms"].fillna(median, inplace=True)

# using sklearn
imputer = SimpleImputer(strategy="median")
# selecting only the numerical columns
housing_num = housing.select_dtypes(include=[np.number])
# fitting the imputer
imputer.fit(housing_num)
# transforming the data
X = imputer.transform(housing_num)

housing_tr = pd.DataFrame(X, columns=housing_num.columns,
                          index=housing_num.index)

# print("housing_num", housing_num)
# print("housing_tr", housing_tr)

# Handling categorical attributes
housing_cat = housing[["ocean_proximity"]]
housing_cat.head(8)

# transforming the categorical data
ordinal_encorder = OrdinalEncoder()
housing_cat_encorded = ordinal_encorder.fit_transform(housing_cat)
print(housing_cat_encorded[:8])
print(ordinal_encorder.categories_)

# using sklearn one hot encoding
cat_encorder = OneHotEncoder()
housing_cat_1hot = cat_encorder.fit_transform(housing_cat)
print(housing_cat_1hot.toarray()[:8])
print(cat_encorder.categories_)

# using pandas get_dummies p144
df_test = pd.DataFrame({"ocean_proximity": ["INLAND", "NEAR BAY"]})
print(pd.get_dummies(df_test))

cat_encorder.transform(df_test)

df_test_unknown = pd.DataFrame({"ocean_proximity": ["<2H OCEAN", "ISLAND"]})
print(pd.get_dummies(df_test_unknown))
cat_encorder.handle_unknown = "ignore"
cat_encorder.transform(df_test_unknown)


print(cat_encorder.feature_names_in_)
print(cat_encorder.get_feature_names_out())
df_output = pd.DataFrame(cat_encorder.transform(df_test_unknown).toarray(),
                         columns=cat_encorder.get_feature_names_out(),
                         index=df_test_unknown.index)

# feature scaling
# Normalization

min_max_scaler = MinMaxScaler(feature_range=(-1, 1))
housing_num_min_max_scaled = min_max_scaler.fit_transform(housing_num)
print("minmax_housing_num:", housing_num_min_max_scaled[:8])

# Standardization
std_scaler = StandardScaler()
housing_num_std_scaled = std_scaler.fit_transform(housing_num)
print("std_housing_num:", housing_num_std_scaled[:8])

# inverse transformation
from sklearn.linear_model import LinearRegression

target_scaler = StandardScaler()

# housingをstrat_train_setに基づいて更新
housing = strat_train_set.drop("median_house_value", axis=1)
housing_labels = strat_train_set["median_house_value"].copy()

# ラベルのスケーリング
target_scsler = StandardScaler()
scaled_labels = target_scsler.fit_transform(housing_labels.to_frame())

# モデルのトレーニング
model = LinearRegression()
model.fit(housing[["median_income"]], scaled_labels)

# 新しいデータで予測
some_new_data = housing[["median_income"]].iloc[:5]
scaled_predictions = model.predict(some_new_data)
predictions = target_scsler.inverse_transform(scaled_predictions)
print(predictions)

# using the TransformedTargetRegressor
from sklearn.compose import TransformedTargetRegressor
model = TransformedTargetRegressor(LinearRegression(),
                                   transformer=StandardScaler())
model.fit(housing[["median_income"]], housing_labels)
predictions = model.predict(some_new_data)
print(predictions)