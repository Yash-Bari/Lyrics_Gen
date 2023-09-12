# Import necessary libraries
import streamlit as st
import openai
from gtts import gTTS
from deep_translator import GoogleTranslator

# Set your OpenAI API key
openai.api_key = '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'

# Create a Streamlit web app
st.title("🎵 Poem and Song Lyrics Generator with Translator 🌍📜🎶")

# Add a text input for user prompts
user_prompt = st.text_area("Enter your creative prompt here:")

# Language selection dropdown with user-friendly language names
language_names = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "hi": "Hindi",
    "mr": "Marathi",

}
selected_language = st.selectbox("Select a language for translation:", list(language_names.values()))

# Initialize the translated_lyrics variable
translated_lyrics = ""

# Initialize the generated_lyrics variable
generated_lyrics = ""


# Function to generate lyrics with OpenAI GPT-3
def generate_lyrics_with_openai(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1000  # Increase max_tokens to generate longer text
    )
    generated_text = response.choices[0].text
    return generated_text


# Function to translate lyrics using Deep Translator
def translate_lyrics_with_deep_translator(lyrics, target_language):
    translated_lyrics = GoogleTranslator(source='auto', target=target_language).translate(lyrics)
    return translated_lyrics


# Function to create and play the audio
def play_audio(audio_text, language):
    if audio_text:
        tts = gTTS(text=audio_text, lang=language)
        with st.spinner("Generating audio... 🎧🎶"):
            audio_data = tts.save("temp_audio.mp3")
        audio_file = open("temp_audio.mp3", "rb").read()
        st.audio(audio_file, format="audio/mp3")


# Example of a creative prompt
example_prompt = """
Compose a romantic song about a moonlit night,
where love is in the air and stars are shining bright.
Mention the beauty of the ocean's gentle waves,
and how our love is like a journey on which my heart craves.
"""

# Create a button to generate and translate
if st.button("Generate and Translate"):
    if not user_prompt:
        st.warning("Please enter a creative prompt.")
    else:
        st.info("Generating lyrics and translating... 🎤🌐🎵")

        # Use OpenAI's GPT-3 API to generate lyrics or poem
        generated_lyrics = generate_lyrics_with_openai(user_prompt)

        # Translate the generated lyrics using Deep Translator
        translated_lyrics = translate_lyrics_with_deep_translator(generated_lyrics, list(language_names.keys())[
            list(language_names.values()).index(selected_language)])

# Display the generated and translated lyrics with a creative interface
st.header("Generated Lyrics:")
if generated_lyrics:
    st.markdown(f"📜 **Generated Lyrics** 📜\n\n{generated_lyrics}")
else:
    st.warning("No lyrics generated yet.")

st.header(f"Translated Lyrics (to {selected_language}):")
if translated_lyrics:
    st.markdown(f"🌍 **Translated Lyrics (to {selected_language})** 🌍\n\n{translated_lyrics}")
else:
    st.warning("No lyrics translated yet.")

# Play the audio automatically if translated lyrics are generated
if translated_lyrics:
    play_audio(translated_lyrics, list(language_names.keys())[list(language_names.values()).index(selected_language)])

# Display an example of a creative prompt
st.sidebar.header("Example Prompt:")
st.sidebar.code(example_prompt)