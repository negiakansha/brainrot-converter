from gtts import gTTS
from moviepy.editor import AudioFileClip, CompositeVideoClip, VideoFileClip, ImageClip
from PIL import Image, ImageDraw, ImageFont
import os

# Using virtual env for python 3.11.0
# pip install moviepy==1.0.3 
# pip install gTTS
# pip install "Pillow<10"


def create_video(summarized_text):
    # Get absolute path to the static folder
    static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

    # Ensure static folder exists
    os.makedirs(static_dir, exist_ok=True)

    # Paths
    audio_path = os.path.join(static_dir, "audio.mp3")
    video_path = os.path.join(static_dir, "output.mp4")
    background_path = os.path.join(static_dir, "background.mp4")  # move background here or change this

    # --- Convert text to speech ---
    tts = gTTS(summarized_text)
    tts.save(audio_path)

    # --- Load audio and get duration ---
    audio_clip = AudioFileClip(audio_path)
    total_duration = audio_clip.duration

    # --- Prepare text frames ---
    words = summarized_text.split()
    words_per_line = 5
    lines = [' '.join(words[i:i + words_per_line]) for i in range(0, len(words), words_per_line)]
    
    # Estimate timing better
    total_chars = sum(len(line) for line in lines)
    clips = []
    current_time = 0
    video_size = (888, 1570)
    font_path = "arial.ttf"
    
    for line in lines:
        # Better timing estimate
        line_duration = total_duration * (len(line) / total_chars)
    
        img = Image.new('RGBA', video_size, color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype(font_path, 50)
        except:
            font = ImageFont.load_default()
    
        text_w, text_h = draw.textbbox((0, 0), line, font=font)[2:]
        pos_x = (video_size[0] - text_w) // 2
        pos_y = (video_size[1] - text_h) // 2
        draw.text((pos_x, pos_y), line, fill="white", stroke_width=1, stroke_fill="white", font=font)
    
        frame_file = os.path.join(static_dir, f"frame_{len(clips)}.png")
        img.save(frame_file)
    
        clip = (
            ImageClip(frame_file)
            .set_duration(line_duration)
            .set_start(current_time)
            .fadein(0.2)
            .fadeout(0.2)
        )
        clips.append(clip)
        current_time += line_duration

    # --- Load background ---
    background = VideoFileClip(background_path).subclip(0, total_duration).resize(video_size)

    # --- Combine all ---
    final_video = CompositeVideoClip([background, *clips]).set_audio(audio_clip)
    final_video.write_videofile(video_path, fps=15, preset='ultrafast', audio_codec='aac', audio_bitrate='128k')

    # --- Cleanup ---
    for i in range(len(lines)):
        try:
            os.remove(os.path.join(static_dir, f"frame_{i}.png"))
        except FileNotFoundError:
            pass

    print("Static path absolute:", os.path.abspath(video_path))
    print("File exists?", os.path.exists(video_path))
    return True

# Takes about 1:20 to finish rendering