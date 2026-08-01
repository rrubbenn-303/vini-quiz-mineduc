import json
import os

# Definimos la estructura de módulos por asignatura según el horario de Eduhome
modulos_por_asignatura = {
    "Lenguaje": ["Lenguaje y Comunicación", "Taller de Comprensión Lectora", "Reforzamiento de Lenguaje"],
    "Matemática": ["Matemática", "Reforzamiento de Matemática"],
    "Ciencias e Historia": ["Ciencias Naturales", "Historia, Geografía y Ciencias Sociales"],
    "Inglés": ["English", "English With Fun"],
    "Artes y Creatividad": ["Educación Artística", "Teoría Musical", "Interpretación Musical", "Robótica"],
    "Desarrollo Integral": ["Educación Socioemocional", "Taller de Funciones Ejecutivas", "Taller de Movimiento y Coordinación"]
}

# Banco de preguntas (Mock data para 3° Básico)
preguntas_base = [
    # --- Lenguaje ---
    {
        "modulo_eduhome": "Lenguaje y Comunicación",
        "eje": "Lectura",
        "oa": "OA 4",
        "dificultad": "Fácil",
        "pregunta": "¿Cuál de estas palabras es un sustantivo propio?",
        "opciones": ["perro", "Marta", "ciudad", "lápiz"],
        "respuesta_correcta": "Marta",
        "retroalimentacion": "Los sustantivos propios nombran a personas, lugares o mascotas específicas y siempre se escriben con mayúscula inicial."
    },
    {
        "modulo_eduhome": "Lenguaje y Comunicación",
        "eje": "Escritura",
        "oa": "OA 12",
        "dificultad": "Media",
        "pregunta": "¿Qué signo de puntuación se usa para hacer una pregunta?",
        "opciones": ["Punto (.)", "Coma (,)", "Signos de interrogación (¿?)", "Signos de exclamación (¡!)"],
        "respuesta_correcta": "Signos de interrogación (¿?)",
        "retroalimentacion": "Los signos de interrogación (¿?) se utilizan al principio y al final de una oración para indicar que es una pregunta."
    },
    {
        "modulo_eduhome": "Taller de Comprensión Lectora",
        "eje": "Lectura",
        "oa": "OA 4",
        "dificultad": "Media",
        "pregunta": "Si un cuento dice 'Había una vez en un bosque encantado...', ¿de qué parte del cuento estamos hablando?",
        "opciones": ["El final", "El desarrollo", "El inicio", "El título"],
        "respuesta_correcta": "El inicio",
        "retroalimentacion": "El inicio de un cuento suele presentar a los personajes y el lugar donde ocurre la historia."
    },
    {
        "modulo_eduhome": "Reforzamiento de Lenguaje",
        "eje": "Lectura",
        "oa": "OA 2",
        "dificultad": "Fácil",
        "pregunta": "¿Cuántas sílabas tiene la palabra 'Elefante'?",
        "opciones": ["2", "3", "4", "5"],
        "respuesta_correcta": "4",
        "retroalimentacion": "La palabra se divide así: E - le - fan - te. ¡Son 4 sílabas!"
    },

    # --- Matemática ---
    {
        "modulo_eduhome": "Matemática",
        "eje": "Números y Operaciones",
        "oa": "OA 3",
        "dificultad": "Fácil",
        "pregunta": "¿Cuánto es 8 + 5?",
        "opciones": ["12", "13", "14", "15"],
        "respuesta_correcta": "13",
        "retroalimentacion": "Si a 8 le sumas 2 llegas a 10, y te faltan 3 más, así que 10 + 3 = 13."
    },
    {
        "modulo_eduhome": "Matemática",
        "eje": "Geometría",
        "oa": "OA 14",
        "dificultad": "Media",
        "pregunta": "¿Cuántos lados tiene un triángulo?",
        "opciones": ["2", "3", "4", "5"],
        "respuesta_correcta": "3",
        "retroalimentacion": "La palabra 'tri' significa tres, por lo que un triángulo es una figura de 3 lados."
    },
    {
        "modulo_eduhome": "Reforzamiento de Matemática",
        "eje": "Números y Operaciones",
        "oa": "OA 8",
        "dificultad": "Difícil",
        "pregunta": "Si tienes 3 cajas y cada caja tiene 4 manzanas, ¿cuántas manzanas tienes en total?",
        "opciones": ["7", "10", "12", "14"],
        "respuesta_correcta": "12",
        "retroalimentacion": "Puedes sumar 4 + 4 + 4 o multiplicar 3 x 4, lo que da 12 manzanas."
    },

    # --- Ciencias e Historia ---
    {
        "modulo_eduhome": "Ciencias Naturales",
        "eje": "Ciencias de la Vida",
        "oa": "OA 1",
        "dificultad": "Media",
        "pregunta": "¿Qué necesitan las plantas para realizar la fotosíntesis?",
        "opciones": ["Solo agua", "Agua, luz solar y dióxido de carbono", "Azúcar y sal", "Solo tierra"],
        "respuesta_correcta": "Agua, luz solar y dióxido de carbono",
        "retroalimentacion": "Las plantas fabrican su propio alimento usando la luz del sol, el agua que absorben y el aire."
    },
    {
        "modulo_eduhome": "Ciencias Naturales",
        "eje": "Ciencias de la Tierra y el Universo",
        "oa": "OA 11",
        "dificultad": "Fácil",
        "pregunta": "¿Cuál es el planeta en el que vivimos?",
        "opciones": ["Marte", "Venus", "Tierra", "Júpiter"],
        "respuesta_correcta": "Tierra",
        "retroalimentacion": "Vivimos en la Tierra, el tercer planeta desde el Sol."
    },
    {
        "modulo_eduhome": "Historia, Geografía y Ciencias Sociales",
        "eje": "Geografía",
        "oa": "OA 7",
        "dificultad": "Fácil",
        "pregunta": "¿En qué continente se encuentra Chile?",
        "opciones": ["Europa", "Asia", "África", "América"],
        "respuesta_correcta": "América",
        "retroalimentacion": "Chile está ubicado en América del Sur."
    },

    # --- Inglés ---
    {
        "modulo_eduhome": "English",
        "eje": "Vocabulario",
        "oa": "OA 1",
        "dificultad": "Fácil",
        "pregunta": "¿Cómo se dice 'Rojo' en inglés?",
        "opciones": ["Blue", "Green", "Red", "Yellow"],
        "respuesta_correcta": "Red",
        "retroalimentacion": "El color rojo en inglés se dice 'Red'."
    },
    {
        "modulo_eduhome": "English With Fun",
        "eje": "Vocabulario",
        "oa": "OA 2",
        "dificultad": "Media",
        "pregunta": "¿Qué animal es un 'Dog'?",
        "opciones": ["Gato", "Perro", "Caballo", "Pájaro"],
        "respuesta_correcta": "Perro",
        "retroalimentacion": "'Dog' es la palabra en inglés para 'Perro'."
    },

    # --- Artes y Creatividad ---
    {
        "modulo_eduhome": "Educación Artística",
        "eje": "Creación",
        "oa": "OA 1",
        "dificultad": "Fácil",
        "pregunta": "¿Cuáles son los colores primarios?",
        "opciones": ["Verde, Morado, Naranja", "Blanco, Negro, Gris", "Rojo, Azul, Amarillo", "Rosa, Celeste, Lila"],
        "respuesta_correcta": "Rojo, Azul, Amarillo",
        "retroalimentacion": "Los colores primarios son el rojo, el azul y el amarillo; a partir de ellos se pueden crear los demás colores."
    },
    {
        "modulo_eduhome": "Teoría Musical",
        "eje": "Apreciación",
        "oa": "OA 3",
        "dificultad": "Media",
        "pregunta": "¿Qué instrumento tiene teclas blancas y negras?",
        "opciones": ["Guitarra", "Batería", "Piano", "Flauta"],
        "respuesta_correcta": "Piano",
        "retroalimentacion": "El piano es un instrumento de teclado que tiene teclas blancas y negras para tocar diferentes notas."
    },
    {
        "modulo_eduhome": "Interpretación Musical",
        "eje": "Apreciación",
        "oa": "OA 4",
        "dificultad": "Fácil",
        "pregunta": "¿Con qué parte del cuerpo aplaudimos al ritmo de la música?",
        "opciones": ["Los pies", "Las manos", "La cabeza", "Los hombros"],
        "respuesta_correcta": "Las manos",
        "retroalimentacion": "¡Usamos las manos para aplaudir y seguir el ritmo!"
    },
    {
        "modulo_eduhome": "Robótica",
        "eje": "Tecnología",
        "oa": "OA 1",
        "dificultad": "Difícil",
        "pregunta": "¿Qué le dice al robot lo que tiene que hacer?",
        "opciones": ["Un motor", "Un código o programa", "Una rueda", "Un cable"],
        "respuesta_correcta": "Un código o programa",
        "retroalimentacion": "Los robots siguen las instrucciones que los humanos escriben en forma de código o programas."
    },

    # --- Desarrollo Integral ---
    {
        "modulo_eduhome": "Educación Socioemocional",
        "eje": "Autoconocimiento",
        "oa": "OA 1",
        "dificultad": "Fácil",
        "pregunta": "¿Qué emoción sientes cuando te dan un regalo sorpresa que te gusta mucho?",
        "opciones": ["Tristeza", "Miedo", "Alegría", "Enojo"],
        "respuesta_correcta": "Alegría",
        "retroalimentacion": "La alegría es una emoción positiva que sentimos cuando ocurren cosas buenas y divertidas."
    },
    {
        "modulo_eduhome": "Taller de Funciones Ejecutivas",
        "eje": "Organización",
        "oa": "OA 2",
        "dificultad": "Media",
        "pregunta": "Si tienes que hacer la tarea, jugar y cenar, ¿qué es mejor hacer primero?",
        "opciones": ["Jugar sin parar", "La tarea, luego jugar y después cenar", "No cenar y jugar", "Empezar la tarea y no terminarla"],
        "respuesta_correcta": "La tarea, luego jugar y después cenar",
        "retroalimentacion": "Organizar tu tiempo haciendo primero las responsabilidades como la tarea te deja libre para disfrutar jugando y luego cenar tranquilo."
    },
    {
        "modulo_eduhome": "Taller de Movimiento y Coordinación",
        "eje": "Motricidad",
        "oa": "OA 3",
        "dificultad": "Fácil",
        "pregunta": "¿Qué haces cuando saltas la cuerda?",
        "opciones": ["Duermes", "Mueves los pies y las manos coordinadamente", "Te quedas quieto", "Cantas bajito"],
        "respuesta_correcta": "Mueves los pies y las manos coordinadamente",
        "retroalimentacion": "Saltar la cuerda requiere mover las manos para girar la cuerda y saltar con los pies al mismo tiempo. ¡Es un excelente ejercicio de coordinación!"
    }
]

def main():
    preguntas_finales = []
    contador_id = 1

    # Procesar y mapear las preguntas
    for p in preguntas_base:
        # Encontrar la asignatura basada en el modulo
        asignatura_encontrada = "Desconocida"
        for asig, mods in modulos_por_asignatura.items():
            if p["modulo_eduhome"] in mods:
                asignatura_encontrada = asig
                break

        pregunta_completa = {
            "id": contador_id,
            "asignatura": asignatura_encontrada,
            "modulo_eduhome": p["modulo_eduhome"],
            "eje": p["eje"],
            "oa": p["oa"],
            "dificultad": p["dificultad"],
            "pregunta": p["pregunta"],
            "opciones": p["opciones"],
            "respuesta_correcta": p["respuesta_correcta"],
            "retroalimentacion": p["retroalimentacion"]
        }
        preguntas_finales.append(pregunta_completa)
        contador_id += 1

    # Guardar en JSON
    directorio = "data"
    if not os.path.exists(directorio):
        os.makedirs(directorio)

    ruta_archivo = os.path.join(directorio, "preguntas.json")
    with open(ruta_archivo, 'w', encoding='utf-8') as f:
        json.dump(preguntas_finales, f, ensure_ascii=False, indent=4)

    print(f"✅ Se han generado exitosamente {len(preguntas_finales)} preguntas de prueba.")
    print(f"📂 Archivo guardado en: {ruta_archivo}")

if __name__ == "__main__":
    main()
