# Flask App Routing

from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "<h1>Welcome to Flask<h1>"


@app.route("/index",methods=["GET"])
def index():
    return "<h1>Welcome to Index Page<h2>"


@app.route("/success/<int:score>")
def success(score):
    if score >= 35:
        return "You have passed with " + str(score)
    else:
        return "you are failed with " + str(score)


@app.route("/fail/<int:score>")
def fail(score):
    return "You are failed in exam with " + str(score)


@app.route('/form',methods=["GET","POST"])
def form():
    if request.method=="GET":
        return render_template("form.html")
    else:
        maths=float(request.form["maths"])
        science=float(request.form["science"])
        history=float(request.form["history"])

        avg=(maths+science+history)/3
        if avg >= 35:
            res="success"
        else:
            res="fail"
        return redirect(url_for(res,score=avg))

        # return render_template("form.html", score=avg)


@app.route('/api', methods=['POST'])
def calculate():
    data = request.get_json()
    val_a = float(dict(data)["a"])
    val_b = float(dict(data)["b"])
    return jsonify(val_a+val_b)


if __name__ == '__main__':
    app.run(debug=True)