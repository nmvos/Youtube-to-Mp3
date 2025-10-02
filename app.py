import yt_dlp
from flask import Flask, render_template, request, send_file, flash, redirect
import os

app = Flask(__name__)
app.secret_key = "secret"

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': 'downloads/%(title)s.%(ext)s',
    'noplaylist': True,
}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]
        try:
            downloads_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "downloads")
            if not os.path.exists(downloads_dir):
                os.makedirs(downloads_dir)
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url)
                ydl.download([url])
            filename = ydl.prepare_filename(info).replace(".webm", ".mp3").replace(".m4a", ".mp3")
            abs_filename = os.path.abspath(filename)
            if not os.path.exists(abs_filename):
                flash("Download is mislukt.", "danger")
                return redirect("/")
            return send_file(abs_filename, as_attachment=True)
        except Exception as e:
            flash(f"Fout: {str(e)}", "danger")
            return redirect("/")
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
