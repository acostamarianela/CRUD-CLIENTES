from clasePersona import Persona
from firebase_admin import credentials
from firebase_admin import db

# Se hereda la clase persona para crear al Cliente
class Cliente(Persona):
    def __init__(self, nombre='', apellido='', email='', domicilio='', telefono='', dni=''):
        super().__init__(nombre, apellido, email, domicilio, telefono)
        self.__idCliente = None
        self.__dni = dni
    
    #ENCAPSULAMIENTO Y ABSTRACCION
    def getIdCliente(self):
        return self.__idCliente
    
    def setIdCliente(self, idCliente):
        self.__idCliente = idCliente
    
    def getDNI(self):
        return self.__dni
    
    def setDNI(self, dni):
        self.__dni = dni

    def agregarCliente(self):
        ref = db.reference('/Clientes')
        nuevoClienteRef = ref.push({
            'nombre': self.getNombre(),
            'apellido': self.getApellido(),
            'email': self.getEmail(),
            'domicilio': self.getDomicilio(),
            'telefono': self.getTelefono(),
            'dni': self.getDNI()
            
        })
        #idCliente = self.getIdCliente()
        idCliente = nuevoClienteRef.key  # Actualizamos el ID
        self.setIdCliente(idCliente)
        return idCliente
    
    def obtenerClientePorId(self, clienteId):
        ref = db.reference('/Clientes')
        cliente_data = ref.child(clienteId).get()
        if cliente_data:
            cliente = Cliente(
                cliente_data.get('nombre'),
                cliente_data.get('apellido'),
                cliente_data.get('email'),
                cliente_data.get('domicilio'),
                cliente_data.get('telefono'),
                cliente_data.get('dni')
            )
            cliente.setIdCliente(clienteId)
            return cliente
        else:
            return None
    
    def obtenerClientePorDNI(self, dni):
        ref = db.reference('/Clientes')
        resultados = ref.get()
        if resultados is not None:
            for cliente_id, cliente_data in resultados.items():
                if 'dni' in cliente_data and cliente_data['dni'] == dni:
                    print(f'Cliente encontrado: {cliente_data}')
                    cliente = Cliente(
                        cliente_data.get('nombre'),
                        cliente_data.get('apellido'),
                        cliente_data.get('email'), 
                        cliente_data.get('domicilio'),
                        cliente_data.get('telefono'),       
                        cliente_data.get('dni')
                    )
                    print(cliente_id)
                    cliente.setIdCliente(cliente_id)
                    print(f'hola {cliente.getIdCliente()}')
                    return cliente

        return None
    
    def actualizarCliente(self, clienteId, nombre, apellido, email, domicilio, telefono, dni):
        # Actualiza un cliente existente
        ref = db.reference('/Clientes')
        ref.child(clienteId).update({
            'nombre': nombre,
            'apellido': apellido,
            'email': email,
            'domicilio': domicilio,
            'telefono': telefono,
            'dni': dni
        })

    def eliminarCliente(self, clienteId):
        # Elimina un cliente por su ID
        ref = db.reference('/Clientes')
        ref.child(clienteId).delete()

    #POLIMORFISMO
    def obtenerDatos(self):
        dni = self.getDNI()
        return f'{super().obtenerDatos()}, DNI: {dni}'
    