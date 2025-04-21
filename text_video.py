from gtts import gTTS
from moviepy.editor import AudioFileClip, CompositeVideoClip, VideoFileClip, ImageClip
from PIL import Image, ImageDraw, ImageFont
import os

# Using virtual env for python 3.11.0
# pip install moviepy==1.0.3 
# pip install gTTS
# pip install "Pillow<10"

def create_video(summarized_text):
    # ---- Step 1: Define your text ----
    # The text is 121 words long
    text = summarized_text

    # ---- Step 2: Convert text to speech ----
    tts = gTTS(text)
    tts.save("audio.mp3")

    # ---- Step 3: Load audio and get duration ----
    audio_clip = AudioFileClip("audio.mp3")
    total_duration = audio_clip.duration

    # ---- Step 4: Split text into chunks (e.g., 5 words per line) ----
    words = text.split()
    words_per_line = 5
    lines = [' '.join(words[i:i + words_per_line]) for i in range(0, len(words), words_per_line)]
    n_lines = len(lines)
    duration_per_line = total_duration / n_lines

    # ---- Step 5: Generate text images and convert to ImageClips ----
    video_size = (888, 1570)
    clips = []

    # Use a basic font path — change this if you have a different font
    font_path = "arial.ttf"  # Windows usually has it. Else try "DejaVuSans.ttf"

    for i, line in enumerate(lines):
        start_time = i * duration_per_line

        # Create image with text using PIL - transparent background
        img = Image.new('RGBA', video_size, color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype(font_path, 50)
        except:
            font = ImageFont.load_default()

        # Add a semi-transparent black rectangle as background for the text -> Not used
        text_size = draw.textbbox((0, 0), line, font=font)
        text_w = text_size[2] - text_size[0]
        text_h = text_size[3] - text_size[1]
        
        # Position at the center of the screen
        position_x = (video_size[0] - text_w) // 2  # center horizontally
        position_y = (video_size[1] - text_h) // 2  # center vertically
        
        # Draw the text in white
        draw.text((position_x, position_y), line, fill="white", stroke_width = 1, stroke_fill = "white", font=font)

        # Save as temporary file
        frame_filename = f"frame_{i}.png"
        img.save(frame_filename)

        # Create an ImageClip
        clip = ImageClip(frame_filename).set_duration(duration_per_line).set_start(start_time).fadein(0.2).fadeout(0.2)
        clips.append(clip)

    # ---- Step 6: Background clip ----
    background = VideoFileClip("background.mp4").subclip(0, total_duration).resize(video_size)

    # ---- Step 7: Combine everything ----
    video = CompositeVideoClip([background, *clips]).set_audio(audio_clip)

    # ---- Step 8: Export video ----
    video.write_videofile(
        "output.mp4", 
        fps=15,
        preset='ultrafast',  # Faster encoding
        audio_codec='aac',  # Efficient audio codec
        audio_bitrate='128k'  # Reasonable audio quality
    )

    # ---- Step 9: Clean up images ----
    for i in range(n_lines):
        os.remove(f"frame_{i}.png")

    # return True because video has been generated
    return True

# Takes about 1:20 to finish rendering