from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from fbConfig import db  # Importa la variable db desde el módulo config
from claseCliente import Cliente

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buscarCliente', methods=['GET'])
def buscarCliente():
    clienteDNI = request.args.get('clienteDNI')
    if clienteDNI:
        cliente = Cliente()
        clienteObtenido = cliente.obtenerClientePorDNI(clienteDNI)
        if clienteObtenido:
            # Aquí puedes renderizar una plantilla para mostrar los detalles del cliente
            # o simplemente imprimir los detalles en la página.
            return render_template('mostrarCliente.html', cliente=clienteObtenido)
        else:
            return "Cliente no encontrado"
    return redirect(url_for('index'))


@app.route('/agregarCliente', methods=['GET', 'POST'])
def agregarCliente():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        email = request.form.get('email')
        domicilio = request.form.get('domicilio')
        telefono = request.form.get('telefono')
        dni = request.form.get('dniCliente')
        

        nuevoCliente = Cliente(nombre, apellido,email, domicilio, telefono, dni)
        nuevoCliente.agregarCliente()

        return redirect(url_for('index'))
    return render_template('agregarCliente.html')

@app.route('/modificarCliente/<clienteId>', methods=['GET', 'POST'])
def modificarCliente(clienteId):
    print(clienteId)
    cliente = Cliente()
    clienteObtenido = cliente.obtenerClientePorId(clienteId)

    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        domicilio = request.form['domicilio']
        telefono = request.form['telefono']
        dni = request.form['dniCliente']
        cliente.actualizarCliente(clienteId, nombre, apellido, email, domicilio, telefono, dni)

        return redirect('/')
    else:
        return render_template('modificarCliente.html', cliente=clienteObtenido, clienteId=clienteId)


@app.route('/eliminarCliente/<clienteId>', methods=['GET', 'POST'])
def eliminarCliente(clienteId):
    cliente = Cliente()
    clienteObtenido = cliente.obtenerClientePorId(clienteId)
    if clienteObtenido:
        cliente.eliminarCliente(clienteId)
    return redirect('/')

@app.route('/listarClientes', methods=['GET'])
def listarClientes():
    ref = db.reference('/Clientes')
    clientes = []
    resultado = ref.get()
    if resultado is not None:
        for cliente_id, cliente_data in resultado.items():
            cliente = Cliente(
                cliente_data.get('nombre'),
                cliente_data.get('apellido'),
                cliente_data.get('email'),
                cliente_data.get('domicilio'),
                cliente_data.get('telefono'),
                cliente_data.get('dni')
            )
            cliente.setIdCliente(cliente_id)
            clientes.append(cliente)
    return render_template('listarClientes.html', clientes=clientes)


if __name__ == '__main__':
    app.run(debug=True)