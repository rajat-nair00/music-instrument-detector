Music Instrument Detector & Separator (Django Web App)
Overview
This web application enables users to upload music/audio files and receive:

Automated detection of musical instruments present in the track (using TensorFlow and YAMNet features)

Separation of audio into individual instrument stems (using Demucs)

Instant playback and download of detected instrument stems from the browser

It is built with Django and integrates advanced audio processing models.

Features
Upload audio files (WAV/MP3 supported)

AI Instrument Detection: Identifies instruments such as Voice, Electric Guitar, Piano, Saxophone, etc.

Audio Source Separation: Splits music into stems like vocals, drums, bass, guitar, etc.

Web Playback: Play the original track and separated stems directly from the web interface

Download: Save original and stem files for personal use

Getting Started
1. Clone the repository
text
git clone https://github.com/rajat-nair00/music-instrument-detector.git
cd music-instrument-detector
3. Install Python dependencies
Ensure Python 3.9 or newer is installed.

text
pip install -r requirements.txt
Dependencies include:

django

tensorflow

tensorflow-hub

librosa

demucs

soundfile

tqdm

scikit-learn

3. Prepare Model Files
Create a folder audio/models/ inside your Django app and place:

trained_model.h5 — your trained Keras model file

label_encoder.pkl — your label encoder for instruments

4. Run Database Migrations and Create Admin User
text
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
5. Start the Development Server
text
python manage.py runserver
Open your browser at http://localhost:8000/ to access the app.

Usage Instructions
Upload music/audio files via the web form.

View a list of instruments detected in the audio.

Listen to the separate instrument stems through the embedded player.

Download the original or separated audio files.

Project Structure
text
audio/                  # Django app handling audio processing
    models/             # Contains your trained model and encoder
    templates/audio_processor/
        base.html
        home.html
        upload.html
        result.html
    static/             # Optional, for static files
media/                  # Uploaded audio and processed stems storage
manage.py
requirements.txt
README.md
.gitignore
Notes
During development, Django serves media files; configure production storage accordingly.

Supported audio formats include WAV and MP3. Large files should be tested and handled for upload limits.

The instrument detection uses a deep learning model trained with YAMNet embeddings.

Credits
IRMAS Dataset

Demucs for audio source separation

YAMNet for audio embeddings

Django Web Framework

