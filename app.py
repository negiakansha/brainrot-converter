from flask import Flask, render_template, request
from summarizer import summarize_text


app = Flask(__name__)

# The '/' is the root url
@app.route('/')
def home():
  # The first param is the file of the homepage we are rendering
  # The second param is  what the summarized text we are going to show
  return render_template('index.html', summarized_text="")

# Defines a new route /convert that only accepts POST requests.
@app.route('/convert', methods=['POST'])
def convert_text():
  # Extract the text from the form
  input_text = request.form['input_text']
  
  # Temp location to where we are going to do all the 
  summarized_text = summarize_text(input_text) # placeholder
  return render_template('index.html', summarized_text=summarized_text)

if __name__ == '__main__':
  app.run(debug=True)
