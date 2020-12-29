import librosa
import numpy as np

# we will be using beat_tracker evaluate files and writing to baseline_output folder
# hacky, but needs to be run from within the baseline_output folder. TODO: maybe fix if have time
for i in range(1, 7):
    filename = f'../evaluate/evaluate{i}.wav'
    y, sr = librosa.load(filename)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr, units='time')
    with open(f'baseline_output/output{i}.txt', 'w') as f:
        f.write('\t'.join(beat_frames.astype(str)))
        print(f'beat track for file {i}: {np.array2string(beat_frames)[1:-1]}')
