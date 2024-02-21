from flask import Flask, request

import mailgun

app = Flask(__name__)


# email receiving server(have set up in Maligun) - 暂时不需要

@app.route("/income", methods=["GET", "POST"])
def income():
    if request.method == "POST":
        mailgun.on_receive(request.form)  # 需要以表单数据的形式发送请求，而非JSON
    return "ok"


@app.route("/")
def homepage():
    return "Mail Server is Running now..."


app.run(
    host="0.0.0.0",
    port=10234
)
