from moviepy.editor import TextClip, CompositeVideoClip
import numpy as np

class VFXProcessor:
    def __init__(self, font="Arial-Bold", fontsize=70, color='white'):
        self.font = font
        self.fontsize = fontsize
        self.color = color

    def generate_kinetic_typography(self, words_data, video_size):
        """Tạo các TextClip dạng Pop-up/Karaoke đồng bộ với timestamp"""
        text_clips = []
        for word in words_data:
            # Tạo chữ với stroke đen để nổi bật
            txt_clip = TextClip(
                word['text'].strip(),
                fontsize=self.fontsize,
                color=self.color,
                font=self.font,
                stroke_color='black',
                stroke_width=2,
                method='caption',
                size=(video_size[0] * 0.8, None)
            )
            
            # Cài đặt thời gian xuất hiện (Pop-up effect)
            duration = word['end'] - word['start']
            txt_clip = txt_clip.set_start(word['start']).set_duration(duration)
            
            # Căn giữa dưới cùng
            txt_clip = txt_clip.set_position(('center', 'bottom'))
            text_clips.append(txt_clip)
            
        return text_clips

    def apply_depth_aware_text(self, bg_video, text_clips, subject_mask_func=None):
        """
        Tích hợp Depth-Aware Text. 
        subject_mask_func: Hàm AI (như YOLO/Segment-Anything) để tách lớp người.
        """
        # Nếu chưa có AI tách nền, render text nổi bình thường (Phía trên video)
        if not subject_mask_func:
            return CompositeVideoClip([bg_video] + text_clips)
            
        # TODO cho phiên bản nâng cao:
        # 1. Tách bg_video thành: Background Layer và Subject Layer
        # 2. Layering: Background -> Text -> Subject
        pass
