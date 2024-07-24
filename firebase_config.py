
import firebase_admin
from firebase_admin import credentials, storage

# Inicializa Firebase
def initialize_firebase(json_key_path, storage_bucket):
    if not firebase_admin._apps:
        cred = credentials.Certificate(json_key_path)
        firebase_admin.initialize_app(cred, {'storageBucket': storage_bucket})