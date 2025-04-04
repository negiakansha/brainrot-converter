from transformers import pipeline
import torch

# Check if GPU is available
device = 0 if torch.cuda.is_available() else -1  

# init the summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=device)

def chunk_text(text, max_tokens=400):
    """
    Splits text into chunks of approximately max_tokens words each.
    """
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), max_tokens):
        chunks.append(" ".join(words[i:i + max_tokens]))

    return chunks

def summarize_text(input_text):
    if not input_text.strip():
        return "No text provided to summarize."
    
    input_word_count = len(input_text.split())
    
    # If the input is shorter than 50 words
    # Return it with this message
    if input_word_count < 50:
        return f"The input text is too short to summarize. Original text: {input_text}"
    
    try:
        # Break up long text into 400-word chunks
        text_chunks = chunk_text(input_text, max_tokens=500)

        # Summarize each chunk
        summarized_chunks = []
        for chunk in text_chunks:
            chunk_word_count = len(chunk.split())
            max_len = chunk_word_count  # Set max length as the length of the chunk being summarized
            
            # The min length is half of the word count of the 
            # text that is being summarized
            min_summary_length = max(int(chunk_word_count * 1 / 2), 50)  # Ensure at least 50 words

            # Adjust max_length and min_length 
            summary = summarizer(chunk, max_length=max_len, min_length=min_summary_length, do_sample=False)
            summarized_chunks.append(summary[0]['summary_text'])

        # Combine summarized chunks into final summary
        combined_summary = " ".join(summarized_chunks)

        
        return combined_summary
    
    except Exception as e:
        error_message = str(e).lower()
        if "token indices sequence length is longer" in error_message or "maximum" in error_message:
            return "Error: The text is too long to summarize. Please shorten your input."
        return "An error occurred while summarizing. Please try again."
