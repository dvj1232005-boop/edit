import os
from moviepy.editor import AudioFileClip
from modules.audio_intelligence import AudioAnalyzer
from modules.visual_engine import VisualEngine
from modules.vfx_typography import VFXProcessor

def process_automated_pipeline(raw_video_dir, audio_path, output_path):
    print("=== BẮT ĐẦU PIPELINE AI PRO-VIDEO EDITING ===")
    
    # 1. Chuẩn bị đầu vào
    raw_videos = [os.path.join(raw_video_dir, f) for f in os.listdir(raw_video_dir) if f.endswith(('.mp4', '.mov'))]
    audio_clip = AudioFileClip(audio_path)
    target_duration = audio_clip.duration
    
    # 2. Khởi tạo Modules
    audio_ai = AudioAnalyzer(model_size="base") # Dùng large-v3 cho chuẩn Pro
    visual_ai = VisualEngine()
    vfx_ai = VFXProcessor()
    
    # 3. Phân tích Âm thanh
    print("\n[1/4] Đang phân tích AI Âm thanh...")
    lyrics_data = audio_ai.extract_lyrics(audio_path)
    beat_data = audio_ai.detect_beats(audio_path)
    
    # 4. Biên tập hình ảnh (Beat-Sync)
    print("\n[2/4] Đang thực hiện Smart Beat-Sync...")
    edited_video = visual_ai.smart_beat_sync(
        raw_videos, 
        beat_data['beat_times'], 
        target_duration
    )
    
    # 5. Xử lý VFX & Typography
    print("\n[3/4] Đang tạo Kinetic Typography...")
    text_clips = vfx_ai.generate_kinetic_typography(lyrics_data, edited_video.size)
    
    # Merge Text và Video (Cơ sở cho Depth-Aware Text)
    final_video = vfx_ai.apply_depth_aware_text(edited_video, text_clips)
    
    # Thêm nhạc nền
    final_video = final_video.set_audio(audio_clip)
    
    # 6. Render Output
    print("\n[4/4] Đang xuất file (Rendering)...")
    final_video.write_videofile(
        output_path,
        fps=60, # Chuẩn mượt cho Reels/TikTok
        codec="libx264",
        audio_codec="aac",
        preset="fast",
        threads=8 # Tối ưu CPU
    )
    
    print("\n=== HOÀN THÀNH PIPELINE ===")
    print(f"Video đã lưu tại: {output_path}")

if __name__ == "__main__":
    # Thay đổi đường dẫn theo máy của bạn
    RAW_DIR = "./inputs/raw_videos"
    AUDIO_FILE = "./inputs/music/target_audio.mp3"
    OUTPUT_FILE = "./outputs/final_master.mp4"
    
    # Tạo thư mục nếu chưa có
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(AUDIO_FILE), exist_ok=True)
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    # process_automated_pipeline(RAW_DIR, AUDIO_FILE, OUTPUT_FILE)
