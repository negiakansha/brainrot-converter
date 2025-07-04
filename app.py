from flask import Flask, render_template, request
from summarizer import summarize_text
from text_video import create_video
from gemma import to_genz_slang
import threading
import time
import os

app = Flask(__name__, static_folder='static', template_folder='templates')

# The '/' is the root url
@app.route('/')
def home():
  # The first param is the file of the homepage we are rendering
  # The second param is what the summarized text we are going to show
  return render_template('index.html')


@app.route('/convert', methods=['POST'])
def convert_text():
    # Check for and remove existing files
    audio_path = os.path.join(app.static_folder, 'audio.mp3')
    video_path = os.path.join(app.static_folder, 'output.mp4')
    
    # Delete existing files if they exist
    if os.path.exists(audio_path):
        os.remove(audio_path)
        print(f"Deleted existing {audio_path}")
        
    if os.path.exists(video_path):
        os.remove(video_path)
        print(f"Deleted existing {video_path}")
    
    input_text = request.form['input_text']
    
    # Step 1: Summarize the text
    summarized_text = summarize_text(input_text)
    print("Summarized text:\n ", summarized_text)
    
    # Step 2: Convert to Gen Z slang 
    # Using gemma:4b
    slang_text = to_genz_slang(summarized_text)
    print("Slang text: \n", slang_text)
    # Step 3: Generate video from slang
    # Create the audio
    # Create images of the subtitles
    # Combine both to a pre determined video
    thread = threading.Thread(target=create_video, args=(slang_text,))
    thread.start()

    return render_template("video.html")

@app.route('/check_video')
def check_video():
    video_path = os.path.join(app.static_folder, 'output.mp4')

    # Set a timeout limit of 15 sec to wait for the video to be ready
    timeout = 15
    start_time = time.time()

    # This checks the storage size
    # Each check would see if the storage size has change, and
    # if it doesn't change after 3 checks then the video is ready
    last_size = 0
    stable_checks = 0
    max_stable_checks = 3

    # Keep checking the file until the timeout period is reached
    while time.time() - start_time < timeout:
        if os.path.exists(video_path):
            # This gets the size of the output.mp4 in the static folder
            current_size = os.path.getsize(video_path)
            
            # This then checks the size in comparison to the last check
            # It needs to be the same 3 times in a row 
            # If it is the same then it returns a json that the file exists
            # If it isn't the same then the check restarts until it hits 3
            if current_size == last_size:
                stable_checks += 1
                if stable_checks >= max_stable_checks:
                    print(f"File exists and is ready: {video_path}")
                    return {'exists': True}  #Return when video is ready
            else:
                stable_checks = 0

            last_size = current_size

        # Wait an extra 2 seconds before the next check
        time.sleep(2)  

    print("Video is still being created or an error occurred.")
    return {'exists': False}

    
@app.route('/watch')
def watch_video():
    return render_template('watch.html')
    
    
if __name__ == '__main__':
  app.run(debug=True)
