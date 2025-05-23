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


housing = load_housing_data()

print(housing.head())
housing.info()

print(housing["ocean_proximity"].value_counts())
print(housing.describe())

housing.hist(bins=50, figsize=(12, 8))
plt.show()


def shuffle_and_split_data(data, test_ratio):
    shuffled_indices = np.random.permutation(len(data))
    test_set_size = int(len(data) * test_ratio)
    test_indices = shuffled_indices[:test_set_size]
    train_indices = shuffled_indices[test_set_size:]
    return data.iloc[train_indices], data.iloc[test_indices]


train_set, test_set = shuffle_and_split_data(housing, 0.2)
print('trainset:', len(train_set))
print('testset:', len(test_set))


def is_id_in_test_set(identifier, test_ratio):
    return crc32(np.int64(identifier)) < test_ratio*2**32


def split_data_with_id_hash(data, test_ratio, id_column):
    ids = data[id_column]
    in_test_set = ids.apply(lambda id_: is_id_in_test_set(id_, test_ratio))
    return data.loc[~in_test_set], data.loc[in_test_set]


# building an id based on the index
housing_with_id = housing.reset_index()
train_set, test_set = split_data_with_id_hash(housing_with_id, 0.2, "index")

# building an id based on the latitude and longitude
housing_with_id["id"] = housing["longitude"]*1000+housing["latitude"]
train_set, test_set = split_data_with_id_hash(housing_with_id, 0.2, "id")

# using sklearn to split the data
train_set, test_set = train_test_split(housing, test_size=0.2, random_state=42)

# creating an income category attribute
housing["income_cat"] = pd.cut(housing["median_income"],
                               bins=[0., 1.5, 3.0, 4.5, 6., np.inf],
                               labels=[1, 2, 3, 4, 5])

housing["income_cat"].value_counts().sort_index().plot.bar(rot=0, grid=True)
plt.xlabel("Income category")
plt.ylabel("Number of districts")
plt.show()

# stratified sampling based on the income category 分割比率を全体の比率と変えずに実行

splitter = StratifiedShuffleSplit(n_splits=10, test_size=0.2, random_state=42)
strat_splits = []
for train_index, test_index in splitter.split(housing, housing["income_cat"]):
    strat_train_set_n = housing.iloc[train_index]
    strat_test_set_n = housing.iloc[test_index]
    strat_splits.append([strat_test_set_n, strat_test_set_n])

strat_train_set, strat_test_set = strat_splits[0]

strat_train_set, strat_test_set = train_test_split(
    housing, test_size=0.2, stratify=housing["income_cat"], random_state=42)

print(strat_test_set["income_cat"].value_counts()/len(strat_test_set))

# removing the income category attribute
for set in (strat_train_set, strat_test_set):
    set.drop("income_cat", axis=1, inplace=True)

housing = strat_train_set.copy()

housing.plot(kind="scatter", x="longitude", y="latitude", grid=True)
plt.show()

housing.plot(kind="scatter", x="longitude", y="latitude", alpha=0.2)
plt.show()

housing.plot(kind="scatter", x="longitude", y="latitude", alpha=0.4,
             s=housing["population"]/100, label="population",
             c="median_house_value", cmap=plt.get_cmap("jet"), colorbar=True,
             legend=True, sharex=False, figsize=(10, 7))
plt.show()

# LabelEncoderのインスタンス化
label_encoder = LabelEncoder()
# ocean_proximityをカテゴリー変数に変換
housing["ocean_proximity"] = label_encoder.fit_transform(
    housing["ocean_proximity"])
print(housing["ocean_proximity"])

# Looking for Correlations
corr_matrix = housing.corr()
corr_matrix["median_house_value"].sort_values(ascending=False)

attributes = ["median_house_value", "median_income", "total_rooms",
              "housing_median_age"]
scatter_matrix(housing[attributes], figsize=(12, 8))
plt.show()

housing.plot(kind="scatter", x="median_income",y="median_house_value",
             alpha=0.1, grid=True)