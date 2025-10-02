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
}


@app.route("/", methods=["GET", "POST"])
def index():
    info = None
    if request.method == "POST":
        action = request.form.get("action")
        url = request.form["url"]
        if action == "convert":
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                # sla info op in session
                session["info"] = {
                    "id": info.get("id"),
                    "title": info.get("title"),
                    "thumbnail": info.get("thumbnail"),
                    "url": url,
                }
                return render_template("home.html", info=session["info"])
            except Exception as e:
                flash(f"Fout: {str(e)}", "danger")
                return redirect("/")
        elif action == "download":
            # haal info uit session
            info = session.get("info")
            if not info:
                flash("Geen video-informatie gevonden. Probeer opnieuw.", "danger")
                return redirect("/")
            try:
                downloads_dir = os.path.join(
                    os.path.dirname(os.path.abspath(__file__)), "downloads"
                )
                if not os.path.exists(downloads_dir):
                    os.makedirs(downloads_dir)
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info_dl = ydl.extract_info(info["url"])
                    ydl.download([info["url"]])
                filename = (
                    ydl.prepare_filename(info_dl)
                    .replace(".webm", ".mp3")
                    .replace(".m4a", ".mp3")
                )
                abs_filename = os.path.abspath(filename)
                if not os.path.exists(abs_filename):
                    flash("Download is mislukt. Bestand niet gevonden.", "danger")
                    session.pop("info", None)  # info wissen bij fout
                    return redirect("/")
                session.pop("info", None)  # info wissen na download
                return send_file(abs_filename, as_attachment=True)
            except Exception as e:
                flash(f"Fout: {str(e)}", "danger")
                session.pop("info", None)  # info wissen bij fout
                return redirect("/")
    else:
        session.pop("info", None)  # info wissen bij GET

    if "info" in session:
        info = session["info"]
    return render_template("home.html", info=info)


if __name__ == "__main__":
    app.run(debug=True)
