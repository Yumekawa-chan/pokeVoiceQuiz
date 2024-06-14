import requests
from bs4 import BeautifulSoup
import os

url = 'http://games255.512.jp/pokewav_DL/index.html'
base_url = 'http://games255.512.jp/pokewav/'

if not os.path.exists('pokemon_sounds'):
    os.makedirs('pokemon_sounds')

response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.content, 'html.parser')

links = soup.find_all('a', href=True)
wav_links = [link for link in links if link['href'].endswith(('.wav', '.mp3'))]

for link in wav_links:
    relative_url = link['href'].split('/')[-1]
    wav_url = base_url + relative_url 
    pokemon_name = link.text.split(':')[1].strip().replace(" ", "_")
    response = requests.get(wav_url)
    
    with open(os.path.join('pokemon_sounds', f'{pokemon_name}.wav' if relative_url.endswith('.wav') else f'{pokemon_name}.mp3'), 'wb') as f:
        f.write(response.content)

print("All .wav and .mp3 files have been downloaded and saved.")
