from transformers import pipeline
import torch

# Check if GPU is available
device = 0 if torch.cuda.is_available() else -1  


# init the summarization model
# if the GPU is avaiable it uses that else the cpu
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=device)
    

# Splits text into chunks of about max_words words each.
def chunk_text(text, max_words=400):
    words = text.split()
    chunks = []
    
    # Loop over each word in the list words 
    for i in range(0, len(words), max_words):
        # Keep looping and adding each word to a string to store in the chunk list
        # After reaching 400 words a new chunk is started
        chunks.append(" ".join(words[i:i + max_words]))

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
        text_chunks = chunk_text(input_text, max_words=400)

        # Summarize each chunk
        summarized_chunks = []
        for chunk in text_chunks:
            chunk_word_count = len(chunk.split())
            max_len = chunk_word_count  # Set max length as the length of the chunk being summarized
            
            # The min length is half of the word count of the 
            # text that is being summarized
            min_summary_length = max(int(chunk_word_count * 1 / 2), 50)  # Ensure at least 50 words

            # Adjust max_length and min_length 
            # Then put all the summarized chunks into a list 
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
