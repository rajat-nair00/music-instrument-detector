import os
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import pickle
import librosa

# --- Configure Your Model Directory ---
# Absolute path to your models folder
MODEL_DIR = r'C:\Users\Dell\Documents\Rajat Nair\SCOPE_OJT\Music\audio\models'

# --- Load YAMNet Model Once ---
yamnet_handle = 'https://tfhub.dev/google/yamnet/1'
yamnet_model = hub.load(yamnet_handle)

# --- Load Trained Model and Label Encoder Once ---
MODEL_PATH = os.path.join(MODEL_DIR, 'trained_model.h5')
ENCODER_PATH = os.path.join(MODEL_DIR, 'label_encoder.pkl')

# Make sure both files exist; helpful for debugging
assert os.path.exists(MODEL_PATH), f"Model file not found: {MODEL_PATH}"
assert os.path.exists(ENCODER_PATH), f"Encoder file not found: {ENCODER_PATH}"

model = tf.keras.models.load_model(MODEL_PATH)
with open(ENCODER_PATH, 'rb') as f:
    encoder = pickle.load(f)

INSTRUMENT_LABELS = {
    'voi': 'Voice',
    'gel': 'Electric Guitar',
    'gac': 'Acoustic Guitar',
    'pia': 'Piano',
    'org': 'Organ',
    'sax': 'Saxophone',
    # Add other codes as needed
}

# --- Feature Extraction ---
def extract_yamnet_features(filepath, sr=16000, duration=4):
    audio, orig_sr = librosa.load(filepath, sr=sr, duration=duration)
    if len(audio) < duration * sr:
        audio = np.pad(audio, (0, duration * sr - len(audio)))
    if orig_sr != sr:
        audio = librosa.resample(audio, orig_sr, sr)
    scores, embeddings, _ = yamnet_model(audio)
    return np.mean(embeddings.numpy(), axis=0)

# --- Instrument Detection ---
def detect_instruments(filepath, threshold=0.2):
    features = extract_yamnet_features(filepath)
    features = np.expand_dims(features, axis=0)
    predictions = model.predict(features)[0]

    detected = []
    for idx, prob in enumerate(predictions):
        if prob >= threshold:
            code = encoder.inverse_transform([idx])[0]
            instrument = INSTRUMENT_LABELS.get(code, code)  # fallback to code if not mapped
            detected.append({
                'instrument': instrument,
                'confidence': round(float(prob) * 100, 2)
            })
    return detected



