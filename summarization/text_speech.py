import os
import shutil
from gtts import gTTS
from deep_translator import GoogleTranslator

class TextToSpeechConverter:
    def __init__(self, output_directory="audio_outputs"):
        self.output_directory = output_directory
        
        # Remove existing directory and create a fresh one
        if os.path.exists(self.output_directory):
            shutil.rmtree(self.output_directory)
        
        # Create a new, empty directory
        os.makedirs(self.output_directory)

    def convert_english_to_hindi_audio(self, english_text, filename=None):
        """
        Translates the given English text to Hindi, converts it to audio, and saves it as an MP3 file.

        Args:
            english_text (str): The English text to convert to audio.
            filename (str, optional): The desired filename for the audio output. 
                                      If None, generates a default filename.
        
        Returns:
            str or None: Path to the saved audio file, or None if an error occurs.
        """
        try:
            # Generate a default filename if not provided
            if filename is None:
                filename = f"news_coverage.mp3"
            
            # Translate English to Hindi using deep_translator
            hindi_text = GoogleTranslator(source='auto', target='hi').translate(english_text)

            # Convert Hindi text to audio
            tts = gTTS(text=hindi_text, lang='hi')
            filepath = os.path.join(self.output_directory, filename)
            tts.save(filepath)
            
            print(f"English text: {english_text}")
            print(f"Hindi translation: {hindi_text}")
            print(f"Audio saved to: {filepath}")
            return filepath
        except Exception as e:
            print(f"Error during audio conversion: {e}")
            return None