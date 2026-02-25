const activitySelect = document.getElementById("ActivityType");
const predictButton = document.getElementById("PredictButtonWrapper");
const form = document.getElementById("predictForm");
const resultBox = document.getElementById("resultBox");

const activityFields = {
    "Walking": ["DistanceField", "StepsField"],
    "Yoga": ["AvgStressField", "StressChangeField"],
    "Strength": ["TotalRepsField", "TotalPosesField"],
    "Cardio": []
};

// Ukrywa wszystkie pasujące elementy i usuwa obowiązek wypełniania ich pól
function hideFields(selector) {
    document.querySelectorAll(selector).forEach(el => {
        el.classList.add("d-none");
        el.querySelectorAll("input, select").forEach(i => i.required = false);
    });
}

// Pokazuje elementy o podanych ID i ustawia ich pola jako wymagane
function showFieldsById(ids) {
    ids.forEach(id => {
        const el = document.getElementById(id);
        el.classList.remove("d-none");
        el.querySelectorAll("input, select").forEach(i => i.required = true);
    });
}

// Reaguje na zmianę aktywności, ukrywa wszystko, pokazuje pola wspólne i specyficzne i przycisk predykcji
function updateFields() {
    const selected = activitySelect.value;

    hideFields(".specific-field");
    hideFields(".common-field");
    predictButton.classList.add("d-none");

    if (!selected) return;

    document.querySelectorAll(".common-field").forEach(el => {
        el.classList.remove("d-none");
        el.querySelectorAll("input, select").forEach(i => i.required = true);
    });

    showFieldsById(activityFields[selected] || []);
    predictButton.classList.remove("d-none");
}

activitySelect.addEventListener("change", updateFields);

// przetwarza formularz, zamienia puste pola na 0, wysyła dane do serwera i wyświetla wynik lub błąd
form.addEventListener("submit", async function (event) {
    event.preventDefault();

    resultBox.className = "alert alert-info mt-4 d-none";

    const formData = new FormData(form);
    const jsonData = Object.fromEntries(formData.entries());

    for (let key in jsonData) {
        if (jsonData[key] === "") {
            jsonData[key] = 0; // domyślna wartość dla ukrytych pól
        } else if (!isNaN(jsonData[key])) {
        jsonData[key] = Number(jsonData[key]);
        }
    }

    try {
        const response = await axios.post("/predict", jsonData);
        const value = response.data.calories_per_min.toFixed(4);

        resultBox.classList.remove("d-none");
        resultBox.innerHTML =
            `<strong>Wynik predykcji:</strong> ${value} kcal/min`;

    } catch (error) {
        resultBox.className = "alert mt-4";   // reset klas
        resultBox.classList.remove("d-none");
        resultBox.classList.add("alert-danger");

        if (error.response && error.response.data && error.response.data.detail) {
            resultBox.innerText = "Błąd: " + error.response.data.detail;
        } else {
            resultBox.innerText = "Błąd serwera.";
        }

        resultBox.scrollIntoView({ behavior: "smooth" });
    }
});