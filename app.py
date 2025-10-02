import yt_dlp
from flask import Flask, render_template, request, send_file, flash, redirect, session
import os

app = Flask(__name__)
app.secret_key = "secret"

ydl_opts = {
    "format": "bestaudio/best",
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }
    ],
    "outtmpl": "downloads/%(title)s.%(ext)s",
    "noplaylist": True,
    "cachedir": False,
    "quiet": True,
    "extractaudio": True,
}


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]
        action = request.form.get("action")
        try:
            downloads_dir = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "downloads"
            )
            if not os.path.exists(downloads_dir):
                os.makedirs(downloads_dir)
            if action == "convert":
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                session["video_info"] = {
                    "id": info.get("id"),
                    "title": info.get("title"),
                    "thumbnail": info.get("thumbnail"),
                    "url": url,
                    "ext": info.get("ext", "webm"),
                }
                return render_template("home.html", info=info)
            elif action == "download":
                info = session.get("video_info")
                if not info:
                    flash("Geen video-informatie gevonden. Probeer opnieuw.", "danger")
                    return redirect("/")
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([info["url"]])
                    filename = os.path.join("downloads", f"{info['title']}.mp3")
                    abs_filename = os.path.abspath(filename)
                if not os.path.exists(abs_filename):
                    flash("Download is mislukt.", "danger")
                    return redirect("/")
                response = send_file(abs_filename, as_attachment=True)
                try:
                    os.remove(abs_filename)
                except Exception:
                    pass
                return response
        except Exception as e:
            flash(f"Fout: {str(e)}", "danger")
            return redirect("/")
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
