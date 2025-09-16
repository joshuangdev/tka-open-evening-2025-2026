import firebase_admin
from firebase_admin import credentials, firestore, auth
from dotenv import load_dotenv
import os, json

load_dotenv()

# Firebase Admin SDK setup
# Initialize Firebase using environment variables
def init_firebase():
    try:
        # Check if running locally with service account file
        if os.path.exists('serviceAccountKey.json'):
            cred = credentials.Certificate('serviceAccountKey.json')
            firebase_admin.initialize_app(cred)
            print("Firebase initialized with local service account")
        else:
            # Production: Use environment variables
            firebase_config_json = os.getenv('FIREBASE_CONFIG')
            if firebase_config_json:
                # Parse JSON string from environment variable
                firebase_config = json.loads(firebase_config_json)
                cred = credentials.Certificate(firebase_config)
                firebase_admin.initialize_app(cred)
                print("Firebase initialized with environment variables")
            else:
                # Alternative: individual environment variables
                firebase_config = {
                    "type": "service_account",
                    "project_id": os.getenv('FIREBASE_PROJECT_ID'),
                    "private_key_id": os.getenv('FIREBASE_PRIVATE_KEY_ID'),
                    "private_key": os.getenv('FIREBASE_PRIVATE_KEY', '').replace('\\n', '\n'),
                    "client_email": os.getenv('FIREBASE_CLIENT_EMAIL'),
                    "client_id": os.getenv('FIREBASE_CLIENT_ID'),
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/{os.getenv('FIREBASE_CLIENT_EMAIL')}"
                }
                
                # Validate required fields
                required_fields = ['project_id', 'private_key', 'client_email']
                if all(firebase_config.get(field) for field in required_fields):
                    cred = credentials.Certificate(firebase_config)
                    firebase_admin.initialize_app(cred)
                    print("Firebase initialized with individual environment variables")
                else:
                    raise ValueError("Missing required Firebase environment variables")
        
        return firestore.client()
        
    except Exception as e:
        print(f"Firebase initialization error: {e}")
        return None

# Initialize Firebase
db = init_firebase()