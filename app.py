# Importar las bibliotecas necesarias
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from fbConfig import db  # Importa la variable db desde el módulo config
from claseCliente import Cliente

# Crear la aplicación Flask
app = Flask(__name__)


#Ruta principal que renderiza la pagina donde se van a poder realizar las primeras acciones
@app.route('/')
def index():
    return render_template('index.html')

#Ruta para buscar un cliente
@app.route('/buscarCliente', methods=['GET'])
# Esta ruta maneja la búsqueda de un cliente por su DNI. Recibe el DNI del cliente como un parámetro GET, 
# busca el cliente en la base de datos y muestra la información del cliente si se encuentra.
def buscarCliente():
    clienteDNI = request.args.get('clienteDNI')
    if clienteDNI:
        cliente = Cliente()
        clienteObtenido = cliente.obtenerClientePorDNI(clienteDNI)
        if clienteObtenido:
            return render_template('mostrarCliente.html', cliente=clienteObtenido)
        else:
            return "Cliente no encontrado"
    return redirect(url_for('index'))


#Ruta para agregar un cliente
@app.route('/agregarCliente', methods=['GET', 'POST'])
def agregarCliente():
    #Recibe los datos del cliente a través de un formulario HTML
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

#Ruta para modificar un cliente
@app.route('/modificarCliente/<clienteId>', methods=['GET', 'POST'])
def modificarCliente(clienteId):
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


#Ruta para eliminar cliente
@app.route('/eliminarCliente/<clienteId>', methods=['GET', 'POST'])
def eliminarCliente(clienteId):
    #Esta ruta permite eliminar un cliente existente. Recibe el ID del cliente como parámetro en la URL y 
    #procede a eliminarlo de la base de datos.
    cliente = Cliente()
    clienteObtenido = cliente.obtenerClientePorId(clienteId)
    if clienteObtenido:
        cliente.eliminarCliente(clienteId)
    return redirect('/')

#Ruta para Listar Clientes
@app.route('/listarClientes', methods=['GET'])
#Esta ruta recupera todos los clientes de la base de datos y muestra una lista de clientes en una página.
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

# Ejecutar la aplicacion Flask
if __name__ == '__main__':
    app.run(debug=True)