import sys
import speech_recognition as sr
import subprocess
from subprocess import PIPE
from pathlib import Path

AUDIO_DIR = './audio/'
TEXT_DIR = './text/'

def main():
    args = sys.argv

    for m4a_file in Path(AUDIO_DIR).glob('*.m4a'):
        wav_file = convert_m4a_to_wav(m4a_file)

        r = sr.Recognizer()

        with sr.AudioFile(wav_file) as source:
            audio = r.record(source)
            result = r.recognize_google(audio, language='ja_JP')
            save(wav_file.stem, result)

def convert_m4a_to_wav(m4a_file):
    wav_file = str(m4a_file.with_suffix('.wav'))
    command = 'ffmpeg -i ' + str(m4a_file) + ' ' + wav_file
    subprocess.run(command, shell=True, stdout=PIPE, stderr=PIPE)
    return wav_file

def save(file_name, text):
    if not Path(TEXT_DIR).exists():
        Parh(TEXT_DIR).mkdir()

    file_path = TEXT_DIR + file_name + '.txt'
    text_file = open(file_path, 'w', encoding='utf-8')
    text_file.write(text)
    text_file.close()

if __name__ == "__main__":
    main()