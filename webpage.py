from flask import Flask, render_template, jsonify, request
import make_plots
import glob
import os
import pandas as pd
import numpy  as np
import json 

df = make_plots.generate_dataframe()

app = Flask(__name__)

@app.route("/")
def index():
    df_summary = make_plots.summarize(df)
    html = render_template("table.html", data = df_summary.to_json(orient='records'))
    print(html)
    return html




@app.route("/summary")
def data_summary():
    return "You can extend this to summarize your data."

@app.route("/query")
def query_example():
    uuids = []
    for i in range(5):
        if request.args.get(f"uuid{i}"):
            uuids.append(request.args.get(f"uuid{i}"))

    df_summary = make_plots.summarize(df)

    html_tmp = {}
    html_tmp['comparison']={
        'text':"",
        'json':make_plots.timeseries(df[df.uuid.isin(uuids)]).to_json() 
        }
        
    html = render_template("plot.html", charts = html_tmp)
    print(html)
    return html


if __name__ == "__main__":
    app.run(debug=True)
