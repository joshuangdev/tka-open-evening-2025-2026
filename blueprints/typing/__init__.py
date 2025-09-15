from flask import Blueprint, session, redirect, render_template, url_for, request, jsonify
import os

typing_bp = Blueprint('typing', __name__, template_folder="templates/typing")

@typing_bp.route('/', methods=['GET', 'POST'])
def typing_home():
    return render_template('hellotype.html')

@typing_bp.route("/results", methods=["POST"])
def typing_results():
    wpm = request.form.get("wpm")
    accuracy = request.form.get("accuracy")
    time_taken = request.form.get("time")
    mistakes = request.form.get("mistakes")
    print(time_taken)
    return render_template("results.html",
                           wpm=wpm,
                           accuracy=accuracy,
                           time=time_taken,
                           mistakes=mistakes)

@typing_bp.route('/generate', methods=['GET'])
def generate_text():
    list = request.args.get('collection', default='general', type=str)
    with open(f"{os.getcwd()}/blueprints/typing/data/food.txt", "r") as file:
        text = file.read().split(", ")
    return jsonify({'status': 'success', 'text': text})