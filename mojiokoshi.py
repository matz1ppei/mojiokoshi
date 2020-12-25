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

        for splited_file in split_file(wav_file):
            with sr.AudioFile(str(splited_file)) as source:
                audio = r.record(source)
                result = r.recognize_google(audio, language='ja_JP')
                save(m4a_file.stem, result)
        print(f'文字起こしを終了します', flush=True)

def convert_m4a_to_wav(m4a_file):
    print('.m4aファイルを変換しています', flush=True)
    wav_file = str(m4a_file.with_suffix('.wav'))
    command = 'ffmpeg -i ' + str(m4a_file) + ' ' + wav_file
    subprocess.run(command, shell=True, stdout=PIPE, stderr=PIPE)
    print('.m4aファイルを変換しました：' + wav_file, flush=True)
    return wav_file

def split_file(wav_file):
    output_file = wav_file.replace('.wav', '')
    command = f'ffmpeg -i {wav_file} -f segment -segment_time 300 {output_file}_%03d.wav'
    subprocess.run(command, shell=True, stdout=PIPE, stderr=PIPE)
    print('.wavファイルを分割しました\r\n文字起こしを開始します', flush=True)
    return Path().glob(f'{output_file}_[0-9][0-9][0-9].wav')

def save(file_name, text):
    if not Path(TEXT_DIR).exists():
        Parh(TEXT_DIR).mkdir()

    dt_now = datetime.now().strftime('%Y%m%d%H%M')
    file_name += '_' + dt_now + '.txt'
    file_path = TEXT_DIR + file_name
    text_file = open(file_path, 'a', encoding='utf-8')
    text_file.write(text)
    text_file.close()

if __name__ == "__main__":
    main()