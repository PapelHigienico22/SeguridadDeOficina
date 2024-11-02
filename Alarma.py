import yagmail
from datetime import datetime

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

if __name__ == '__main__':
    # Reemplaza estos valores por la hora y lugar deseados
    hora_evento = datetime.now().strftime('%H:%M')  # Hora actual
    lugar_evento = 'Oficina principal'  # Lugar del evento

    # Llama a la función para enviar la notificación
    enviar_notificacion(hora_evento, lugar_evento)
