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
    return "Bienvenido a la API de Reservas"

# Endpoint para consultar horarios disponibles
@app.route('/disponibles', methods=['GET'])
def obtener_horarios_disponibles():
    horarios = [f"{h}:00" for h in range(8, 19)]
    reservas = Reserva.query.with_entities(Reserva.horario).all()
    reservados = {r[0] for r in reservas}
    disponibles = [h for h in horarios if h not in reservados]
    return jsonify(disponibles)

# Endpoint para reservar un carro
@app.route('/reservar', methods=['POST'])
def reservar_carro():
    data = request.json
    nueva_reserva = Reserva(
        docente=data['docente'],
        sala=data['sala'],
        horario=data['horario'],
        carro=data['carro']
    )
    db.session.add(nueva_reserva)
    db.session.commit()
    enviar_correo(data)  # Notificación
    return jsonify({"mensaje": "Reserva realizada con éxito"}), 201

# Función para enviar correo de confirmación
def enviar_correo(data):
    remitente = "tu_correo@gmail.com"
    destinatario = "destino@gmail.com"
    asunto = "Nueva Reserva de Carro Tecnológico"
    cuerpo = f"""\
    Asunto: {asunto}
    
    Tío Hernán, necesito reservar el carro tecnológico número {data['carro']}, 
    en la sala {data['sala']}, de {data['horario']}, para {data['docente']}.
    Atte ReservaBot Porvenir School
    """
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(remitente, "tu_contraseña")
        server.sendmail(remitente, destinatario, cuerpo.encode('utf-8'))
        server.quit()
    except Exception as e:
        print("Error al enviar correo:", e)

if __name__ == '__main__':
    app.run(debug=True)

