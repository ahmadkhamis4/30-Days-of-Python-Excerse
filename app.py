import os
import re
import secrets
from collections import Counter

from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0


@app.route("/")
def home():
    return render_template(
        "home.html",
        techs=["HTML", "CSS", "Flask", "Python"],
        name="30 Days Of Python Programming",
        title="Home",
    )


@app.route("/about")
def about():
    return render_template(
        "about.html",
        name="30 Days Of Python Programming",
        title="About Us",
    )


@app.route("/post", methods=["GET", "POST"])
def post():
    if request.method == "GET":
        return render_template("post.html", title="Text Analyzer")

    content = request.form.get("content", "").strip()
    if not content:
        return render_template(
            "post.html",
            title="Text Analyzer",
            error="Enter some text to analyze.",
        ), 400

    words = re.findall(r"\b[\w'-]+\b", content.casefold())
    counts = Counter(words)
    session["analysis"] = {
        "word_count": len(words),
        "character_count": len(content),
        "unique_word_count": len(counts),
        "frequent_words": [
            {"word": word, "count": count}
            for word, count in counts.most_common(10)
        ],
    }
    return redirect(url_for("result"))


@app.route("/result")
def result():
    analysis = session.pop("analysis", None)
    if analysis is None:
        return redirect(url_for("post"))
    return render_template("result.html", title="Analysis Results", analysis=analysis)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG") == "1"
    app.run(debug=debug, host="0.0.0.0", port=port)
