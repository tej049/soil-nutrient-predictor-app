import streamlit as st
import joblib
from gtts import gTTS
import os

# Load trained model
model = joblib.load("soil_nutrient_model.joblib")

# Kannada voice response generator
def play_kannada_audio(text, filename="output.mp3"):
    tts = gTTS(text=text, lang='kn')
    tts.save(filename)
    os.system(f"start {filename}" if os.name == "nt" else f"mpg123 {filename}")

# App title
st.title("Soil Nutrient Deficiency Predictor")
st.markdown("Get predictions in **English and Kannada** with optional Kannada voice output.")

# Input fields (with Kannada labels)
temperature = st.number_input("Temperature (ತಾಪಮಾನ) in °C", 10.0, 50.0)
humidity = st.number_input("Humidity (ಆರ್ದ್ರತೆ) in %", 10, 100)
ph = st.number_input("Soil pH (ಮಣ್ಣಿನ ಪಿಎಚ್)", 3.0, 10.0)
ec = st.number_input("Electrical Conductivity (ವಿದ್ಯುತ್ ಚಾಲಕತೆ)", 0.0, 5.0)
organic_carbon = st.number_input("Organic Carbon (%) (ಸಸ್ಯ ಕಾರ್ಬನ್)", 0.1, 3.0)

soil_type = st.selectbox("Soil Type (ಮಣ್ಣಿನ ಪ್ರಕಾರ)", ['Loamy', 'Clay', 'Sandy', 'Silty'])
crop_type = st.selectbox("Crop Type (ಬೆಳೆ ಪ್ರಕಾರ)", ['Rice', 'Wheat', 'Maize', 'Sugarcane', 'Millet'])

# Categorical mapping
soil_map = {'Loamy': 0, 'Clay': 1, 'Sandy': 2, 'Silty': 3}
crop_map = {'Rice': 0, 'Wheat': 1, 'Maize': 2, 'Sugarcane': 3, 'Millet': 4}

# Predict button
if st.button("Predict (ಅಂದಾಜು ಮಾಡಿ)"):
    input_data = [[
        temperature, humidity, ph, ec, organic_carbon,
        soil_map[soil_type], crop_map[crop_type]
    ]]
    prediction = model.predict(input_data)[0]

    # Output mapping
    labels = ['Nitrogen', 'Phosphorus', 'Potassium']
    kannada_labels = ['ನೈಟ್ರೋಜನ್', 'ಫಾಸ್ಪರಸ್', 'ಪೊಟಾಷಿಯಮ್']
    recommendations = {
        'Nitrogen': "Apply Urea or Vermicompost.",
        'Phosphorus': "Apply Single Super Phosphate or Bone meal.",
        'Potassium': "Apply Muriate of Potash or Wood ash."
    }
    kannada_recommendations = {
        'Nitrogen': "ಯುರಿಯಾ ಅಥವಾ ವರ್ಮಿಕಂಪೋಸ್ಟ್ ಹಾಕಿ.",
        'Phosphorus': "ಸಿಂಗಲ್ ಸೂಪರ್ ಫಾಸ್ಫೇಟ್ ಅಥವಾ ಅಸ್ಥಿಮಜ್ಜೆ ಹಾಕಿ.",
        'Potassium': "ಮ್ಯೂರಿಯೇಟ್ ಆಫ್ ಪೊಟಾಶ್ ಅಥವಾ ಮರದ ಬೂದಿ ಹಾಕಿ."
    }

    st.subheader("Results (ಫಲಿತಾಂಶ):")
    response_text = ""

    for i, val in enumerate(prediction):
        if val == 0:
            st.error(f"Deficient in {labels[i]} ({kannada_labels[i]})")
            st.markdown(f"**Suggestion**: {recommendations[labels[i]]}  \n"
                        f"**ಸಲಹೆ**: {kannada_recommendations[labels[i]]}")
            response_text += f"{kannada_labels[i]} ಕೊರತೆ ಇದೆ. {kannada_recommendations[labels[i]]} "
        else:
            st.success(f"Sufficient {labels[i]} ({kannada_labels[i]})")
            response_text += f"{kannada_labels[i]} ಸರಿಯಾಗಿಯೇ ಇದೆ. "

# Example prediction result (replace this with your actual output)
english_output = "Your soil is Nitrogen deficient. Recommended: Urea fertilizer."
kannada_output = "ನಿಮ್ಮ ಮಣ್ಣುದಲ್ಲಿ ನೈಟ್ರೋಜನ್ ಕೊರತೆಯಿದೆ. ಶಿಫಾರಸು: ಯೂರಿಯಾ ಗೊಬ್ಬರ."

# Display both outputs
st.subheader("🪴 Result (ಫಲಿತಾಂಶ):")
st.markdown(f"**English**: {english_output}")
st.markdown(f"**Kannada (ಕನ್ನಡ)**: {kannada_output}")

# Voice Output in Kannada
if st.button("🔊 ಕನ್ನಡದಲ್ಲಿ ಸಲಹೆ ಕೇಳಿ (Voice Output in Kannada)"):
    try:
        tts = gTTS(text=kannada_output, lang='kn')
        tts.save("output.mp3")
        with open("output.mp3", "rb") as audio_file:
            st.audio(audio_file.read(), format="audio/mp3")
    except Exception as e:
        st.error("Voice generation failed. Error: {}".format(e))
