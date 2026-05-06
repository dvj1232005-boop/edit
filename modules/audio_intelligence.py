import whisper
import librosa
import numpy as np

class AudioAnalyzer:
    def __init__(self, model_size="base"):
        # Chuyển sang "large-v3" trên server có GPU mạnh
        print(f"Loading Whisper model ({model_size})...")
        self.whisper_model = whisper.load_model(model_size)

    def extract_lyrics(self, audio_path):
        """Trích xuất lời bài hát với Word-level timestamps"""
        print("Transcribing audio and aligning timestamps...")
        result = self.whisper_model.transcribe(audio_path, word_timestamps=True)
        
        words_data = []
        for segment in result['segments']:
            for word in segment.get('words', []):
                words_data.append({
                    'text': word['word'],
                    'start': word['start'],
                    'end': word['end']
                })
        return words_data

    def detect_beats(self, audio_path):
        """Phân tích Onset strength và Beats bằng Librosa"""
        print("Analyzing beats and BPM...")
        y, sr = librosa.load(audio_path)
        
        # Lấy tempo và các điểm beat
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        beat_times = librosa.frames_to_time(beat_frames, sr=sr)
        
        # Phân tích năng lượng (Onset strength) để tìm điểm Drop/Build-up
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        
        return {
            "bpm": tempo,
            "beat_times": beat_times,
            "onset_env": onset_env
        }
