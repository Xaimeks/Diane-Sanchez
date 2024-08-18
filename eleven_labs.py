from dotenv import load_dotenv
import os
from elevenlabs.client import ElevenLabs
from elevenlabs import play

load_dotenv()
api_key = os.getenv('ELEVEN_LABS_API_KEY')

def eleven_labs_tts(text):

  client = ElevenLabs(
    api_key=api_key,
  )

  audio_generator = client.generate(
    text=text,
    voice="Rachel",
    model="eleven_multilingual_v2"
  )
  
  audio = b"".join(audio_generator)

  output_file = "voice.mp3"
  with open(output_file, 'wb') as file:
    file.write(audio)
    