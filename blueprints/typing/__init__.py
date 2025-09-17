from flask import Blueprint, session, redirect, render_template, url_for, request, jsonify
import os, uuid, random
from firebase import db

typing_bp = Blueprint('typing', __name__, template_folder="templates/typing")

@typing_bp.route('/', methods=['GET', 'POST'])
def typing_home():
    return render_template('hellotype.html', name=request.args.get("name", False))

@typing_bp.route("/submit", methods=["POST"])
def typing_submit():
    identifier = str(uuid.uuid4())
    col = db.collection("typing")
    col.document(identifier).set({
        "name": request.headers.get("name", "Anonymous"),
        "wpm": request.headers.get("wpm"),
        "accuracy": request.headers.get("accuracy"),
        "time": request.headers.get("time"),
        "test": request.headers.get("test"),
        "words": request.headers.get("words")
    })
    return redirect(url_for("typing.typing_results", id=identifier))

@typing_bp.route("/submit_advanced", methods=["POST"])
def typing_advancedsubmit():
    identifier = str(uuid.uuid4())
    col = db.collection("typing advanced")
    col.document(identifier).set({
        "name": request.headers.get("name", "Anonymous"),
        "wpm": request.headers.get("wpm"),
        "accuracy": request.headers.get("accuracy"),
        "time": request.headers.get("time"),
        "test": request.headers.get("test"),
        "words": request.headers.get("words")
    })
    return redirect(url_for("typing.advanced_typing_results", id=identifier))


@typing_bp.route("/results")
def typing_results():
    identifier = request.args.get("id")
    col = db.collection("typing")
    doc_ref = col.document(identifier)
    doc = doc_ref.get()
    if doc.exists:
        data = doc.to_dict()
        return render_template("results.html", **data)
    else:
        return redirect(url_for("home.onboarding"))    
@typing_bp.route("/advanced_results")
def advanced_typing_results():
    identifier = request.args.get("id")
    col = db.collection("typing advanced")
    doc_ref = col.document(identifier)
    doc = doc_ref.get()
    if doc.exists:
        data = doc.to_dict()
        return render_template("advanced_results.html", **data, mode="AdvancedType")
    else:
        return redirect(url_for("home.onboarding"))
@typing_bp.route('/generate', methods=['GET'])
def generate_text():
    collection = request.args.get('collection', default='general', type=str)
    key = {"general": "general.txt", "food": "food.txt"}
    file_path = os.path.join(os.getcwd(), f"blueprints/typing/data/{key.get(collection, 'general.txt')}")

    with open(file_path, "r") as file:
        text = file.read().strip().split(",")  # split by comma only, no space

    text = [t.strip() for t in text]  # clean any accidental whitespace
    random.shuffle(text)  # shuffle in place
    shuffled_text = ",".join(text)  # join with commas, no spaces

    return jsonify({'status': 'success', 'text': shuffled_text})

@typing_bp.route('/generate_advanced', methods=['GET'])
def generate_advanced_text():
    collection = request.args.get('collection', default='general', type=str)
    key = {"tka": "tka.txt"}
    file_path = os.path.join(os.getcwd(), f"blueprints/typing/data/{key.get(collection, 'tka.txt')}")

    with open(file_path, "r") as file:
        text = file.read().splitlines()
    
    print(text)

    return jsonify({'status': 'success', 'text': text[random.randint(0, len(text)-1)]})

@typing_bp.route('/advancedtype')
def advanced_type():
    return render_template('advancedtype.html', name=request.args.get("name", False))

@typing_bp.route('/leaderboard')
def typing_leaderboard():
    col = db.collection("typing")
    docs = col.stream()
    results = []
    for doc in docs:
        if doc.exists:
            data = doc.to_dict()
            results.append(data)
    print(results)
    results = sorted(results, key=lambda x: (-float(x.get("wpm", 0)), -float(x.get("accuracy", 0)), float(x.get("time", float('inf')))))[:10]
    return render_template("leaderboard.html", results=results, mode="HelloType")

@typing_bp.route('/advanced_leaderboard')
def advanced_leaderboard():
    col = db.collection("typing advanced")
    docs = col.stream()
    results = []
    for doc in docs:
        if doc.exists:
            data = doc.to_dict()
            results.append(data)
    print(results)
    results = sorted(results, key=lambda x: (-float(x.get("wpm", 0)), -float(x.get("accuracy", 0)), float(x.get("time", float('inf')))))[:10]
    return render_template("leaderboard.html", results=results)

