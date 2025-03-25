from transformers import pipeline
import torch

# Check if GPU is available
device = 0 if torch.cuda.is_available() else -1  

# Initialize the summarization model
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", device=device)

def summarize_text(input_text):
    if not input_text.strip():  # Check if input is empty
        return "No text provided to summarize."
    
    try:
        # Generate summary
        summary = summarizer(input_text, max_length=80, min_length=30, do_sample=False)
        return summary[0]['summary_text']  # Return only the summary text
    
    except Exception as e:  # Catch any error
        error_message = str(e).lower()
        if "Token indicies sequence length is longer" in error_message or "maximum" in error_message:
            return "Error: The text is too long to summarize. Please shorten your input."
        return "An error occurred while summarizing. Please try again."
