from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json
from models import Base, Movie
import os

app = Flask(__name__)
CORS(app)  # Habilitar CORS

# Configuración de la base de datos
DATABASE_URL = "postgresql://postgres:postgres@db:5432/movies"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

@app.route('/upload', methods=['POST'])
def upload_data():
    # Verificar que los archivos estén en la solicitud
    if 'json' not in request.files or 'video' not in request.files:
        return jsonify({'error': 'Se requieren tanto el JSON como el archivo de video'}), 400

    # Obtener el archivo JSON y el video
    json_file = request.files['json']
    video_file = request.files['video']

    # Leer el contenido del archivo JSON y convertirlo a un diccionario
    try:
        json_data = json.loads(json_file.read().decode('utf-8'))
    except Exception as e:
        return jsonify({'error': f'Error al procesar el JSON: {str(e)}'}), 400

    # Guardar los datos en la base de datos
    session = Session()
    movie = Movie(data=json.dumps(json_data))  # Guardar el JSON como un string
    session.add(movie)
    session.commit()

    # Guardar el video localmente
    video_path = f"/tmp/{movie.id}.mp4"
    video_file.save(video_path)
    
    return jsonify({'message': 'Datos y video subidos correctamente'}), 201

@app.route('/movies', methods=['GET'])
def get_movies():
    session = Session()
    movies = session.query(Movie).all()
    result = [{'id': movie.id, 'data': json.loads(movie.data)} for movie in movies]
    return jsonify(result)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9000)
