from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .forms import AudioUploadForm
from .models import AudioUpload
from .utils import detect_instruments
from django.conf import settings
import os
import shutil
import librosa
import numpy as np

def home(request):
    return render(request, 'home.html')

# Use Demucs for separation via subprocess
def separate_stems(filepath, output_dir):
    import subprocess
    os.makedirs(output_dir, exist_ok=True)
    subprocess.run(
        f'demucs "{filepath}" -o "{output_dir}"',
        shell=True, check=True
    )

# Check if audio has meaningful sound
def has_sound(audio_path, rms_threshold_db=-45, amp_threshold=0.01):
    y, sr = librosa.load(audio_path, sr=None)
    rms = librosa.feature.rms(y=y).mean()
    rms_db = librosa.amplitude_to_db([rms])[0]
    max_amp = np.max(np.abs(y))
    return (rms_db > rms_threshold_db) and (max_amp > amp_threshold)

def upload_audio(request):
    if request.method == 'POST':
        form = AudioUploadForm(request.POST, request.FILES)
        if form.is_valid():
            audio_obj = form.save()
            return redirect('result', pk=audio_obj.pk)
    else:
        form = AudioUploadForm()
    return render(request, 'upload.html', {'form': form})

def audio_result(request, pk):
    audio = get_object_or_404(AudioUpload, pk=pk)
    filepath = audio.file.path

    # Detect instruments
    detected_instruments = detect_instruments(filepath)

    # Separate audio stems folder path
    stems_dir = os.path.join(settings.MEDIA_ROOT, 'stems', str(pk))

    # Run separation if stems folder does not exist
    if not os.path.exists(stems_dir):
        separate_stems(filepath, os.path.join(settings.MEDIA_ROOT, 'stems'))

    # Demucs outputs in media/stems/htdemucs/[basename]/
    base = os.path.splitext(os.path.basename(filepath))[0]
    demucs_out = os.path.join(settings.MEDIA_ROOT, 'stems', 'htdemucs', base)

    stems = []
    if os.path.exists(demucs_out):
        for fname in os.listdir(demucs_out):
            out_path = os.path.join(demucs_out, fname)

            # Copy only meaningful stems to MEDIA root for playback
            if has_sound(out_path):
                stem_dest = os.path.join(settings.MEDIA_ROOT, 'stems', f"{pk}_{fname}")
                if not os.path.exists(stem_dest):
                    shutil.copy2(out_path, stem_dest)
                stems.append((f'stems/{pk}_{fname}', fname.split('.')[0]))

    return render(request, 'result.html', {
    'audio': audio,
    'instruments': detected_instruments,
    'stems': stems,
    'MEDIA_URL': settings.MEDIA_URL,
})

# Create your views here.
