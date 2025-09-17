from flask import Blueprint, session, redirect, render_template, url_for, request, jsonify

main_bp = Blueprint('main', __name__, template_folder="templates/main")

@main_bp.route('/')
def home():
    return render_template('home.html')

@main_bp.route("/onboarding")
def onboarding():
    if request.args.get("mode"):
        return render_template("onboarding_advanced.html", mode=request.args.get("mode"))
    return render_template("onboarding.html")

@main_bp.route("/contents")
def contents():
    return render_template("contents.html")

@main_bp.route("/manual")
def manual():
    return render_template("manual.html")

@main_bp.route('/catchthefruit')
def catchthefruit():
    return render_template('catchthefruit.html')