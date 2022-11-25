import random
from datetime import date, datetime
import re

#Clases
class User:
    def __init__(self, is_null, username, password, email, pais):
        self.is_null = is_null
        self.username = username
        self.password = password
        self.email = email
        self.pais=pais

#Para que la aplicación sea escalable, de momento no usaremos esta clase.
class Admin(User): #Hija de clase User
    pass

class Producto:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio

class Pedido:
    def __init__(self, idpedido, idcliente, idseguimiento, fecha, importe, importe_iva):
        self.idpedido = idpedido
        self.idcliente = idcliente
        self.idseguimiento = idseguimiento
        self.fecha = fecha
        self.importe = importe
        self.importe_iva = importe_iva

#Instanciando objetos
product1=Producto('Camiseta Angels',14.99)
product2=Producto('Sudadera oversize con capucha',25.99)
product3=Producto('Camiseta canalé manga larga',19.99)
product4=Producto('Blazer fiesta lentejuelas',39.99)
product5=Producto('Parka de plumón estampada',120)

#Variables globales
users = [] #base de datos de usuarios, todos los objetos que se almacenan en esta lista son objetos de clase User
logged_user = User(True, 'null', 'null', 'null', 'null') #Objeto de clase User
products=[product1,product2,product3,product4,product5]
cart = []
wishlist = []
new_pedido = Pedido(0,{ },0,{ },0,0) #Objeto de clase Pedido

#Funciones auxiliares
def check_user_exist(username): #La usamos en el registro
    user_exists = False
    if users:
        for user in users:
            if user.username == username:
                user_exists = True
    return user_exists
    
def verify_user(username, password): #La usamos en login
    user_verified = False
    for user in users:
        if user.username == username and user.password == password:
            user_verified = True
    return user_verified

def set_logged_user(username): #La usamos en el login
    for user in users:
        if user.username == username:
            return user

def check_email(email): #La usamos en el registro
    regex = re.compile(r'([A-Za-z0-9]+[.-_-])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if re.fullmatch(regex, email):
      return True
    else:
      return False

def check_input(input): #La usamos en el registro
    regex = '^(?!\s*$).+'
    if re.fullmatch(regex, input):
      return True
    else:
      return False

def calcular_iva(pais, importe):
    if logged_user.pais=="finlandia".lower() or logged_user.pais=="dinamarca".lower() or logged_user.pais=="suecia".lower():
        importe_iva=importe*1.25
    elif logged_user.pais=="portugal".lower() or logged_user.pais=="irlanda".lower() or logged_user.pais=="polonia".lower() or logged_user.pais=="grecia".lower():
        importe_iva=importe*1.23
    elif logged_user.pais=="españa".lower() or logged_user.pais=="belgica".lower() or logged_user.pais=="italia".lower() or logged_user.pais=="holanda".lower():
        importe_iva=importe*1.21
    elif logged_user.pais=="francia".lower() or logged_user.pais=="austria".lower() or logged_user.pais=="bulgaria".lower():
        importe_iva=importe*1.20
    elif logged_user.pais=="alemania".lower() or logged_user.pais=="chipre".lower() or logged_user.pais=="rumania".lower() or logged_user.pais=="malta".lower():
        importe_iva=importe*1.19
    else:
        importe_iva=importe*1.21 #Si no es ninguno de los anteriores, se aplica el tipo de IVA generalista
    return importe_iva

#Menú de tienda
def shop_menu():
    try:
        print('-- Menu de la tienda --')
        print(f'-- Usuario: {logged_user.username} --\n')
        print('[1] Ver lista de productos')
        print('[2] Ver carrito')
        print('[3] Ver lista de deseos')
        print('[4] Añadir producto a carrito')
        print('[5] Añadir producto a lista de deseos')
        print('[6] Pagar productos')
        print('[0] Deslogearse\n')
        option = int(input('Elija una opcion: '))
        print('')
        return option
    except:
        print('\nIntroduzca una opción válida.\n')

#Login menu functions
def login_menu():
    try:
        print('-- Menu del login --\n')
        print('[1] Login')
        print('[2] Registrarse')
        print('[0] Salir\n')
        option = int(input('Elija una opcion: '))
        print('')
        return option
    except:
        print('\nIntroduzca una opción válida.\n')

def signin():
    print('-- Registro de usuario --\n')
    try:
        username = input('Introduzca un nombre de usuario: ')
        while not check_input(username): #while check_input == False
            print('\nFormato de usuario incorrecto.\n')
            username = input('Por favor, introduzca otro usuario: ')
        while check_user_exist(username.lower()): #while check_user_exist == True (Explicado en la memoria)
            print('\nYa existe ese usuario\n')
            username = input('Por favor, introduzca otro nombre de usuario: ')
        password = input('Introduzca una contraseña: ')
        while not check_input(password):
            print('\nFormato de contraseña incorrecto.\n')
            password = input('Por favor, introduzca otra contraseña: ')
        email = input('Introduzca tu email: ')
        while not check_email(email): #while check_email == False (Explicado en la memoria)
            print('\nFormato de email incorrecto.\n')
            email = input('Por favor, introduzca otro email: ')
        pais = input('Introduzca su país de residencia: ')
        while not check_input(pais):
            print('\nFormato de país incorrecto.\n')
            pais = input('Por favor, introduzca otro país: ')
    except:
        print('\nError al registrar usuario\n')
    else:
        new_user = User(False, username.lower(), password, email, pais) #instanciando objeto
        users.append(new_user) #añadimos este objeto a la lista users (base de datos de usuarios)
        print('\nUsuario registrado exitosamente\n')
    
def login():
    print('-- Login de usuario --\n')
    username = input('Introduzca su nombre de usuario: ')
    password = input('Introduzca su contraseña: ')
    exit_login = ''
    while (not verify_user(username.lower(), password)) and (exit_login.lower() != 'e'):
        print('\nUsuario o contraseña erroneos\n')
        exit_login = input('Si quiere salir del login escriba "e", si quiere introducir sus datos otra vez escriba cualquier otra cosa: ')
        print('')
        if exit_login.lower() != 'e':
            username = input('Introduzca su nombre de usuario: ')
            password = input('Introduzca su contraseña: ')
    if exit_login.lower() != 'e': 
        global logged_user
        logged_user = set_logged_user(username.lower()) #Settear la variable. Busca el objeto usuario en la lista users y lo pone en la variable.
        print(f'\nSe ha logeado exitosamente, {logged_user.username}\n')

# Ver productos (Opcion 1)
def verProductos():
    print("Estos son los artículos disponibles en nuestra tienda:")
    for i in range(len(products)):
        print(f'''
            [{i+1}] {products[i].nombre} | Precio: {products[i].precio} €''')
    print('')

# Ver carrito (Opcion 2)
def verCarrito():
    if not cart: #Si la lista carrito está vacía
        print('Tu carrito está vacío.')
        print('')
    else:
        print("Estos son los artículos en tu carrito:")
        for i in range(len(cart)):
            print(f'''
                [{i+1}] {cart[i].nombre} | Precio: {cart[i].precio} €''')
        print('')

# Ver lista de deseos (Opcion 3)
def verDeseos():
    if not wishlist: #Si la lista de deseos está vacía
        print('Tu lista de deseos está vacía.')
        print('')
    else:
        print("Estos son los artículos en tu lista de deseos:")
        for i in range(len(wishlist)):
            print(f'''
                [{i+1}] {wishlist[i].nombre} | Precio: {wishlist[i].precio} €''')
        print('')
    
# Añadir al carrito (Opcion 4)
def comprar():
    verProductos()
    exit_comprar = ''
    option_buy = 0
    while exit_comprar.lower() != 'e':
        try:
            option_buy=int(input('Introduzca el código de producto que deseas comprar: '))
            if option_buy==0:
                raise Exception("Error") #Forzamos que haya un error para que salte el trycatch
            cart.append(products[option_buy-1])
            print(f'\nSe ha añadido exitosamente {products[option_buy-1].nombre} a su carrito.\n')
            exit_comprar = input('Si quiere dejar de comprar escriba "e", si quiere añadir otro producto al carrito escriba cualquier otra cosa: ')
            print('')
        except:
            print('\nEste producto no existe.\n')

# Añadir a lista de deseos (Opcion 5)
def deseos():
    verProductos()
    exit_deseos = ''
    option_deseos = 0
    while exit_deseos.lower() != 'e':
        try:
            option_deseos=int(input('Introduzca el código de producto que deseas añadir a la lista de deseos: '))
            if option_deseos==0:
                raise Exception("Error") #Forzamos que haya un error para que salte el trycatch
            wishlist.append(products[option_deseos-1])
            print(f'\nSe ha añadido exitosamente {products[option_deseos-1].nombre} a su lista de deseos.\n')
            exit_deseos = input('Si quiere volver al menú escriba "e", si quiere añadir otro producto a la lista de deseos escriba cualquier otra cosa: ')
            print('')
        except:
            print('\nEste producto no existe.\n')

# Pagar productos (Opcion 6)
def pagar():
    if not cart: #Si el carrito está vacío
        print('Tu carrito está vacío. Añade productos para proceder al pago.')
        print('')
    else:
        option_pagar=''
        importe=sum(producto.precio for producto in cart) #Sumatorio del precio de los items de la lista carrito
        importe_iva=calcular_iva(logged_user.pais, importe) #Llamamos a función auxiliar y le pasamos dos parámetros
        idpedido=random.randint(31000, 49990) #Generamos ID pedido
        idseguimiento=random.randint(31000, 49990) #Generamos código de seguimiento
        fecha=datetime.now()
        fechap=fecha.strftime('%d-%m-%Y') #Damos formato a la fecha
        
        print(f'El sumatorio total sin IVA del importe de su compra es {round(importe, 2)} €\n''')
        print(f'El sumatorio total de su compra aplicando el IVA de {logged_user.pais.capitalize()} es {round(importe_iva, 2)} €\n')
        option_pagar=input("¿Desea proceder con el pago de su pedido? Escriba S/N: ")
        print('')
        if option_pagar.lower()=='s':
            print(f'Muchas gracias, {logged_user.username.capitalize()}. En breve recibirá su pedido. Su código de seguimiento es {idseguimiento}.\n')
            global new_pedido
            new_pedido = Pedido(idpedido, logged_user.username, idseguimiento, fechap, importe, importe_iva) #instanciando objeto
            seguimiento()
            cart.clear() #Tras el pago de los productos, la lista carrito se vacía
        else:
            pass

# Realiza el seguimiento tras comprar
def seguimiento():
    print(f'Hemos enviado un email a {logged_user.email} con el resumen de su pedido.')
    with open('resumen_pedido.txt','w') as f:
        f.write(f'destinatario: {logged_user.email}\n\n')
        f.write(f'---- RESUMEN DE PEDIDO ----\n\n')
        f.write(f'¡Hola, {logged_user.username.capitalize()}!\n\n')
        f.write(f'El ID de su pedido es {new_pedido.idpedido} | Fecha de compra: {new_pedido.fecha}\n')
        f.write(f'El importe total de su pedido es {round(new_pedido.importe_iva, 2)} €\n')
        f.write(f'Su código de seguimiento es {new_pedido.idseguimiento}\n\n')
        f.write(f'Muchas gracias por su compra.')
    print('')
    
#Main
def main():
    option_login = login_menu()
    while option_login != 0:
        if option_login == 1:
            login()
            if logged_user.is_null == False: #propiedad de clase User, is_null, funciona como bandera o flag
                option_shop = shop_menu()
                while option_shop != 0:
                    if option_shop == 1:
                       verProductos()
                    elif option_shop == 2:
                        verCarrito()
                    elif option_shop == 3:
                        verDeseos()
                    elif option_shop == 4:
                        comprar()
                    elif option_shop == 5:
                        deseos()
                    elif option_shop == 6:
                        pagar()
                    option_shop = shop_menu()
        elif option_login == 2:
            signin()
        option_login = login_menu()

#Initiate program
main()