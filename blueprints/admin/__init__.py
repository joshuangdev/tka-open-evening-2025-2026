from flask import Blueprint, session, redirect, render_template, url_for, request, jsonify
from dotenv import load_dotenv
import os, time
from firebase import db
from functools import wraps

load_dotenv()  
password = os.getenv('ADMIN_PASSWORD')
sessiontimeout = int(os.getenv('SESSION_TIMEOUT', 120))


admin_bp = Blueprint('admin', __name__, template_folder="templates/admin")

def admin_required(json=True):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not session.get('login'):
                return jsonify({"success": False, "error": "Not logged in"}) if json else redirect(url_for('main.home'))
            if session.get('login-time') and (time.time() - session['login-time'] > sessiontimeout):
                session.pop('login', None)
                session.pop('login-time', None)
                return jsonify({"success": False, "error": "Session expired"}) if json else redirect(url_for('main.home'))
            return f(*args, **kwargs)
        return wrapper
    return decorator

@admin_bp.route('/')
def auth():
    return render_template('auth.html')

@admin_bp.route('/ep', methods=['GET', 'POST'])
def endpoint():
    if not session.get('login') and request.method == 'GET':
        return redirect(url_for('main.home'))
    else:
        if request.method == 'POST':
            if request.headers.get('password') == password:
                session['login'] = True
                session['login-time'] = time.time()
                return jsonify({"redirect": url_for('admin.dash')})
            else:
                return jsonify({"redirect": url_for('main.home')})
        else:
            if session.get('login'):
                return jsonify({"redirect": url_for('admin.dash')})
            else:
                return jsonify({"redirect": url_for('main.home')})
            
@admin_bp.route('/extend-session', methods=['POST'])
@admin_required(json=True)
def extend_session():
    session['login-time'] = time.time()
    return jsonify({"success": True})
            
@admin_bp.route('/dash')
@admin_required(json=True)
def dash():
    typing = db.collection('typing').get()
    typing_advanced = db.collection('typing advanced').get()
    data = {
        "typing": [doc.to_dict() | {"id": doc.id} for doc in typing],
        "typing_advanced": [doc.to_dict() | {"id": doc.id} for doc in typing_advanced]
    }
    return render_template('dash.html', data=data)

@admin_bp.route('/pop')
def pop():
    session.pop('login', None)
    return redirect(url_for('main.home'))

@admin_bp.route('/delete/<collection>/<doc_id>', methods=['POST'])
@admin_required(json=True)
def delete_doc(collection, doc_id):
    db.collection(collection).document(doc_id).delete()
    return jsonify({"success": True})

@admin_bp.route('/update/<collection>/<doc_id>', methods=['POST'])
@admin_required(json=True)
def update_doc(collection, doc_id):
    content = request.json
    db.collection(collection).document(doc_id).update(content)
    return jsonify({"success": True})

@admin_bp.route('/add/<collection>', methods=['POST'])
@admin_required(json=True)
def add_doc(collection):
    content = request.json
    db.collection(collection).add(content)
    return jsonify({"success": True})


