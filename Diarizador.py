from pyannote.audio import Pipeline
from pyannote.audio import Audio
from pyannote.core import Segment
import torch
import shutil
import whisper
import soundfile as sf
import os
import shutil
import tempfile
from openai import OpenAI
from dotenv import load_dotenv
import numpy as np  # Add this import statement

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI()

pipeline = Pipeline.from_pretrained(
    'pyannote/speaker-diarization-3.1',
    use_auth_token='SENHA_PYANOTE',
)

pipeline.to(torch.device('cuda'))

temp_dir = tempfile.mkdtemp()
diretorio = DIRETORIO

files = os.listdir(diretorio)
print(files)

for file in files:
    
    audio_name = file
    print(audio_name)
    audio_file_path = os.path.join(diretorio, audio_name)
    diarization = pipeline(audio_file_path)

    current_speaker = None
    start_time = None
    
    merged_segments = []  # Store merged segments here 



    audio_data, samplerate = sf.read(audio_file_path)

    print('iniciando transcrição')
    
    
    try:
        # Specify the encoding when opening the file
        with open(f'Transcrição Diarizada {audio_name}.txt', 'w', encoding='utf-8') as file:
            for turn, _, speaker in diarization.itertracks(yield_label=True):
                
                print(diarization)
                try:
                    start_time, end_time = turn.start, turn.end
                    
                    if current_speaker == speaker:
                        # Calculate the start and end in samples
                        start_sample = int(start_time * samplerate)
                        end_sample = int(end_time * samplerate)

                        # Extract the segment and append to merged_segments
                        segment = audio_data[start_sample:end_sample]
                        merged_segments.append(segment)
                    else:
                        # Process and merge the segments for the previous speaker
                        if merged_segments:
                            # Combine all merged segments
                            merged_segment = np.concatenate(merged_segments)
                            temp_audio_path = os.path.join(temp_dir, "temp_audio.wav")
                            sf.write(temp_audio_path, merged_segment, samplerate)

                            audio_file = open(temp_audio_path, 'rb')
                            # Transcribe the audio for merged_segments
                            result = client.audio.transcriptions.create(
                                model='whisper-1',
                                file=audio_file,
                                language='pt',
                                response_format='text'
                            )

                            # Write the transcription to the file
                            file.write(f"{current_speaker} : {result}/n")
                            print(f'{current_speaker} : {result}')
                        
                        # Reset merged_segments for the new speaker
                        merged_segments = []

                    current_speaker = speaker

                except Exception as e:
                    print(f"Error processing segment: {str(e)}")
                    continue
    finally:
        try:
            # Clean up the temporary directory
            shutil.rmtree(temp_dir)
        except:
            print("Um audio finalizado")

    # Process and merge any remaining segments for the last speaker
    try:
        if merged_segments:
            merged_segment = np.concatenate(merged_segments)
            temp_audio_path = os.path.join(temp_dir, "temp_audio.wav")
            sf.write(temp_audio_path, merged_segment, samplerate)

            audio_file = open(temp_audio_path, 'rb')
            # Transcribe the audio for merged_segments
            result = client.audio.transcriptions.create(
                    model='whisper-1',
                    file=audio_file,
                    language='pt',
                    response_format='text'
                )

            # Write the transcription to the file
            file.write(f"{current_speaker} : {result}/n")
            print(f'{current_speaker} : {result}')
    except:
        print('Erro em um pedaço do audio')
    # Debug or info
    print(f"Processed {len(diarization)} segments.")
