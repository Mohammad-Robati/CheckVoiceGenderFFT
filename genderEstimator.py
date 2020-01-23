import librosa
import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import fft, fftfreq
from os import listdir
from os.path import isfile, join


class GenderEstimator:

    def __init__(self):
        self.amplifier = 1000000

    def readFile(self, file):
        amplitudes, sampleRate = librosa.load(file)
        return amplitudes, sampleRate

    def calculatePSD(self, file):
        y, sr = self.readFile(file)
        n = len(y)
        freqs = fftfreq(n)
        mask = freqs > 0
        fft_vals = fft(y)
        psd = self.amplifier * (np.abs(fft_vals / n) ** 2)
        #self.plot(psd, freqs, mask, sr)
        return psd, freqs, mask, sr

    def getMaxFrequency(self, file):
        psd, freqs, mask, sr = self.calculatePSD(file)
        maxPower = max(psd[mask])
        maxFrequency = (freqs[mask]*sr)[list.index(list(psd[mask]), maxPower)]
        return maxFrequency

    def findGender(self, file):
        maxFrequency = self.getMaxFrequency(file)
        if 45 < maxFrequency < 165:
            return 'male'
        elif 165 < maxFrequency < 300:
            return 'female'
        else:
            return 'none'

    def processFolder(self, folder):
        files = [f for f in listdir(folder) if isfile(join(folder, f))]
        for file in files:
            if file[0] == '.':
                files.remove(file)
        list.sort(files)
        vector = {}
        for file in files:
            vector[file] = self.findGender(folder+'/'+file)
        return vector

    def plot(self, psd, freqs, mask, sr):
        plt.plot(freqs[mask] * sr, psd[mask])
        plt.show()
