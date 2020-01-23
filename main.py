from genderEstimator import GenderEstimator
from noiseReducer import NoiseReducer

# Phase 1
genderEstimator = GenderEstimator()
vector = genderEstimator.processFolder('voices')
for file in vector:
    print(file, ':', vector[file])

# Phase 2
noiseReducer = NoiseReducer()
noiseReducer.runAlgo()
