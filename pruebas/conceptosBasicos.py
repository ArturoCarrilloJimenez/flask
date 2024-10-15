import random;

# Se declaran variables directamente, no hay que definir el tipo
nombreVar = 10;
array = [2,3,4];

# Para concadenar texto hay que poner comas, a diferencia de java que si ponemos un + este lo sumara
print('variable 1 ', nombreVar);

position = 0;

# Bucle for que recorre un array, string....
for i in array :
    position += 1;
    print('posicion ', position ,i);

# Entrada de texto
entradaNum = 0;
validator = True;

# Bucle while con una variable centinela
while validator == True :
    try : # Capurador de excepciones (try catch de java)
        entradaNum = int(input(int));
        validator = False;
    except: # En caso de que falle el codigo de la parte superior se ejecutara la excepcion
        print('Introduce un numero entero');

# Condicional con if else
if (entradaNum < 0) :
    print('Este numero es negativo');
elif  entradaNum == 0 : # else if
    print('Este numero es 0');
else :
    print('Este numero es positivo');

print("\nAdivina el numero secreto\n");


# Adivina el numero aleatorio

numAleatorio = random.randint(1,101)

contador = 0;
numIntentos = 10;

while contador < numIntentos :
        
    validator = True;
    # Bucle while con una variable centinela
    while (validator == True) or ((entradaNum < 1) or (entradaNum > 100)) :
        try : # Capurador de excepciones (try catch de java)
            entradaNum = int(input(int));
            validator = False;
            if (entradaNum < 1) or (entradaNum > 100) : # Compruebo que este fuera del rango deseado, si no es asi, muestra un mensaje
                print('Introduce un numero entero entre 1 a 100');
        except: # En caso de que falle el codigo de la parte superior se ejecutara la excepcion
            print('Introduce un numero entero entre 1 a 100');
            validator = True;

    # Coomparo que el numero sea igual a el numero aleatorio
    if numAleatorio == entradaNum:
        print('Felicidades, has adivinado el numero');
        break;
    elif contador == (numIntentos - 1) :
        print('Ya has gastado tus ', contador + 1, ' intentos, el numero secreto era ', numAleatorio);
    else :
        print('No has adivinado el numero secreto');

    contador += 1;