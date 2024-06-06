tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
print(tempo, flush=True)
bpm[:] = tempo
