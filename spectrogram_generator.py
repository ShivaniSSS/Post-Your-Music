from librosa.core import audio
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import librosa

import numpy as np

import moviepy.editor as mp

from itertools import count

window = 100000
#window = 100
jump = 1000
interval = 1

filename = 'file_example_WAV_1MG.wav'

sound, rate = librosa.load(filename,sr=None)

audio_length = librosa.get_duration(filename = 'file_example_WAV_1MG.wav')


# Size of the FFT, which will also be used as the window length
n_fft=2048

# Step or stride between windows. If the step is smaller than the window lenght, the windows will overlap
hop_length=512

# Calculate the spectrogram as the square of the complex magnitude of the STFT
spectrogram_librosa = np.abs(librosa.stft(
    sound, n_fft=n_fft, hop_length=hop_length, win_length=n_fft, window='hann')) ** 2

spectrogram_librosa_db = librosa.power_to_db(spectrogram_librosa, ref=np.max)

frequencies = librosa.core.fft_frequencies(n_fft=2048*4)

#interval = 512/rate *1000

fig = plt.figure()
plt.axis('off')
plt.rcParams['figure.facecolor'] = 'black'

_, _, _, im = plt.specgram(frequencies[:2048], Fs=2048*4)
#_, _, _, im = plt.specgram(sound[:1], Fs=rate)

index = count()

def animate(i):
    #_, _, _, im = plt.specgram(sound[i*jump:(i*jump)+window], Fs=rate)
    _, _, _, im = plt.specgram(frequencies[i:i+2048], Fs=2048*4)
    plt.colorbar(format='%+2.0f dB')
    return im,

ani = animation.FuncAnimation(fig, animate, interval=interval, blit=True)

#fps2 = var/audio_length

total_frames = sound.shape[0]/n_fft
framesps = abs(total_frames/audio_length)

ani.save('test.gif', writer = 'ffmpeg', fps = rate, savefig_kwargs={'facecolor': 'black'})


clip = mp.VideoFileClip("test.gif")
clip.set_audio(filename)
clip.write_videofile("test_output.mp4")

clip.close()

#plt.ion()
#plt.show()