from moviepy.editor import VideoFileClip, concatenate_videoclips
import random

class VisualEngine:
    def __init__(self):
        pass

    def smart_beat_sync(self, raw_video_paths, beat_times, target_duration):
        """Cắt ghép video thô dựa trên nhịp điệu bài nhạc"""
        print("Syncing visuals to beats...")
        
        # Load tất cả video thô
        raw_clips = [VideoFileClip(p) for p in raw_video_paths]
        synced_clips = []
        
        current_time = 0
        clip_index = 0
        
        # Duyệt qua các nhịp beat để cắt clip
        for i in range(len(beat_times) - 1):
            if current_time >= target_duration:
                break
                
            beat_duration = beat_times[i+1] - beat_times[i]
            source_clip = raw_clips[clip_index % len(raw_clips)]
            
            # Chọn một đoạn ngẫu nhiên trong clip thô (tránh dính đoạn lỗi)
            max_start = max(0, source_clip.duration - beat_duration)
            start_t = random.uniform(0, max_start)
            
            # Cắt đúng bằng thời lượng của 1 nhịp (Beat)
            cut_clip = source_clip.subclip(start_t, start_t + beat_duration)
            
            # Thêm Speed Ramping nếu cần tại đây (MoviePy vfx.speedx)
            
            synced_clips.append(cut_clip)
            current_time += beat_duration
            clip_index += 1
            
        final_visual = concatenate_videoclips(synced_clips, method="compose")
        return final_visual
