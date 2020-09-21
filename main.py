from flask import Flask
from flask import render_template, request, jsonify
from engine.inv_ind import get_inv_ind
from engine.retrieval import get_retrieved_docs

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template("default.html")

@app.route('/index', methods=["GET", "POST"])
def index_files():
    if request.method == 'POST':
        form_result = request.form
        form_r = form_result.to_dict(flat=False)
    print(form_r)
    inv_ind, docs = get_inv_ind(corpus=form_r["corpus"][0], do_stem=form_r["stem"][0])
    return render_template("index.html", data=inv_ind, docs=docs)

@app.route('/result', methods=["GET", "POST"])
def send_result():
    if request.method == 'POST':
        form_result = request.form
        form_r = form_result.to_dict(flat=False)
    # print(form_r)
    docs = get_retrieved_docs(form_r["query"][0])
    # print(docs)
    return render_template("display.html", docs=docs, query=form_r["query"][0])

if __name__ == '__main__':
    app.run(reloader=False)