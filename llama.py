import ollama

# install at https://ollama.com/
# install model at: https://ollama.com/library/gemma3
# pip install ollama

model_name = "gemma3:4b"

def to_genz_slang(input_text):
    
    prompt = (
        "Reword the following text using Gen Z slang only. "
        "Do not include any explanations, introductions, or definitions. "
        "Only return the translated text. Keep the same meaning and length:\n\n"
        f"{input_text}"
    )


    
    try:
        response = ollama.generate(model=model_name, prompt=prompt)
        return response['response'].strip()
    except Exception as e:
        print(f"Error during slang translation: {e}")
        return "Error generating slang version."