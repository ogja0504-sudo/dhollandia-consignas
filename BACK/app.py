from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

# =========================================
# APP
# =========================================

app = Flask(__name__)

CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg://postgres.ybqeosuunwyajpzokzxl:OVALLEGARCIA0206@aws-1-us-east-1.pooler.supabase.com:6543/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

DB = SQLAlchemy(app)

# =========================================
# CORREO
# =========================================

EMAIL_ADMIN = 'refaccionesmx@dhollandia.com'
EMAIL_PASSWORD = 'TU_PASSWORD'

def enviar_alerta(asunto, mensaje):

    try:

        msg = MIMEText(mensaje)

        msg['Subject'] = asunto
        msg['From'] = EMAIL_ADMIN
        msg['To'] = EMAIL_ADMIN

        servidor = smtplib.SMTP('smtp.gmail.com', 587)

        servidor.starttls()

        servidor.login(EMAIL_ADMIN, EMAIL_PASSWORD)

        servidor.send_message(msg)

        servidor.quit()

        print('ALERTA ENVIADA')

    except Exception as e:

        print(e)

# =========================================
# TABLAS
# =========================================

class Refaccion(DB.Model):

    id = DB.Column(DB.Integer, primary_key=True)

    ciudad = DB.Column(DB.String(100))
    codigo = DB.Column(DB.String(100))
    descripcion = DB.Column(DB.String(300))

    stock = DB.Column(DB.Integer)

    minimo = DB.Column(DB.Integer)

    maximo = DB.Column(DB.Integer)

class Movimiento(DB.Model):

    id = DB.Column(DB.Integer, primary_key=True)

    fecha = DB.Column(DB.String(100))

    ciudad = DB.Column(DB.String(100))

    codigo = DB.Column(DB.String(100))

    descripcion = DB.Column(DB.String(300))

    tipo = DB.Column(DB.String(100))

    cantidad = DB.Column(DB.Integer)

    observaciones = DB.Column(DB.String(500))

# =========================================
# STOCK INICIAL
# =========================================

def crear_stock_inicial():

    if Refaccion.query.first():

        return

    datos = [

        # =========================================
        # LEON
        # =========================================

        ("LEON", "E0242", "CONEXION DEL CABLE DEL SOLENOIDE 24V", 1, 0, 1),
        ("LEON", "E0242.H", "CONEXION DEL CABLE DEL SOLENOIDE 24 V HYDAC", 1, 0, 1),
        ("LEON", "E0246.K.10", "BOBINA CONEXIÓN A CABLE 10V", 1, 0, 1),
        ("LEON", "E0634.12", "RELE REDONDO TRBT 12V 150A", 1, 0, 1),
        ("LEON", "E0634.24", "RELÉ REDONDO TRBT 24V 150A", 1, 0, 1),
        ("LEON", "E0834.C5009.VHT", "CONTROL CON INTERRUPTOR DE PALANCA VHT", 2, 0, 2),
        ("LEON", "EG509.B.P0.K01.C3807", "CAJA DE MANDO CON BOTÓN PULSADOR ARCTIC DW", 1, 0, 1),
        ("LEON", "F020", "FILTRO COMPLENTARIO DE ACEITE", 1, 0, 1),
        ("LEON", "M0411", "TAPA CENTRAL HIDROELECTRICA 3000W", 1, 0, 1),
        ("LEON", "MP025", "MOTOR 24V 2KW BOMBA EXTERNA", 2, 0, 4),
        ("LEON", "MP033", "MOTOR 12V 1.6-2KW BOMBA EXTERNA", 1, 0, 4),
        ("LEON", "OAE017.PR", "INTERRUPTOR DE PALANCA EXTERIOR", 1, 0, 2),
        ("LEON", "OAE457.35.250.10", "FUSIBLE MEGA 250A 35MM", 1, 0, 1),
        ("LEON", "P011", "BOMBA DE MOTOR 13A-2.5CC -5L", 1, 0, 4),
        ("LEON", "P030.26", "BOMBA HIDRAULICA 2.6CC", 4, 0, 4),
        ("LEON", "V133.12.H", "VALVULA DE SEGURIDAD SA 12V - HYDAC", 1, 0, 1),
        ("LEON", "V177", "CARTUCHO SIN BOBINA DA DHO M18", 1, 0, 1),
        ("LEON", "V178", "CARTUCHO SIN BOBINA 4/2 VÍAS", 1, 0, 1),
        ("LEON", "V190.12.4", "VALVULA LOGICA VH30 12V P4.5", 1, 0, 1),

        # =========================================
        # QUERETARO
        # =========================================

        ("QUERETARO", "P030.26", "BOMBA HIDRAULICA", 5, 0, 5),
        ("QUERETARO", "MP025", "MOTOR 24V", 5, 0, 5),
        ("QUERETARO", "V133.12.H", "VALVULA", 5, 0, 5),
        ("QUERETARO", "E0634.12", "RELE REDONDO", 5, 0, 5),
        ("QUERETARO", "P011", "BOMBA MOTOR", 5, 0, 5),
        ("QUERETARO", "M0411", "TAPA CENTRAL", 5, 0, 5),
        ("QUERETARO", "V190.12.4", "VALVULA", 1, 0, 5),
        ("QUERETARO", "V177", "CARTUCHO", 5, 0, 5),
        ("QUERETARO", "E0242", "CONEXION", 5, 0, 5),
        ("QUERETARO", "V178", "CARTUCHO", 3, 0, 5),
        ("QUERETARO", "E0242.H", "CONEXION HYDAC", 5, 0, 5),
        ("QUERETARO", "E0246.K.10", "BOBINA", 5, 0, 5),
        ("QUERETARO", "EG509.B.P0", "CAJA DE MANDO", 2, 0, 5),

        # =========================================
        # IZTAPALAPA
        # =========================================

        ("IZTAPALAPA", "E2047", "LLAVE INTERRUPTOR", 5, 0, 4),
        ("IZTAPALAPA", "E0634.24", "RELE REDONDO 24V", 1, 0, 4),
        ("IZTAPALAPA", "MP021", "MOTOR 24V", 2, 0, 4),
        ("IZTAPALAPA", "MP033", "MOTOR 12V", 1, 0, 4),
        ("IZTAPALAPA", "E0832.B", "CONTROL UP/DOWN", 2, 0, 4),
        ("IZTAPALAPA", "E0634.12", "RELE REDONDO 12V", 2, 0, 4),

        # =========================================
        # REYES
        # =========================================

        ("REYES", "MP021", "MOTOR 24V", 2, 0, 4),
        ("REYES", "E0811", "INTERRUPTOR", 1, 0, 4),
        ("REYES", "P030.26", "BOMBA HIDRAULICA", 2, 0, 4),
        ("REYES", "V133.12.H", "VALVULA", 1, 0, 4),
        ("REYES", "E0634.12", "RELE REDONDO", 1, 0, 4),
        ("REYES", "E0076", "LLAVE INTERRUPTOR", 2, 0, 4),

        # =========================================
        # VALLEJO
        # =========================================

        ("VALLEJO", "E0634.24", "RELE REDONDO 24V", 2, 0, 4),
        ("VALLEJO", "MP021", "MOTOR 24V", 2, 0, 4),
        ("VALLEJO", "F020", "FILTRO", 2, 0, 4),
        ("VALLEJO", "MP025", "MOTOR 24V", 1, 0, 4),
        ("VALLEJO", "MP033", "MOTOR 12V", 2, 0, 4),
        ("VALLEJO", "E0832.B", "CONTROL UP/DOWN", 2, 0, 4),
        ("VALLEJO", "E0634.12", "RELE REDONDO 12V", 2, 0, 4),
    ]

    for d in datos:

        nueva = Refaccion(
            ciudad=d[0],
            codigo=d[1],
            descripcion=d[2],
            stock=d[3],
            minimo=d[4],
            maximo=d[5]
        )

        DB.session.add(nueva)

    DB.session.commit()

    print("STOCK INICIAL CARGADO")

# =========================================
# VER STOCK
# =========================================

@app.route('/stock')
def stock():

    refacciones = Refaccion.query.order_by(
        Refaccion.ciudad.asc()
    ).all()

    resultado = []

    for r in refacciones:

        estado = "NORMAL"

        if r.stock <= r.minimo:

            estado = "ALERTA"

        resultado.append({

            'id': r.id,
            'ciudad': r.ciudad,
            'codigo': r.codigo,
            'descripcion': r.descripcion,
            'stock': r.stock,
            'minimo': r.minimo,
            'maximo': r.maximo,
            'estado': estado
        })

    return jsonify(resultado)

# =========================================
# MOVIMIENTO
# =========================================

@app.route('/movimiento', methods=['POST'])
def movimiento():

    data = request.json

    ref = Refaccion.query.get(data['id'])

    cantidad = int(data['cantidad'])

    if data['tipo'] == 'SALIDA':

        ref.stock -= cantidad

        if ref.stock < 0:

            ref.stock = 0

        if ref.stock <= ref.minimo:

            enviar_alerta(

                'ALERTA STOCK BAJO',

                f'''

Ciudad: {ref.ciudad}

Codigo: {ref.codigo}

Descripcion: {ref.descripcion}

Stock actual: {ref.stock}

                '''
            )

    if data['tipo'] == 'ENTRADA':

        ref.stock += cantidad

        if ref.stock > ref.maximo:

            ref.stock = ref.maximo

    mov = Movimiento(

        fecha=str(datetime.now()),

        ciudad=ref.ciudad,

        codigo=ref.codigo,

        descripcion=ref.descripcion,

        tipo=data['tipo'],

        cantidad=cantidad,

        observaciones=data['observaciones']
    )

    DB.session.add(mov)

    DB.session.commit()

    return jsonify({'success': True})

# =========================================
# HISTORIAL
# =========================================

@app.route('/historial')
def historial():

    movimientos = Movimiento.query.order_by(
        Movimiento.id.desc()
    ).all()

    resultado = []

    for m in movimientos:

        resultado.append({

            'fecha': m.fecha,

            'ciudad': m.ciudad,

            'codigo': m.codigo,

            'descripcion': m.descripcion,

            'tipo': m.tipo,

            'cantidad': m.cantidad,

            'observaciones': m.observaciones
        })

    return jsonify(resultado)

# =========================================
# EDITAR
# =========================================

@app.route('/editar/<int:id>', methods=['PUT'])
def editar(id):

    ref = Refaccion.query.get(id)

    data = request.json

    ref.stock = data['stock']

    ref.minimo = data['minimo']

    ref.maximo = data['maximo']

    DB.session.commit()

    return jsonify({'success': True})

# =========================================
# START
# =========================================


with app.app_context():

    DB.create_all()

    crear_stock_inicial()

if __name__ == '__main__':

    app.run(
        host='0.0.0.0',
        port=5000
    )
    