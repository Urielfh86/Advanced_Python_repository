import smtplib
from email.mime.text import MIMEText

def email_sender(from_, to, subject, message, password):
    """Para un correcto funcionamiento se debe crear una contraseña de aplicación para poder conectarse al mail mediante el servidor SMTP.
    En el caso de utilizar GMAIL, se deben seguir los siguientes pasos:

    1. Inicia sesión en tu cuenta de Gmail.
    2. Haz clic en tu foto de perfil en la esquina superior derecha y selecciona "Google Account".
    3. Haz clic en "Seguridad".
    4. Haz clic en "Acceso a la cuenta de Google".
    5. Haz clic en "Generar contraseña de aplicación".
    6. Sigue las instrucciones para generar una contraseña específica de la aplicación.
    7. Usa la nueva contraseña específica pasándola en la GUI en el parámetro "password" de la aplicación para iniciar sesión en el servidor SMTP en tu código.

    Además, si no se usa el servidor GMAIL, se debe cambiar el dominio en la linea 27 del código 'smtp.gmail.com' por 'smtp.dominio_utilizado.com'.
    """

    msg = MIMEText(message)
    msg['From'] = from_
    msg['To'] = to
    msg['Subject'] = subject

    port = 587 # Gmail
    mi_contraseña = password

    server = smtplib.SMTP('smtp.gmail.com', port)
    server.starttls()
    server.login(from_, mi_contraseña)

    server.sendmail(from_, to, msg.as_string())

    server.quit()
