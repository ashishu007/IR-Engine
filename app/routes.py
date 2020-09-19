from app import app
from flask import render_template, request, jsonify
from app.engine.inv_ind import get_inv_ind

# Show the input form
@app.route('/')
def hello_world():
    inv_ind, docs = get_inv_ind()
    return render_template("index.html", data=inv_ind, docs=docs)

@app.route('/result', methods=["GET", "POST"])
def send_result():
    if request.method == 'POST':
        form_result = request.form
        form_r = form_result.to_dict(flat=False)
        print(form_r)
    # docs = retrieved_docs(form_r["query"])
    return render_template("display.html", docs=form_r["query"])