import ollama

# install at https://ollama.com/
# install model at: https://ollama.com/library/gemma3
# pip install ollama

model_name = "gemma3:4b"

def to_genz_slang(input_text):
    
    prompt = (
        "Reword the following using Gen Z slang. Imagine you are a genz tiktoker. "
        "Keep the full meaning, but rephrase it casually with modern slang. "
        "Do NOT summarize or shorten it. Also make sure to NOT lose important info."
        "No intro, no explanation — just the translated version:\n\n"
        "Examples to use as refrences:\n"
        '"I don’t understand this topic." → "bruh topic got me lost ngl"\n'
        '"I’m really excited for the concert!" → "no cap hyped for the concert tn for real"\n'
        '"This assignment is due tomorrow." → "assignment due tmrw rip sleep"\n'
        '"I need to study for my exam." → "gotta cram for this test smh"\n'
        '"Can you help me with this problem?" → "ayo help me out w this lmao"\n'
        '"I’m tired and going to bed." → "im dead tired, boutta crash"\n'
        '"That movie was really good." → "that movie lowkey slapped ngl"\n'
        '"However, this may not be realistic when a city government has limited budget or human resources." → "the city is broke for real"\n\n"'
        f"Now translate this while keeping the full meaning:\n{input_text}"
    )

    
    try:
        response = ollama.generate(model=model_name, prompt=prompt)
        return response['response'].strip()
    except Exception as e:
        print(f"Error during slang translation: {e}")
        return "Error generating slang version."