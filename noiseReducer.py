import librosa
import numpy as np
from scipy.io.wavfile import write
import matplotlib.pyplot as plt


class NoiseReducer:

    def __init__(self):
        self.noiseConstant = 0.0000001
        self.noisePower = 5
        self.improvementCoefficient = 20

    def readFile(self, file):
        amplitudes, sampleRate = librosa.load(file)
        return amplitudes, sampleRate

    def addNoise(self, file):
        y, sr = self.readFile(file)
        for i in range(len(y)):
            y[i] = y[i] + self.noisePower*self.noiseConstant*np.random.uniform(0,len(y))
        write('TestWithNoise.wav', sr, y)

    def spectralSubstractionAlgo(self, file):
        signalWithNoise, sampleRate = librosa.load(file, sr=None, mono=True)
        signalFourier = librosa.stft(signalWithNoise)
        positiveSignalFourier = np.abs(signalFourier)
        angle = np.angle(signalFourier)
        complexForm = np.exp(1.0j * angle)
        for i in range(len(positiveSignalFourier)):
            positiveSignalFourier[i] -= self.improvementCoefficient*\
                                        self.noisePower*\
                                        self.noiseConstant*\
                                        len(signalWithNoise)/2
        finalFourier = positiveSignalFourier * complexForm
        signalWithoutNoise = librosa.istft(finalFourier)
        write('TestWithoutNoise.wav', sampleRate, signalWithoutNoise)

    def runAlgo(self):
        self.addNoise('Test.wav')
        self.spectralSubstractionAlgo('TestWithNoise.wav')
        # y, sr = self.readFile('TestWithNoise.wav')
        # plt.figure(1)
        # plt.plot(y)
        # y, sr = self.readFile('TestWithoutNoise.wav')
        # plt.figure(2)
        # plt.plot(y)
        # plt.show()
