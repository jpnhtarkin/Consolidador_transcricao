import os
from dotenv import load_dotenv
from pydub import AudioSegment
import moviepy.editor as mp
import shutil
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

client = OpenAI()
MAX_SIZE = 25 * 1024 * 1024  # 25 MB

def transcricao_raw(caminho_audio):
    print(f"Iniciando transcrição do áudio: {caminho_audio}")
    nome_do_audio = os.path.splitext(os.path.basename(caminho_audio))[0]
    with open(caminho_audio, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model='whisper-1',
            file=audio_file,
            response_format='text',
        )
    caminho_transcricao = os.path.join(os.getcwd(), 'transcricoes', f'Transcricao raw - {nome_do_audio}.txt')
    with open(caminho_transcricao, 'w') as f:
        f.write(transcript)
    return transcript

def video2audio(caminho_do_video):
    print(f"Convertendo vídeo para áudio: {caminho_do_video}")
    caminho_do_audio = os.path.join(os.getcwd(), 'arquivos')
    caminho_do_backup = os.path.join(os.getcwd(), 'backup')
    os.makedirs(caminho_do_audio, exist_ok=True)
    os.makedirs(caminho_do_backup, exist_ok=True)
    nome_do_audio = os.path.splitext(os.path.basename(caminho_do_video))[0] + '.mp3'
    video = mp.VideoFileClip(caminho_do_video)
    caminho_final_do_audio = os.path.join(caminho_do_audio, nome_do_audio)
    video.audio.write_audiofile(caminho_final_do_audio)
    shutil.move(caminho_do_video, caminho_do_backup)
    return caminho_final_do_audio

def audio_chop(caminho_do_audio):
    if not os.path.exists(caminho_do_audio):
        print(f"Arquivo de áudio não encontrado: {caminho_do_audio}")
        return []
    print(f"Dividindo áudio em partes: {caminho_do_audio}")
    nome_do_audio = os.path.splitext(os.path.basename(caminho_do_audio))[0]
    audio = AudioSegment.from_file(caminho_do_audio,'mp3')
    partes = []
    while len(audio) > MAX_SIZE:
        partes.append(audio[:MAX_SIZE])
        audio = audio[MAX_SIZE:]
    partes.append(audio)
    caminho_das_partes = os.path.join(os.getcwd(), 'arquivos', 'partes')
    os.makedirs(caminho_das_partes, exist_ok=True)
    caminhos_das_partes = []
    for i, parte in enumerate(partes):
        caminho_parte = os.path.join(caminho_das_partes, f"{nome_do_audio}_parte_{i}.mp3")
        parte.export(caminho_parte, format='mp3')
        caminhos_das_partes.append(caminho_parte)
    return caminhos_das_partes

def sorter(caminho_dos_arquivos, caminho_das_partes):
    os.makedirs(caminho_das_partes, exist_ok=True)
    for nome_arquivo in os.listdir(caminho_dos_arquivos):
        caminho_arquivo = os.path.join(caminho_dos_arquivos, nome_arquivo)
        extensao_do_arquivo = os.path.splitext(caminho_arquivo)[1].lower()
        if extensao_do_arquivo in ['.mp4', '.avi']:
            caminho_do_audio = video2audio(caminho_arquivo)
            if os.path.getsize(caminho_do_audio) > MAX_SIZE:
                caminhos_das_partes = audio_chop(caminho_do_audio)
                for caminho_parte in caminhos_das_partes:
                    transcricao_raw(caminho_parte)
            else:
                transcricao_raw(caminho_do_audio)
        elif extensao_do_arquivo in ['.mp3', '.wav']:
            print(f"Processando arquivo de áudio: {caminho_arquivo}")
            if os.path.getsize(caminho_arquivo) > MAX_SIZE:
                caminhos_das_partes = audio_chop(caminho_arquivo)
                for caminho_parte in caminhos_das_partes:
                    transcricao_raw(caminho_parte)
            else:
                transcricao_raw(caminho_arquivo)

def main():
    caminho_arquivos = os.path.join(os.getcwd(), 'arquivos')
    caminho_partes = os.path.join(caminho_arquivos, 'partes')
    sorter(caminho_arquivos, caminho_partes)

if __name__ == '__main__':
    main()
