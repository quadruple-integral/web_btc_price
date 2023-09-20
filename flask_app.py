
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template
import price
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    t, p = price.update()
    return render_template("index.html", t = pd.to_datetime(t, unit = 'ms'), p = round(p))

