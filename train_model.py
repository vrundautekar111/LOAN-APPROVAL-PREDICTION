import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

data = pd.read_csv("loan_data.csv")

print("========================================")
print("DATASET LOADED SUCCESSFULLY")
print("========================================")

print(data.head())

data.columns = data.columns.str.strip()

print("\nDataset columns:")
print(data.columns.tolist())

categorical_columns = [
    "Gender",
    "Married",
    "Dependents",
    "Education",
    "Self_Employed",
    "Property_Area"
]

numerical_columns = [
    "ApplicantIncome",
    "CoapplicantIncome",
    "LoanAmount",
    "Loan_Amount_Term",
    "Credit_History"
]

print("\nHandling missing values...")

for column in categorical_columns:

    if column in data.columns:

        data[column] = data[column].fillna(
            data[column].mode()[0]
        )


for column in numerical_columns:

    if column in data.columns:

        data[column] = pd.to_numeric(
            data[column],
            errors="coerce"
        )

        data[column] = data[column].fillna(
            data[column].median()
        )


print("Missing values handled successfully!")

print("\nEncoding categorical data...")

encoders = {}

for column in categorical_columns:

    if column in data.columns:

        encoder = LabelEncoder()

        data[column] = encoder.fit_transform(
            data[column].astype(str)
        )

        encoders[column] = encoder

target_encoder = LabelEncoder()

data["Loan_Status"] = target_encoder.fit_transform(
    data["Loan_Status"].astype(str)
)

encoders["Loan_Status"] = target_encoder

X = data.drop(
    "Loan_Status",
    axis=1
)

y = data["Loan_Status"]

if "Loan_ID" in X.columns:

    X = X.drop(
        "Loan_ID",
        axis=1
    )

if "id" in X.columns:

    X = X.drop(
        "id",
        axis=1
    )

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.20,

    random_state=42,

    stratify=y
)

print("\nTraining data:", X_train.shape)
print("Testing data:", X_test.shape)

print("\nTraining Logistic Regression model...")

model = LogisticRegression(
    max_iter=1000
)

model.fit(
    X_train,
    y_train
)


y_pred = model.predict(
    X_test
)

accuracy = accuracy_score(
    y_test,
    y_pred
)

print("\n========================================")
print("MODEL RESULTS")
print("========================================")

print(
    f"Accuracy: {accuracy * 100:.2f}%"
)


print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred
    )
)

model_data = {

    "model": model,

    "encoders": encoders,

    "features": list(X.columns)

}


with open(
    "loan_model.pkl",
    "wb"
) as file:

    pickle.dump(
        model_data,
        file
    )


print("\n========================================")
print("MODEL SAVED SUCCESSFULLY")
print("========================================")

print("Created file: loan_model.pkl")