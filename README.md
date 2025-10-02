# YouTube to MP3 Converter

<img src="/static/img/logo.png" width="150" alt="Logo">
Met deze webapplicatie kun je eenvoudig YouTube video's omzetten naar MP3 bestanden

## Features

- Plak een YouTube link en converteer deze naar MP3
- Bekijk de titel en thumbnail van de video voor het downloaden

## Vereisten

- Python 3.7 of hoger
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [Flask](https://flask.palletsprojects.com/)
- [ffmpeg](https://ffmpeg.org/) (moet geïnstalleerd zijn en in je PATH staan)

## Installatie

1. **Clone deze repository of download de bestanden**

2. **Installeer de benodigde Python pakketten via requirements.txt:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Installeer ffmpeg:**
   - Windows: Download van [ffmpeg.org](https://ffmpeg.org/download.html) en voeg toe aan je PATH
   - Mac: `brew install ffmpeg`
   - Linux: `sudo apt install ffmpeg`

4. **Start de applicatie:**
   ```bash
   python app.py
   ```

5. **Open je browser en ga naar:**
   ```
   http://localhost:5000
   ```

## Gebruik

1. Plak een YouTube link in het invoerveld
2. Klik op "Convert"
3. Bekijk de video informatie en klik op "Download" om het MP3 bestand te downloaden
