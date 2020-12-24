import librosa

filename = "C:\\Users\\mwang\\sheet_music_project\\music\\fur_elise\\fur_elise.mp3"
# y, sr = librosa.load(filename)
# filename = librosa.util.example_audio_file()
print(filename)
y, sr = librosa.load(filename)
tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
print('Estimated tempo: {:.2f} beats per minute'.format(tempo))
