from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd

app = Flask(__name__)

try:

    with open(
        "loan_model.pkl",
        "rb"
    ) as file:

        saved_data = pickle.load(file)

    model = saved_data["model"]

    encoders = saved_data["encoders"]

    features = saved_data["features"]

    print("========================================")
    print("MODEL LOADED SUCCESSFULLY")
    print("========================================")

except Exception as e:

    print("Error loading model:")
    print(e)

    model = None
    encoders = {}
    features = []

@app.route("/")
def home():

    return render_template(
        "index.html"
    )

@app.route(
    "/predict",
    methods=["POST"]
)
def predict():

    try:

        if model is None:

            return jsonify({
                "error": "Model is not loaded."
            }), 500

        data = request.get_json()

        print("\nReceived data:")
        print(data)

        gender = data["gender"]

        married = data["married"]

        dependents = data["dependents"]

        education = data["education"]

        self_employed = data["self_employed"]

        applicant_income = float(
            data["applicant_income"]
        )

        coapplicant_income = float(
            data["coapplicant_income"]
        )

        loan_amount = float(
            data["loan_amount"]
        )

        loan_term = float(
            data["loan_term"]
        )

        credit_history = float(
            data["credit_history"]
        )

        property_area = data["property_area"]

        gender_encoded = encoders[
            "Gender"
        ].transform(
            [gender]
        )[0]


        married_encoded = encoders[
            "Married"
        ].transform(
            [married]
        )[0]


        dependents_encoded = encoders[
            "Dependents"
        ].transform(
            [dependents]
        )[0]


        education_encoded = encoders[
            "Education"
        ].transform(
            [education]
        )[0]


        self_employed_encoded = encoders[
            "Self_Employed"
        ].transform(
            [self_employed]
        )[0]


        property_area_encoded = encoders[
            "Property_Area"
        ].transform(
            [property_area]
        )[0]

        input_values = {

            "Gender":
                gender_encoded,

            "Married":
                married_encoded,

            "Dependents":
                dependents_encoded,

            "Education":
                education_encoded,

            "Self_Employed":
                self_employed_encoded,

            "ApplicantIncome":
                applicant_income,

            "CoapplicantIncome":
                coapplicant_income,

            "LoanAmount":
                loan_amount,

            "Loan_Amount_Term":
                loan_term,

            "Credit_History":
                credit_history,

            "Property_Area":
                property_area_encoded

        }


        input_data = pd.DataFrame(
            [input_values]
        )

        input_data = input_data[
            features
        ]


        print("\nInput data:")
        print(input_data)

        prediction = model.predict(
            input_data
        )[0]


        probability = model.predict_proba(
            input_data
        )[0]

        approved_class = encoders[
            "Loan_Status"
        ].transform(
            ["Y"]
        )[0]


        if prediction == approved_class:

            result = "Loan Approved"

        else:

            result = "Loan Not Approved"

        approval_probability = (
            probability[
                list(model.classes_).index(
                    approved_class
                )
            ] * 100
        )


        approval_probability = round(
            approval_probability,
            2
        )


        print("\nPrediction:")
        print(result)

        print(
            "Approval Probability:",
            approval_probability,
            "%"
        )

        return jsonify({

            "prediction": result,

            "probability":
                approval_probability

        })


    except Exception as e:

        print("\nPrediction Error:")
        print(e)

        return jsonify({

            "error": str(e)

        }), 400

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=8080,
        debug=True
    )