import librosa
import numpy as np

from matplotlib import pyplot as plt
from matplotlib import animation

import moviepy
import moviepy.editor as mp
#from moviepy.editor import *

import subprocess

import os
from app import app, mongo

class Generate_video():



    '''def __init__(self, filename):
        #self.audio = audio
        self.filename = filename

        self.audio = mongo.send_file(filename)

        if self.filename.endswith('.mp3'):
            subprocess.call(['ffmpeg', '-i', 'uploads/'+{self.filename}, 'input_audio.wav'])
            self.filename = 'input_audio.wav'''

    def generate_video(file_path, filename):

        #audio = mongo.send_file(filename)
        #audio = file_path
        audio = mongo.db.user.find_one({"audio": filename})
        #audio processing

        #creating animation
        def create_circle(idata):
            circle = plt.Circle((0, 0), idata[0], color = 'c')
            return circle

        def update_radius(i, circle, idata):
            circle.radius = idata[i*100]
            return circle

        #idata, audio_length = process()

    #def process():
        file_path_new = str("uploads\\") + filename
        time_series, rate = librosa.load(file_path_new)
        #stft
        data = np.abs(librosa.stft(time_series, hop_length=512, n_fft=2048*4))
        #inverse short-time fourier transform
        idata = (librosa.istft(data)*(10**4))
        idata = list(idata)
        audio_length = librosa.get_duration(y=time_series, sr=rate)
            #return idata, audio_length

        print("processesd audio")
        #anim = create_animation(idata)

    #def create_animation(idata):

        fig = plt.gcf()
        ax = plt.axes(xlim=(-50, 50), ylim=(-50, 50))
        ax.set_aspect('equal')
        plt.axis('off')
        plt.rcParams['figure.facecolor'] = 'black'
        circle = create_circle(idata)
        ax.add_patch(circle)
        anim = animation.FuncAnimation(fig, update_radius, fargs = (circle,))
            #return anim

        print("animation ready!")

        gif_anim = anim.save('output.gif', writer = 'ffmpeg', savefig_kwargs={'facecolor': 'black'})

        print("Saved animation as gif")

        clip = mp.VideoFileClip("output.gif")
        c = moviepy.video.fx.all.loop(clip, duration=audio_length)
        c.write_videofile("output.mp4")
        clip.close()
        cmd = f'ffmpeg -y -i {file_path}  -r 30 -i output.mp4  -filter:a aresample=async=1 -c:a flac -c:v copy -strict -2 video_output.mp4'
        output = subprocess.check_output(cmd, shell=True)
        output.save(app.config['DOWNLOAD_FOLDER'], 'video_output.mp4')
        #mongo.db.user.insert(output, 'video_output.mp4')
        #output = subprocess.call(cmd, shell=True)
        #output.save(os.path.join('output', 'video_output.mp4'))
        return f'video_output.mp4'
