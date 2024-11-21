from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Movie

app = Flask(__name__)
CORS(app)  # Habilitar CORS

# Configuración de la base de datos
DATABASE_URL = "postgresql://postgres:postgres@db:5432/movies"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

@app.route('/upload', methods=['POST'])
def upload_data():
    if 'file' not in request.files or 'json' not in request.form:
        return jsonify({'error': 'JSON y archivo son requeridos'}), 400
    
    json_data = request.form['json']
    video_file = request.files['file']

    # Guardar datos en la base de datos
    session = Session()
    movie = Movie(data=json_data)
    session.add(movie)
    session.commit()

    # Guardar archivo localmente
    video_file.save(f"/tmp/{movie.id}.mp4")
    
    return jsonify({'message': 'Datos y video subidos correctamente'}), 201

@app.route('/movies', methods=['GET'])
def get_movies():
    session = Session()
    movies = session.query(Movie).all()
    result = [{'id': movie.id, 'data': movie.data} for movie in movies]
    return jsonify(result)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9000)
