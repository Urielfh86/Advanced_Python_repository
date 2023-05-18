STOCK ANALYZER

Esta aplicación está diseñada para obtener información de las acciones de la bolsa de los Estados Unidos.
Utiliza la API de Alpha Vantage para brindar información de acciones de la bolsa de Estados Unidos y muestra la información por consola. 
Además, si el usuario lo desea, también puede enviar la información por correo electrónico para una persistencia de la misma.

Requisitos para su correcto funcionamiento: 

1- Para utilizar esta aplicación, primero se debe obtener una API Key de Alpha Vantage siguiendo las instrucciones en este enlace: https://www.alphavantage.co/support/#api-key

Esta API key debe ser colocada en el fichero "stock_analyzer.py", línea 8 del código, en la variable de clase "__api_key".

2- Para enviar información por correo electrónico, se debe tener una cuenta de correo y crear una contraseña de aplicación. En el caso de utilizar Gmail, se deben seguir los siguientes pasos:

I. Inicia sesión en tu cuenta de Gmail.
II. Haz click en tu foto de perfil en la esquina superior derecha y selecciona "Google Account".
III. Haz click en "Seguridad".
IV. Haz click en "Acceso a la cuenta de Google".
V. Haz click en "Generar contraseña de aplicación".
VI. Sigue las instrucciones para generar una contraseña específica de la aplicación.

Esta contraseña debe ser colocada en el campo "Password" que muestra la interfaz gráfica.

IMPORTANTE: Si no se utiliza el servidor Gmail, se debe cambiar el dominio en la línea 27 del código 'smtp.gmail.com' por 'smtp.dominio_utilizado.com' en el fichero "mail_sender.py".

Se deben tener instalados los módulos "sys", "requests", "PyQt6" y "smtplib".

Por último, para correr la aplicación se debe ejecutar el fichero "analyzer.py", código principal. 

NO PEDIR ANÁLISIS MUY SEGUIDOS PORQUE LA API GRATUITA FALLA. DEJAR PASAR UN MINUTO COMO MÍNIMO ENTRE ANÁLISIS. 


