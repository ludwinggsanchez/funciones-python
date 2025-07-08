import random
from flask import jsonify

def function_four():
    # Selecciona una clave aleatoria del diccionario
    clave = random.choice(list(traducciones.keys()))
    traduccion = traducciones.get(clave, "Traducción no encontrada.")
    return jsonify({'message': f'Traducción de "{clave}": {traduccion}'})

traducciones = {
    "hello": "hola",
    "good morning": "buenos días",
    "good night": "buenas noches",
    "how are you": "cómo estás",
    "thank you": "gracias",
    "please": "por favor",
    "goodbye": "adiós",
    "yes": "sí",
    "no": "no",
    "what is your name": "¿cómo te llamas?",
    "my name is": "me llamo",
    "i am fine": "estoy bien",
    "see you later": "hasta luego"
}

def traducir(frase):
    frase = frase.lower().strip()
    return traducciones.get(frase, "Traducción no encontrada.")

if __name__ == "__main__":
    print("Traductor inglés a español. Escriba 'salir' para terminar.")
    while True:
        frase = input("Ingrese una frase en inglés: ")
        if frase.lower().strip() == "salir":
            break
        print("Traducción:", traducir(frase))
