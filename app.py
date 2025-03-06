from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import smtplib

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reservas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de Reservas
class Reserva(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    docente = db.Column(db.String(100), nullable=False)
    sala = db.Column(db.String(20), nullable=False)
    horario = db.Column(db.String(20), nullable=False)
    carro = db.Column(db.Integer, nullable=False)

# Crear la base de datos
with app.app_context():
    db.create_all()

# Endpoint para evitar error 404 Page not found
@app.route('/')
def index():
    return "Bienvenido a la API de Reservas de Porvenir School - Todo parece funcionar correctamente."

# Endpoint para consultar horarios disponibles
@app.route('/disponibles', methods=['GET'])
def obtener_horarios_disponibles():
    horarios = [f"{h}:00" for h in range(8, 19)]
    reservas = Reserva.query.with_entities(Reserva.horario).all()
    reservados = {r[0] for r in reservas}
    disponibles = [h for h in horarios if h not in reservados]
    return jsonify(disponibles)

# Endpoint para reservar un carro
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configuración de la base de datos SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reservas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de la base de datos
class Reserva(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    docente = db.Column(db.String(100), nullable=False)
    sala = db.Column(db.String(20), nullable=False)
    horario = db.Column(db.String(20), nullable=False)
    carro = db.Column(db.Integer, nullable=False)  # 1 = Básica, 2 = Media

# Crear la base de datos si no existe
with app.app_context():
    db.create_all()

@app.route('/reservar', methods=['POST'])
def reservar():
    data = request.get_json()

    docente = data.get('docente')
    sala = data.get('sala')
    horario = data.get('horario')
    carro = data.get('carro')

    # Validar si el horario ya está tomado para ese carro
    reserva_existente = Reserva.query.filter_by(horario=horario, carro=carro).first()
    
    if reserva_existente:
        return jsonify({"error": f"El carro {carro} ya está reservado en algun horario solicitado. Debe corregir su solicitud."}), 400

    # Si el horario está disponible, se guarda la reserva
    nueva_reserva = Reserva(docente=docente, sala=sala, horario=horario, carro=carro)
    db.session.add(nueva_reserva)
    db.session.commit()

    return jsonify({"mensaje": "Reserva confirmada", "docente": docente, "sala": sala, "horario": horario, "carro": carro}), 201

if __name__ == '__main__':
    app.run(debug=True)


# Función para enviar correo de confirmación
def enviar_correo(data):
    remitente = "fernando.faundez@porvenirschool.cl"
    destinatario = "fernando.faundez.e@gmail.com"
    asunto = "Nueva Reserva de Carro Tecnológico"
    cuerpo = f"""\
    Asunto: {asunto}
    
    Buen dia Ma'am, necesito reservar el carro tecnológico número {data['carro']}, 
    en la sala {data['sala']}, de {data['horario']}, para {data['docente']}.
    Atte Bot de Reserva de carros Porvenir School
    """
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(remitente, "12345678abc#")
        server.sendmail(remitente, destinatario, cuerpo.encode('utf-8'))
        server.quit()
    except Exception as e:
        print("Error al enviar correo:", e)

if __name__ == '__main__':
    app.run(debug=True)

