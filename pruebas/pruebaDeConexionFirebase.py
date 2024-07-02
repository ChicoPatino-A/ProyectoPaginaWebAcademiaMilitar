import firebase_admin
from firebase_admin import credentials, storage
import os

def initialize_firebase(json_key_path, storage_bucket):
    # Inicializa la app de Firebase
    cred = credentials.Certificate(json_key_path)
    firebase_admin.initialize_app(cred, {
        'storageBucket': storage_bucket
    })

def upload_image(file_path):
    # Obtiene el bucket de almacenamiento
    bucket = storage.bucket()
    # Nombre del archivo que se subirá
    blob = bucket.blob(os.path.basename(file_path))
    # Sube el archivo
    blob.upload_from_filename(file_path)
    # Hace el archivo público
    blob.make_public()
    # Retorna la URL pública del archivo
    return blob.public_url

if __name__ == "__main__":
    json_key_path = 'C://Users//aclog//Desktop//ProyectoFinal//Codigo//pruebas//academiadelogistica-4a432-firebase-adminsdk-j0rgu-442fbffdb6.json'  # Cambia esto a la ruta de tu archivo JSON
    storage_bucket = 'academiadelogistica-4a432.appspot.com'  # Cambia esto al nombre de tu bucket

    initialize_firebase(json_key_path, storage_bucket)

    file_path = 'C://Users//aclog//Desktop//ProyectoFinal//Codigo//static//images//johana.jpg'  # Cambia esto a la ruta de la imagen que deseas subir
    public_url = upload_image(file_path)
    print(f"La imagen se ha subido. URL pública: {public_url}")


