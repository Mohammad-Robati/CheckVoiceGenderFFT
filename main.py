from signalProcessor import SignalProcessor


signalProcessor = SignalProcessor()
vector = signalProcessor.processFolder('voices')
for file in vector:
    print(file, ':', vector[file])


