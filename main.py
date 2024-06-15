import os
import random
from pydub import AudioSegment
from pydub.playback import play as play_mp3
import simpleaudio as sa
from time import sleep
import unicodedata

def explanation_session():
    print("ポケモン鳴き声クイズへようこそ！")
    sleep(1.5)
    print("このゲームでは、ランダムに選ばれたポケモンの鳴き声を聞いて、そのポケモンの名前を当てるクイズを行います。")
    sleep(1.5)
    print("出題範囲は、第1世代から第5世代までのポケモンです。")
    sleep(1.5)
    print("1つのポケモンに対して、2回までのチャンスがあります。")
    sleep(1.5)
    print("ポケモンの名前は、カタカナorひらがなで入力してください。")
    sleep(1.5)
    print("それでは、ゲームを始めましょう！")
    sleep(1.5)

def get_random_sounds(directory, num_files=10):
    files = [file for file in os.listdir(directory) if file.endswith(('.wav', '.mp3'))]
    random_files = random.sample(files, num_files)
    return random_files

def play_sound(file_path):
    if file_path.endswith('.wav'):
        wave_obj = sa.WaveObject.from_wave_file(file_path)
        play_obj = wave_obj.play()
        play_obj.wait_done()
    else:
        sound = AudioSegment.from_file(file_path)
        play_mp3(sound)

def katakana_to_hiragana(text):
    return ''.join(chr(ord(char) - ord('ァ') + ord('ぁ')) if 'ァ' <= char <= 'ヶ' else char for char in text)

def normalize_text(text):
    text = unicodedata.normalize('NFKC', text)
    text = katakana_to_hiragana(text)
    return text

def play_game():
    explanation_session()
    sound_directory = 'pokemon_sounds'
    sounds = get_random_sounds(sound_directory)
    score = 0

    for sound_file in sounds:
        print("鳴き声を聞いて、ポケモンの名前を当ててください。")
        sleep(1.5)
        play_sound(os.path.join(sound_directory, sound_file))
        
        for attempt in range(2):
            guess = input(f"{attempt + 1}/2 回目のチャレンジ: あなたの答え: ").strip()
            correct_name = os.path.splitext(sound_file)[0]
            if normalize_text(guess) == normalize_text(correct_name):
                print("正解！")
                score += 1
                break
            else:
                print("不正解！")
        
        print(f"正解は: {correct_name} でした。\n")
    
    print(f"あなたの総得点は 100 点中 {score * 10} 点です。")

if __name__ == "__main__":
    play_game()
