import sys
import speech_recognition as sr
import subprocess
from subprocess import PIPE
from datetime import datetime
from pathlib import Path

AUDIO_DIR = './audio/'
TEXT_DIR = './text/'

def main():
    args = sys.argv

    for m4a_file in Path(AUDIO_DIR).glob('*.m4a'):
        wav_file = convert_m4a_to_wav(m4a_file)

        r = sr.Recognizer()

        print('文字起こしを開始します', flush=True)
        with sr.AudioFile(wav_file) as source:
            audio = r.record(source)
            result = r.recognize_google(audio, language='ja_JP')
            save(m4a_file.stem, result)

def convert_m4a_to_wav(m4a_file):
    print('.m4aファイルを変換しています', flush=True)
    wav_file = str(m4a_file.with_suffix('.wav'))
    command = 'ffmpeg -i ' + str(m4a_file) + ' ' + wav_file
    subprocess.run(command, shell=True, stdout=PIPE, stderr=PIPE)
    print('.m4aファイルを変換しました：' + wav_file, flush=True)
    return wav_file

def save(file_name, text):
    if not Path(TEXT_DIR).exists():
        Parh(TEXT_DIR).mkdir()

    dt_now = datetime.now().strftime('%Y%m%d%H%M')
    file_name += '_' + dt_now + '.txt'
    file_path = TEXT_DIR + file_name
    text_file = open(file_path, 'w', encoding='utf-8')
    text_file.write(text)
    text_file.close()
    print(f'文字起こしを終了します：{file_name}', flush=True)

if __name__ == "__main__":
    main()