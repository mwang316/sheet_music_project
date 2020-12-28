# We will be evaluating using the algorithm as described here https://www.music-ir.org/mirex/wiki/2006:Audio_Beat_Tracking.

import librosa

# we will be using beat_tracker evaluate files
filename = "evaluate1.wav"
y, sr = librosa.load(filename)
tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
print('Estimated tempo: {:.2f} beats per minute'.format(tempo))
