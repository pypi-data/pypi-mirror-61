# Monitaur Client Library

Tested with:

1. Python 3.7.6
1. Python 3.6.10

## Install

```sh
$ pip install monitaur
```

## Example

```python
from monitaur import Monitaur
from monitaur.utils import hash_file


# create monitaur instance
monitaur = Monitaur(
    auth_key="changme",
    base_url="http://localhost:8008",
)

# train model
dataset = loadtxt("./_example/data.csv", delimiter=",")
seed = 7
test_size = 0.1
model_data = train_model(dataset, seed, test_size)
trained_model = model_data["trained_model"]
training_data = model_data["training_data"]
dump(trained_model, open(f"./_example/data.joblib", "wb"))


# add model to api
model_data = {
    "name": "Diabetes Classifier",
    "model_type": "xgboost",
    "model_class": "tabular",
    "library": "xg_boost",
    "trained_model_hash": hash_file("./_example/data.joblib"),  # trained model (None is allowed)
    "production_file_hash": hash_file("./_example/prediction.py"),  # production file used for running inputs through the trained model (None is allowed)
    "feature_number": 8,
    "owner": "Anthony Habayeb",
    "developer": "Andrew Clark",
    "influences": True,
}
model_set_id = monitaur.add_model(**model_data)

# get aws credentials
credentials = monitaur.get_credentials(model_set_id)

# record training
record_training_data = {
    "credentials": credentials,
    "model_set_id": model_set_id,
    "trained_model": trained_model,
    "training_data": training_data,
    "feature_names": [
        "Pregnancies",
        "Glucose",
        "BloodPressure",
        "SkinThickness",
        "Insulin",
        "BMI",
        "DiabetesPedigreeF",
        "Age",
    ],
    # "re_train": True
}
monitaur.record_training(**record_training_data)

# record transaction
prediction = get_prediction([2, 84, 68, 27, 0, 26.7, 0.341, 32])
transaction_data = {
    "credentials": credentials,
    "model_set_id": model_set_id,
    "trained_model_hash": hash_file("./_example/data.joblib"),
    "production_file_hash": hash_file("./_example/prediction.py"),
    "prediction": prediction,
    "features": {
        "Pregnancies": 2,
        "Glucose": 84,
        "BloodPressure": 68,
        "SkinThickness": 27,
        "Insulin": 0,
        "BMI": 26.7,
        "DiabetesPedigreeF": 0.341,
        "Age": 32,
    },
}
response = monitaur.record_transaction(**transaction_data)
print(response)
```
