import serial
import time

# Configura el puerto serial (ajusta a 'COM6')
arduino = serial.Serial('COM6', 9600)
time.sleep(2)  # Espera para que el puerto se inicie

import yagmail
from datetime import datetime

#------------------------------Alarma-------------------------------------------------------
def leer_credenciales(archivo):
    with open(archivo, 'r') as f:
        correo = f.readline().strip()             # Primera línea: tu correo
        contrasena = f.readline().strip()          # Segunda línea: contraseña de aplicación
    return correo, contrasena

def leer_destinatarios(archivo):
    with open(archivo, 'r') as f:
        destinatarios = [line.strip() for line in f.readlines() if line.strip()]
    return destinatarios

def enviar_notificacion(hora, lugar):
    # Leer credenciales y destinatarios desde los archivos
    correo, contrasena = leer_credenciales('credenciales.txt')
    destinatarios = leer_destinatarios('destinatarios.txt')
    
    # Configura yagmail con las credenciales leídas
    yag = yagmail.SMTP(correo, contrasena)

    # Crea el mensaje en formato HTML
    asunto = 'Alarma Activada'
    contenido = f'''
    <h1>¡Alarma Activada!</h1>
    <p>Se ha activado una alarma.</p>
    <p><strong>Hora:</strong> {hora}</p>
    <p><strong>Lugar:</strong> {lugar}</p>
    '''

    # Envía el correo a cada destinatario
    for destinatario in destinatarios:
        try:
            # Asegúrate de pasar el contenido como una lista
            yag.send(to=destinatario, subject=asunto, contents=[contenido])
            print(f'Correo enviado exitosamente a {destinatario}.')
        except Exception as e:
            print(f'Error al enviar el correo a {destinatario}: {e}')

#---------------------------------------------------------------------------------------------

def verificar_uid(uid):
    try:
        with open('permitidos.txt', 'r') as archivo:
            uids_permitidos = archivo.read().splitlines()
        # Imprime los UIDs permitidos y el UID que se compara
        print(f"UID leído: '{uid}'")
        print("UIDs permitidos:")
        for permitido in uids_permitidos:
            print(f"'{permitido}'")
        
        if uid in uids_permitidos:
            return "GRANTED"
        else:
            return "DENIED"
    except FileNotFoundError:
        print("Archivo 'permitidos.txt' no encontrado")
        return "DENIED"

while True:
    if arduino.in_waiting > 0:
        uid = arduino.readline().decode('utf-8').strip()
        if uid:  # Verifica que no esté vacío
            print(f"UID recibido: {uid}")
            
            resultado = verificar_uid(uid)
            arduino.write((resultado + '\n').encode('utf-8'))
            print(f"Resultado enviado: {resultado}")
            
            # Reemplaza estos valores por la hora y lugar deseados
            hora_evento = datetime.now().strftime('%H:%M')  # Hora actual
            lugar_evento = 'Oficina principal'  # Lugar del evento

            # Llama a la función para enviar la notificación
            enviar_notificacion(hora_evento, lugar_evento)
