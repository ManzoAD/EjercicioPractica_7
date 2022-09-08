import json
import random
import bcrypt
from io import open
'''
Tema: Aplicación de estructuras de Python: archivos, JSON, cifrado de contraseñas
Fecha: 06 de septiembre del 2022
Autor: Leonardo Martínez González
Continuación de la práctica 6
'''


'''
Crear un programa que utilice los archivos Estudiantes.prn y kardex.txt:

1. Crear un método que regrese un conjunto de tuplas de estudiantes. (5) 10 min.
2. Crear un método que regrese un conjunto de tuplas de materias.
3. Crear un método que dado un número de control regrese el siguiente formato JSON:
   {
        "Nombre": "Manzo Avalos Diego",
        "Materias":[
            {
                "Nombre":"Base de Datos",
                "Promedio":85
            },
            {
                "Nombre":"Inteligencia Artificial",
                "Promedio":100
            },
            . . . 
        ],
        "Promedio general": 98.4
   }

4. Regresar una lista de JSON con las materias de un estudiante, el formato es el siguiente:
[
    {"Nombre": "Contabilidad Financiera"},
    {"Nombre": "Dise\u00f1o UX y UI"}, 
    {"Nombre": "Base de datos distribuidas"}, 
    {"Nombre": "Finanzas internacionales IV"}, 
    {"Nombre": "Analisis y dise\u00f1o de sistemas de informacion"}, 
    {"Nombre": "Microservicios"},
    {"Nombre": "Algoritmos inteligentes"}
]


5. Generar un archivo de usuarios que contenga el numero de control, éste será el usuario
   y se generará una contraseña de tamaño 10 la cual debe tener:
   A. Al menos una letra mayúscula 
   B. Al menos una letra minúscula
   C. Numeros
   D. Al menos UN carácter especial, considere ( @, #, $,%,&,_,?,! )

   Considere:
    - Crear un método para generar cada caracter
    - El codigo ascii: https://elcodigoascii.com.ar/
    - Cifrar la contraseña con bcrypt, se utiliza con node.js, react, etc. Para ello:
        * Descargue la libreria bcrypt con el comando: "pip install bcrypt" desde la terminal o desde PyCharm
        * Página: https://pypi.org/project/bcrypt/
        * Video:Como Cifrar Contraseñas en Python     https://www.youtube.com/watch?v=9tEovDYSPK4

   El formato del archivo usuarios.txt será:
   control contrasena contraseña_cifrada

6. Crear un método "autenticar_usuario(usuario,contrasena)" que regrese una bandera que 
   indica si se pudo AUTENTICAR, el nombre del estudiante y un mensaje, regresar el JSON:
   {
        "Bandera": True,
        "Usuario": "Leonardo Martínez González",
        "Mensaje": "Bienvenido al Sistema de Autenticación de usuarios"
   }

   ó

   {
        "Bandera": False,
        "Usuario": "",
        "Mensaje": "No existe el Usuario"
   }

   ó

    {
        "Bandera": False,
        "Usuario": "Leonardo Martínez González",
        "Mensaje": "Contraseña incorrecta"
   }


'''
#4.- Lista Materias
def regresa_materias_por_estudiante(ctrl):
    promedios=materias()
    lista_materias=[]
    for mat in promedios:
        c,m,p=mat #Destructurar la variable mat
        if ctrl==c:
            lista_materias.append({"Nombre":m})
    return  json.dumps(lista_materias)
    
#print(regresa_materias_por_estudiante("18420461"))
#for i in regresa_materias_por_estudiante("18420461"):
 #   print(i)

 #Ejercicio numero 6
def generar_letra_minuscula():
    return chr(random.randint(65,90))

def generar_letra_mayuscula():
    return chr(random.randint(97,122))

def generar_numeros():
    return chr(random.randint(48,57))

def generar_caracter_especial():
    lista_carateres=['@','#','$','%','&','_','?','!']
    return lista_carateres[random.randint(0,7)]

def generar_contra():
    clave = ""
    for i in range(1,10):
        numero = random.randint(1,5)
        if numero==1:
            clave+=generar_letra_mayuscula()
        elif numero==2:
            clave+=generar_letra_minuscula()
        elif numero==3:
            clave+=generar_caracter_especial()
        elif numero>=4 and numero <=5:
            clave+=generar_numeros()
    return clave

#print('Generar contraseña')
#print(generar_contra())

def cifrar_contra(mycontra):
    sal = bcrypt.gensalt()
    contra_cifrada = bcrypt.hashpw(mycontra.encode('utf-8'),sal)
    return contra_cifrada

#clave= generar_contra()
#print('Clave Generada: ',clave)
#print('Clave cifrada')
#print(cifrar_contra(clave))

#print("validando")
#print(bcrypt.checkpw(("7tte_7H3_").encode('utf-8'),("$2b$12$Yja028g3p4VPeAAy0gPWsec4i7LMyY8525Fk0EEy8yhnA/I68DUhS").encode('utf-8')))

#Generar el archivo de usuarios:
dicValida={}
def generar_archivo_usuarios():
    contador=0
    #obtener la lista estudiantes
    estudiantes=estudiante()
    usuarios = open("usuarios.txt","w")
    for est in estudiantes:
        c,n = est
        clave = generar_contra()
        claveCif= cifrar_contra(clave)
        registro=c+" "+clave+" "+str(claveCif,'utf-8')+"\n"
        usuarios.write(registro)
        contador+=1
        print(contador)
    print('archivo generado')

#generar_archivo_usuarios()

def estudiante():
    archivo_texto=open("Estudiantes.prn","r")
    lineas_texto=archivo_texto.readlines()
    archivo_texto.close()

    listaux=[]

    conj=set()
    for estu in lineas_texto[0:]:
        i=estu.split('\n')
        s=i[0]
        listaux.append(s[0:8])
        listaux.append(s[8:])
        conj.add(tuple(listaux))
        listaux.clear()
    return conj

def  materias():
    archiv=open("Kardex.txt","r")
    lineas=archiv.readlines()
    archiv.close()
    conjNuev=set()
    listaux =[]
    for estuadv in lineas[0:]:
        dt=estuadv.split('|')
        cd=dt[2].split('\n')
        listaux.append(dt[0])
        listaux.append(dt[1])
        listaux.append(cd[0])
        conjNuev.add(tuple(listaux))
        listaux.clear()
    return conjNuev

dicValida={}
bandera=False

def autenticar_usuario():
    cont=0
    #Obtenemos los datos del archivo Usuarios.txt
    archivo_usuarios=open("usuarios.txt","r")
    alumUsua=archivo_usuarios.readlines()
    archivo_usuarios.close()

    usu=input("Ingresa Usuario: ")
    contra=input("Ingresa clave: ")
    estudiantes =estudiante()
    for estu in estudiantes:
        nc,nm=estu
        if(nm==usu): #Encontramos el usuario
            for usaclav in alumUsua:
                usf=usaclav.split('\n')
                us=usf[0].split(' ')
                if(nc==us[0]): #Encontramos credenciales del alumno
                    if(bcrypt.checkpw((contra).encode('utf-8'),(us[2]).encode('utf-8'))):
                        bandera=True
                        dicValida={
                            "Bandera":bandera,
                            "Usuario":nm,
                            "Mensaje":"Bienvenido al Sistema de Autentificacion de Usuarios"
                         }
                    else: #La Contraseña es incorrecta
                        bandera=False
                        dicValida={
                            "Bandera":bandera,
                            "Usuario":nm,
                            "Mensaje":"Contrasena Incorrecta"
                         }
        else:
            cont+=1

        if (nm!=usu) and (cont==len(estudiantes)) : #No se encontro el usuario
            bandera=False
            dicValida={
                "Bandera":bandera,
                "Usuario":"",
                "Mensaje":"No existe el Usuario"
            }
    return  dicValida




#print(autenticar_usuario())
with open("ValidaUsuario_JSON", 'w') as archivo:
      json.dump( autenticar_usuario(), archivo, indent=4) # dump es disparar