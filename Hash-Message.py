import bcrypt
import requests
from cryptography.fernet import Fernet

# URL para la base de datos de usuario 
base_url = 'http://localhost:3000/usuarios'

def registrar_usuario(nombre_usuario, contraseña):
    # Verificar si el nombre de usuario ya existe en la base de datos
    response = requests.get(base_url + "?username=" + nombre_usuario)
    if response.text != "[]":
        print("El nombre de usuario ya existe.")
        return
    
    # Hashear la contraseña antes de almecenarla
    contraseña_hasheada = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt())
    
    # Crear un diccionario con los datos nuevos del nuevo usuario
    nuevo_usuario = {
        'username': nombre_usuario,
        'password': contraseña_hasheada.decode('utf-8') # Convertir el hash a una cadena
    }
    
    # Enviar una solicitud POST para registrar al nuevo usuario
    response = requests.post(base_url, json=nuevo_usuario)
    
    if response.status_code == 201:
        print("Usuario registrado correctamente")
    else:
        print("Error al registrar usuario.")
        
def verificar_contraseña(nombre_usuario, contraseña):
    # Realizar una solicitud GET para obtener los datos del usuario
    response = requests.get(base_url + "?username=" + nombre_usuario)
    
    if response.text == "[]":
        print("El usuario no existe")
        return
    else:
        response_json = response.json()
        contraseña_hasheada = response_json[0]['password']
        if bcrypt.checkpw(contraseña.encode('utf-8'), contraseña_hasheada.encode('utf-8')):
            print("Contraseña correcta. Inicio de sesión exitoso.")
            
            mensaje(nombre_usuario)
            
            return True
        else:
            print("Contraseña incorrecta. Inicio de sesión fallido")
            return False
        
def generar_clave():
    # Generar una clave cifrada
    clave = Fernet.generate_key()
    return clave 

def cifrar_mensaje(clave, mensaje):
    cifrador = Fernet(clave)
    
    # Cifrar el mensaje
    mensaje_cifrado = cifrador.encrypt(mensaje.encode('utf-8'))
    return mensaje_cifrado
    
def descifrar_mensaje(clave, mensaje_cifrado):
    cifrador = Fernet(clave)
    
    # Desifrar el mensaje
    mensaje_descifrado = cifrador.decrypt(mensaje_cifrado).decode('utf-8')
    return mensaje_descifrado

def mensaje(nombre_usuario):
    while True:
        print("\nBienvenido " + nombre_usuario + ", que desea hacer?")
        print("Opciones: \n1. Cifrar\n2. Descifrar\n3. Salir")
        opcion = int(input("Seleccione una opcion: "));
        if opcion == 1:
            
            while True:
                clave = generar_clave()
                print(f"Clave de cifrado generada: {clave}")
                
                print("Introduce un mensaje para cifrar:")
                mensaje = input()
                
                # Cifrar el mensaje 
                mensaje_cifrado = cifrar_mensaje(clave, mensaje)
                print(f"Mensaje cifrado: {mensaje_cifrado}")
                
                # Descifrar el mensaje
                mensaje_descifrado = descifrar_mensaje(clave, mensaje_cifrado)
                print(f"Mensaje descifrado: {mensaje_descifrado}")
                
                salir = int(input("\n¿Desea cifrar otro mensaje?\n1.Si\n2.No\nR= "))
                
                if salir == 2: 
                    break
                
        elif opcion == 2:
            
            while True:
                print("Introduce la calve cifrada:")
                clave = input()
                
                print("Introduce un mensaje para descifrar")
                mensaje_cifrado = input()
                
                # Descifrar el mensaje
                mensaje_descifrado = descifrar_mensaje(clave, mensaje_cifrado)
                print(f"Mensaje descifrado: {mensaje_descifrado}")
                
                salir = int(input("\n¿Desea descifrar otro mensaje?\n1.Si\n2.No\nR= "))
                
                if salir == 2:
                    break
                
        elif opcion == 3:
            return False 
        
def main():
    print("Bienvenido al Sistema de Registro y Autenticacion")
    
    while True:
        print("\n1. Registrar nuevo usuario")
        print("2. Iniciar sesión")
        print("3. Salir")
        opcion = input("Ingrese la opción deseada (1/2/3): ")
        
        if opcion == '1':
            nombre_usuario = input("Ingrese el nombre de usuario: ")
            contraseña = input("Ingrese la contraseña: ")
            registrar_usuario(nombre_usuario, contraseña)
        elif opcion == '2':
            nombre_usuario = input("Ingrese el nombre de usuario: ")
            contraseña = input("Ingrese la contraseña: ")
            verificar_contraseña(nombre_usuario, contraseña)
        elif opcion == '3':
            print("¡Hasta luego!")
            break
        else:
            print("Opción no valida. Intente de nuevo.")
            
if __name__ == "__main__":
    main()
                   