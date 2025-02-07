from codecs import oem_encode
from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

path = CAMINHO_AUDIOS
lista_audios = os.listdir(path)


for item in lista_audios: 
    if item.endswith('.mp3') or item.endswith('.wav'):
        full_path = os.path.join(path, item)
        print(full_path)
        audio_file = open(full_path, 'rb')
        transcrição = client.audio.transcriptions.create(
            model = 'whisper-1',
            file = audio_file,
            language = 'pt',
            response_format = 'text'
        )
        with open(f'{item}.txt', 'w', encoding='utf-8') as file:
            file.write(transcrição)
            
