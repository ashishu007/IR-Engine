from app import app
from flask import render_template, request, jsonify
from app.engine.inv_ind import get_inv_ind

# Show the input form
@app.route('/')
def hello_world():
    # inv_ind = {"dog": [1, 2, 3], "cat": [2, 4]}
    inv_ind, docs = get_inv_ind()
    # print(inv_ind)
    # print(docs)
    return render_template("index.html", data=inv_ind, docs=docs)

@app.route('/result', methods=["GET", "POST"])
def send_result():
    if request.method == 'POST':
        result = request.form
        r = result.to_dict(flat=False)
        # print(result)
        print(r)
    return jsonify(result)