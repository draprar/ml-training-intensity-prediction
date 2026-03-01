const activitySelect = document.getElementById("ActivityType");
const predictButtonWrapper = document.getElementById("PredictButtonWrapper");
const form = document.getElementById("predictForm");
const resultBox = document.getElementById("resultBox");

const activityFields = {
    "Walking": ["DistanceField", "StepsField"],
    "Yoga": ["AvgStressField", "StressChangeField"],
    "Strength": ["TotalRepsField", "TotalPosesField"],
    "Cardio": []
};

// Hides all matching elements and removes the required attribute
function hideFields(selector) {
    document.querySelectorAll(selector).forEach(el => {
        el.classList.add("d-none");
        el.querySelectorAll("input, select").forEach(input => {
            input.required = false;
        });
    });
}

// Shows elements by ID and sets their inputs as required
function showFieldsById(ids) {
    ids.forEach(id => {
        const el = document.getElementById(id);
        if (!el) return;
        el.classList.remove("d-none");
        el.querySelectorAll("input, select").forEach(input => {
            input.required = true;
        });
    });
}

// Handles activity change: hides all fields,
// then shows common + activity-specific fields
function updateFields() {
    const selected = activitySelect.value;

    hideFields(".specific-field");
    hideFields(".common-field");
    predictButtonWrapper.classList.add("d-none");

    if (!selected) return;

    document.querySelectorAll(".common-field").forEach(el => {
        el.classList.remove("d-none");
        el.querySelectorAll("input, select").forEach(input => {
            input.required = true;
        });
    });

    showFieldsById(activityFields[selected] || []);
    predictButtonWrapper.classList.remove("d-none");
}

activitySelect.addEventListener("change", updateFields);

// Handles form submission:
// - converts empty fields to 0
// - casts numeric values
// - sends POST request
// - displays result or error
form.addEventListener("submit", async function (event) {
    event.preventDefault();

    resultBox.className = "alert alert-info mt-4 d-none";

    const formData = new FormData(form);
    const jsonData = Object.fromEntries(formData.entries());

    for (let key in jsonData) {
        if (jsonData[key] === "") {
            jsonData[key] = 0;
        } else if (!isNaN(jsonData[key])) {
            jsonData[key] = Number(jsonData[key]);
        }
    }

    try {
        const response = await axios.post("/predict", jsonData);
        const value = response.data.calories_per_min.toFixed(4);

        resultBox.classList.remove("d-none");
        resultBox.innerHTML =
            `<strong>Prediction result:</strong> ${value} kcal/min`;

    } catch (error) {
        resultBox.className = "alert mt-4 alert-danger";
        resultBox.classList.remove("d-none");

        if (error.response?.data?.detail) {
            resultBox.innerText = "Error: " + error.response.data.detail;
        } else {
            resultBox.innerText = "Server error.";
        }

        resultBox.scrollIntoView({ behavior: "smooth" });
    }
});