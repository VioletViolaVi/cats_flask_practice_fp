from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug import exceptions

from controllers import cats

app = Flask(__name__)
CORS(app)


@app.route("/")
def welcome():
    return "Welcome to flask"


@app.route("/cats", methods=["GET", "POST"])
def cat():
    # if request.method == "GET":
    #     return jsonify(
    #         {"cats": ["Fluffy", "Bubbles"]}
    #     ), 200
    # elif request.method == "POST":
    #     return "We POST some cats", 201
    fns = {
        "GET": cats.index,
        "POST": cats.create,
    }
    resp, code = fns[request.method](request)
    return jsonify(resp), code


@app.route("/cats/<int:cat_id>", methods=["GET", "PUT", "DELETE"])
def cat_handler(cat_id):
    fns = {
        "GET": cats.show,
        "PUT": cats.update,
        "DELETE": cats.destroy
    }
    resp, code = fns[request.method](request, cat_id)
    return jsonify(resp), code


@app.errorhandler(exceptions.NotFound)
def handle_404(err):
    return jsonify({"message": f"Oops... {err}"}), 404


@app.errorhandler(exceptions.InternalServerError)
def handle_500(err):
    return jsonify({"message": f"It's not you it's us"}, 500)


if __name__ == "__main__":
    app.run(debug=True)
