import openai
import text_audio


openai.api_key = "your_API_key"

model_engine = "text-davinci-003"

prompt = text_audio.speech_to_text()
tmp = 0.5

completion = openai.Completion.create(
    engine=model_engine,
    prompt=prompt,
    max_tokens=1024,
    n=1,
    stop=None,
    temperature=tmp,
)

response = completion.choices[0].text
text_audio.text_to_speech(response)
