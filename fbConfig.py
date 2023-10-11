import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

#carga del certificado del proyecto
cred = credentials.Certificate("credentials/crud-poo-ea690-firebase-adminsdk-pdix6-0a7cb38b1c.json")

#referencia a la base de datos en tiempo real
firebase_admin.initialize_app(cred,{'databaseURL':'https://crud-poo-ea690-default-rtdb.firebaseio.com/'})

