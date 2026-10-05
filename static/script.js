const loanForm = document.getElementById("loanForm");

loanForm.addEventListener("submit", async function (event) {

    event.preventDefault();

    const button =
        document.getElementById("predictButton");

    const resultDiv =
        document.getElementById("result");

    const gender =
        document.getElementById("gender").value;


    const married =
        document.getElementById("married").value;


    const dependents =
        document.getElementById("dependents").value;


    const education =
        document.getElementById("education").value;


    const selfEmployed =
        document.getElementById("self_employed").value;


    const applicantIncome =
        document.getElementById("applicant_income").value;


    const coapplicantIncome =
        document.getElementById("coapplicant_income").value;


    const loanAmount =
        document.getElementById("loan_amount").value;


    const loanTerm =
        document.getElementById("loan_term").value;


    const creditHistory =
        document.getElementById("credit_history").value;


    const propertyArea =
        document.getElementById("property_area").value;

    if (
        applicantIncome === "" ||
        coapplicantIncome === "" ||
        loanAmount === ""
    ) {

        resultDiv.style.display = "block";

        resultDiv.style.backgroundColor =
            "#fff3cd";

        resultDiv.style.borderColor =
            "#ffc107";

        resultDiv.style.color =
            "#856404";

        resultDiv.innerHTML =
            "⚠️ Please enter all required details.";

        return;
    }


    const data = {

        gender: gender,

        married: married,

        dependents: dependents,

        education: education,

        self_employed: selfEmployed,

        applicant_income: applicantIncome,

        coapplicant_income: coapplicantIncome,

        loan_amount: loanAmount,

        loan_term: loanTerm,

        credit_history: creditHistory,

        property_area: propertyArea

    };

    resultDiv.style.display = "block";

    resultDiv.style.backgroundColor =
        "#f0f4ff";

    resultDiv.style.borderColor =
        "#667eea";

    resultDiv.style.color =
        "#333";

    resultDiv.innerHTML =
        "⏳ Analyzing loan application...";


    button.disabled = true;

    button.innerHTML =
        "⏳ Predicting...";

    try {

        const response = await fetch(
            "/predict",
            {

                method: "POST",

                headers: {

                    "Content-Type":
                        "application/json"

                },

                body:
                    JSON.stringify(data)

            }
        );

        const result =
            await response.json();

        if (
            !response.ok ||
            result.error
        ) {

            resultDiv.style.display =
                "block";

            resultDiv.style.backgroundColor =
                "#fff0f0";

            resultDiv.style.borderColor =
                "#dc3545";

            resultDiv.style.color =
                "#dc3545";

            resultDiv.innerHTML =

                "❌ Prediction Error" +

                "<br><br>" +

                result.error;

            return;
        }

        const prediction =
            result.prediction;


        const probability =
            result.probability;

        if (
            prediction ===
            "Loan Approved"
        ) {

            resultDiv.style.display =
                "block";

            resultDiv.style.backgroundColor =
                "#e8f8ee";

            resultDiv.style.borderColor =
                "#28a745";

            resultDiv.style.color =
                "#198754";


            resultDiv.innerHTML =

                "<div style='font-size:32px;'>✅</div>" +

                "<div style='font-size:26px; margin:10px 0;'>" +

                "Loan Approved" +

                "</div>" +

                "<div>" +

                "Approval Probability: " +

                "<strong>" +

                probability +

                "%</strong>" +

                "</div>";

        }


        else {

            resultDiv.style.display =
                "block";

            resultDiv.style.backgroundColor =
                "#fff0f0";

            resultDiv.style.borderColor =
                "#dc3545";

            resultDiv.style.color =
                "#dc3545";


            resultDiv.innerHTML =

                "<div style='font-size:32px;'>❌</div>" +

                "<div style='font-size:26px; margin:10px 0;'>" +

                "Loan Not Approved" +

                "</div>" +

                "<div>" +

                "Approval Probability: " +

                "<strong>" +

                probability +

                "%</strong>" +

                "</div>";

        }

        console.log(
            "Prediction:",
            prediction
        );

        console.log(
            "Approval Probability:",
            probability + "%"
        );

    }

    catch (error) {

        console.error(
            "Connection Error:",
            error
        );


        resultDiv.style.display =
            "block";

        resultDiv.style.backgroundColor =
            "#fff0f0";

        resultDiv.style.borderColor =
            "#dc3545";

        resultDiv.style.color =
            "#dc3545";


        resultDiv.innerHTML =

            "❌ Unable to connect to server." +

            "<br><br>" +

            "Please make sure Flask is running on " +

            "<strong>http://127.0.0.1:8080</strong>";

    }

    finally {

        button.disabled = false;

        button.innerHTML =
            "🔍 Predict Loan Approval";

    }

});