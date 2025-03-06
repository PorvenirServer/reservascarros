from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__)

# -------------- CONFIGURACION DEL SERVIDOR SMTP (Correo y App Password) --------------
# Asegúrate de cambiar los siguientes valores con tu propia información.
SMTP_SERVER = "smtp.gmail.com"  # Si usas Gmail, esto es correcto
SMTP_PORT = 587  # Puerto para TLS

# AQUI DEBES COLOCAR TU CORREO ELECTRONICO (ejemplo: "tu_correo@gmail.com")
SENDER_EMAIL = "fernando.faundez.e@gmail.com"  # Cambia por tu correo de Gmail

# AQUI DEBES COLOCAR TU CONTRASEÑA (O UN APP PASSWORD SI USAS GMAIL CON 2FA)
SENDER_PASSWORD = "U6K7mQNPwFTcdHg1977"  # Cambia por tu contraseña o App Password

# -------------- FUNCION PARA ENVIAR CORREO ----------------
def send_email(recipient_email, subject, message_body):
    try:
        # Crear el mensaje
        message = MIMEMultipart()
        message["From"] = SENDER_EMAIL
        message["To"] = recipient_email
        message["Subject"] = subject

        # Agregar el cuerpo del mensaje
        message.attach(MIMEText(message_body, "plain"))

        # Conectar al servidor SMTP
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Encriptar la conexión
            server.login(SENDER_EMAIL, SENDER_PASSWORD)  # Iniciar sesión con tus credenciales
            server.sendmail(SENDER_EMAIL, recipient_email, message.as_string())  # Enviar el correo

        print("Correo enviado exitosamente.")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

# -------------- RUTA DE RESERVA ----------------
@app.route('/reservar', methods=['POST'])
def reservar():
    data = request.json  # Suponiendo que los datos vienen en formato JSON

    # Extraer la información de la solicitud (estos datos provienen del formulario de Google)
    nombre = data.get('nombre')
    correo = data.get('correo')
    horario = data.get('horario')
    sala = data.get('sala')
    carro = data.get('carro')

    # -------------- COMPROBAR DISPONIBILIDAD ----------------
    # Aquí agregas la lógica para validar si el horario está disponible o no
    horario_disponible = True  # Esto debe reemplazarse con la lógica de validación de tu base de datos

    if not horario_disponible:
        # Si el horario no está disponible, enviamos un correo con el aviso
        subject = "Confirmación de Reserva"
        message = f"Estimado/a {nombre},\n\nEl horario {horario} no está disponible de momento. Le ruego que lo/s modifique.\n\nAtte, Bot Reserva Carro Tecnológico."
        send_email(correo, subject, message)  # Enviar correo al usuario
        return jsonify({"message": "El horario no está disponible, por favor modifique."}), 400

    # Si el horario está disponible, proceder con la reserva (guardar en base de datos, etc.)
    subject = "Confirmación de Reserva Exitosa"
    message = f"Estimado/a {nombre},\n\nSu reserva ha sido confirmada para el horario {horario}, en la sala {sala}, con el carro {carro}.\n\nAtte, Bot Reserva Carro Tecnológico."
    send_email(correo, subject, message)  # Enviar correo al usuario confirmando la reserva

    return jsonify({"message": "Reserva realizada exitosamente."}), 201

# -------------- INICIAR LA APLICACION FLASK ----------------
if __name__ == '__main__':
    app.run(debug=True)
