import json
import os

modulos_por_asignatura = {
    "Lenguaje": ["Lenguaje y Comunicación", "Taller de Comprensión Lectora", "Reforzamiento de Lenguaje"],
    "Matemática": ["Matemática", "Reforzamiento de Matemática"],
    "Ciencias e Historia": ["Ciencias Naturales", "Historia, Geografía y Ciencias Sociales"],
    "Inglés": ["English", "English With Fun"],
    "Artes y Creatividad": ["Educación Artística", "Teoría Musical", "Interpretación Musical", "Robótica"],
    "Desarrollo Integral": ["Educación Socioemocional", "Taller de Funciones Ejecutivas", "Taller de Movimiento y Coordinación"]
}

preguntas_base = [
    # --- Lenguaje y Comunicación (min 5) ---
    {"modulo_eduhome": "Lenguaje y Comunicación", "eje": "Lectura", "oa": "OA 4", "dificultad": "Fácil", "pregunta": "¿Cuál de estas palabras es un sustantivo propio?", "opciones": ["perro", "Marta", "ciudad", "lápiz"], "respuesta_correcta": "Marta", "retroalimentacion": "Los sustantivos propios nombran a personas, lugares o mascotas específicas y siempre se escriben con mayúscula inicial."},
    {"modulo_eduhome": "Lenguaje y Comunicación", "eje": "Escritura", "oa": "OA 12", "dificultad": "Media", "pregunta": "¿Qué signo de puntuación se usa para hacer una pregunta?", "opciones": ["Punto (.)", "Coma (,)", "Signos de interrogación (¿?)", "Signos de exclamación (¡!)"], "respuesta_correcta": "Signos de interrogación (¿?)", "retroalimentacion": "Los signos de interrogación se utilizan al principio y al final para indicar una pregunta."},
    {"modulo_eduhome": "Lenguaje y Comunicación", "eje": "Lectura", "oa": "OA 2", "dificultad": "Fácil", "pregunta": "¿Qué palabra es un adjetivo?", "opciones": ["correr", "hermoso", "mesa", "ayer"], "respuesta_correcta": "hermoso", "retroalimentacion": "Los adjetivos describen características de los sustantivos, como 'hermoso'."},
    {"modulo_eduhome": "Lenguaje y Comunicación", "eje": "Escritura", "oa": "OA 12", "dificultad": "Media", "pregunta": "¿Dónde se usa el punto y aparte?", "opciones": ["Para separar palabras", "Al final de una oración", "Al final de un párrafo", "Para hacer una pregunta"], "respuesta_correcta": "Al final de un párrafo", "retroalimentacion": "El punto y aparte marca el final de un párrafo y separa ideas distintas."},
    {"modulo_eduhome": "Lenguaje y Comunicación", "eje": "Comunicación Oral", "oa": "OA 27", "dificultad": "Fácil", "pregunta": "Cuando alguien expone sobre un tema, tú debes...", "opciones": ["Gritar", "Escuchar con atención", "Dormir", "Jugar con el lápiz"], "respuesta_correcta": "Escuchar con atención", "retroalimentacion": "Escuchar con atención demuestra respeto hacia la persona que está hablando."},

    # --- Taller de Comprensión Lectora (min 5) ---
    {"modulo_eduhome": "Taller de Comprensión Lectora", "eje": "Lectura", "oa": "OA 4", "dificultad": "Media", "pregunta": "Si un cuento dice 'Había una vez en un bosque encantado...', ¿de qué parte del cuento estamos hablando?", "opciones": ["El final", "El desarrollo", "El inicio", "El título"], "respuesta_correcta": "El inicio", "retroalimentacion": "El inicio presenta a los personajes y el lugar donde ocurre la historia."},
    {"modulo_eduhome": "Taller de Comprensión Lectora", "eje": "Lectura", "oa": "OA 4", "dificultad": "Fácil", "pregunta": "En el cuento de Caperucita Roja, ¿quién es el personaje principal?", "opciones": ["El lobo", "La abuelita", "Caperucita Roja", "El cazador"], "respuesta_correcta": "Caperucita Roja", "retroalimentacion": "El personaje principal es el más importante de la historia."},
    {"modulo_eduhome": "Taller de Comprensión Lectora", "eje": "Lectura", "oa": "OA 4", "dificultad": "Media", "pregunta": "¿Qué es la moraleja de una fábula?", "opciones": ["El título", "El dibujo", "Una enseñanza o lección", "El autor"], "respuesta_correcta": "Una enseñanza o lección", "retroalimentacion": "Las fábulas siempre dejan una enseñanza llamada moraleja al final."},
    {"modulo_eduhome": "Taller de Comprensión Lectora", "eje": "Lectura", "oa": "OA 3", "dificultad": "Difícil", "pregunta": "Si el texto dice 'Las nubes estaban oscuras y se escuchaban truenos', ¿qué podemos inferir?", "opciones": ["Que va a salir el sol", "Que es de noche", "Que va a llover fuerte", "Que es primavera"], "respuesta_correcta": "Que va a llover fuerte", "retroalimentacion": "Inferir es usar pistas del texto para descubrir algo que no está escrito directamente."},
    {"modulo_eduhome": "Taller de Comprensión Lectora", "eje": "Lectura", "oa": "OA 4", "dificultad": "Fácil", "pregunta": "¿Qué tipo de texto es una receta de cocina?", "opciones": ["Texto poético", "Texto instructivo", "Cuento", "Noticia"], "respuesta_correcta": "Texto instructivo", "retroalimentacion": "Las recetas dan instrucciones paso a paso para preparar algo."},

    # --- Reforzamiento de Lenguaje (min 5) ---
    {"modulo_eduhome": "Reforzamiento de Lenguaje", "eje": "Lectura", "oa": "OA 2", "dificultad": "Fácil", "pregunta": "¿Cuántas sílabas tiene la palabra 'Elefante'?", "opciones": ["2", "3", "4", "5"], "respuesta_correcta": "4", "retroalimentacion": "La palabra se divide así: E - le - fan - te."},
    {"modulo_eduhome": "Reforzamiento de Lenguaje", "eje": "Lectura", "oa": "OA 2", "dificultad": "Fácil", "pregunta": "¿Cuál es la letra inicial de 'Sol'?", "opciones": ["A", "S", "M", "L"], "respuesta_correcta": "S", "retroalimentacion": "La palabra Sol comienza con la letra S."},
    {"modulo_eduhome": "Reforzamiento de Lenguaje", "eje": "Escritura", "oa": "OA 12", "dificultad": "Media", "pregunta": "Identifica la palabra escrita correctamente:", "opciones": ["Hárbol", "Árbol", "Harbol", "Arvol"], "respuesta_correcta": "Árbol", "retroalimentacion": "La palabra correcta es 'Árbol' y lleva tilde por ser grave terminada en 'l'."},
    {"modulo_eduhome": "Reforzamiento de Lenguaje", "eje": "Lectura", "oa": "OA 2", "dificultad": "Media", "pregunta": "¿Qué rima con 'gato'?", "opciones": ["Perro", "Ratón", "Zapato", "Casa"], "respuesta_correcta": "Zapato", "retroalimentacion": "Gato y zapato terminan con el mismo sonido '-ato'."},
    {"modulo_eduhome": "Reforzamiento de Lenguaje", "eje": "Escritura", "oa": "OA 12", "dificultad": "Fácil", "pregunta": "Las oraciones siempre deben comenzar con...", "opciones": ["Un dibujo", "Punto final", "Mayúscula", "Una coma"], "respuesta_correcta": "Mayúscula", "retroalimentacion": "La regla general de escritura es empezar toda oración con letra mayúscula."},

    # --- Matemática (min 5) ---
    {"modulo_eduhome": "Matemática", "eje": "Números y Operaciones", "oa": "OA 3", "dificultad": "Fácil", "pregunta": "¿Cuánto es 8 + 5?", "opciones": ["12", "13", "14", "15"], "respuesta_correcta": "13", "retroalimentacion": "8 más 2 es 10, y te faltan 3 más, así que 10 + 3 = 13."},
    {"modulo_eduhome": "Matemática", "eje": "Geometría", "oa": "OA 14", "dificultad": "Media", "pregunta": "¿Cuántos lados tiene un triángulo?", "opciones": ["2", "3", "4", "5"], "respuesta_correcta": "3", "retroalimentacion": "La palabra 'tri' significa tres, por lo que un triángulo es una figura de 3 lados."},
    {"modulo_eduhome": "Matemática", "eje": "Números y Operaciones", "oa": "OA 1", "dificultad": "Media", "pregunta": "¿Qué número viene después del 199?", "opciones": ["100", "200", "198", "201"], "respuesta_correcta": "200", "retroalimentacion": "Después de contar hasta el 99, pasamos a la siguiente centena, que es el 200."},
    {"modulo_eduhome": "Matemática", "eje": "Medición", "oa": "OA 19", "dificultad": "Fácil", "pregunta": "Si el reloj pequeño marca las 3 y el reloj grande marca las 12, ¿qué hora es?", "opciones": ["Las 12", "Las 3 en punto", "Las 3 y media", "Las 4"], "respuesta_correcta": "Las 3 en punto", "retroalimentacion": "La manecilla pequeña indica la hora y la grande en el 12 indica que son 'en punto'."},
    {"modulo_eduhome": "Matemática", "eje": "Números y Operaciones", "oa": "OA 9", "dificultad": "Difícil", "pregunta": "¿Cuál es la mitad de 10?", "opciones": ["2", "4", "5", "8"], "respuesta_correcta": "5", "retroalimentacion": "Si tienes 10 dulces y los divides en 2 partes iguales, cada parte tiene 5 dulces."},

    # --- Reforzamiento de Matemática (min 5) ---
    {"modulo_eduhome": "Reforzamiento de Matemática", "eje": "Números y Operaciones", "oa": "OA 8", "dificultad": "Difícil", "pregunta": "Si tienes 3 cajas y cada caja tiene 4 manzanas, ¿cuántas manzanas tienes en total?", "opciones": ["7", "10", "12", "14"], "respuesta_correcta": "12", "retroalimentacion": "Puedes sumar 4 + 4 + 4 o multiplicar 3 x 4, lo que da 12 manzanas."},
    {"modulo_eduhome": "Reforzamiento de Matemática", "eje": "Números y Operaciones", "oa": "OA 2", "dificultad": "Fácil", "pregunta": "¿Cuánto es 10 - 4?", "opciones": ["4", "5", "6", "7"], "respuesta_correcta": "6", "retroalimentacion": "Si a 10 le quitas 4, te quedan 6."},
    {"modulo_eduhome": "Reforzamiento de Matemática", "eje": "Números y Operaciones", "oa": "OA 3", "dificultad": "Media", "pregunta": "¿Cuál es el resultado de 15 + 15?", "opciones": ["20", "25", "30", "35"], "respuesta_correcta": "30", "retroalimentacion": "10 + 10 son 20, y 5 + 5 son 10. Sumando ambos da 30."},
    {"modulo_eduhome": "Reforzamiento de Matemática", "eje": "Números y Operaciones", "oa": "OA 8", "dificultad": "Media", "pregunta": "Calcula: 2 x 5", "opciones": ["5", "7", "10", "12"], "respuesta_correcta": "10", "retroalimentacion": "Sumar 5 dos veces da como resultado 10."},
    {"modulo_eduhome": "Reforzamiento de Matemática", "eje": "Patrones y Álgebra", "oa": "OA 12", "dificultad": "Difícil", "pregunta": "Completa la secuencia: 2, 4, 6, 8, ___", "opciones": ["9", "10", "12", "14"], "respuesta_correcta": "10", "retroalimentacion": "La secuencia avanza de 2 en 2, sumando 2 al último número: 8 + 2 = 10."},

    # --- Ciencias Naturales (min 5) ---
    {"modulo_eduhome": "Ciencias Naturales", "eje": "Ciencias de la Vida", "oa": "OA 1", "dificultad": "Media", "pregunta": "¿Qué necesitan las plantas para realizar la fotosíntesis?", "opciones": ["Solo agua", "Agua, luz solar y dióxido de carbono", "Azúcar y sal", "Solo tierra"], "respuesta_correcta": "Agua, luz solar y dióxido de carbono", "retroalimentacion": "Las plantas fabrican su propio alimento usando la luz, agua y aire."},
    {"modulo_eduhome": "Ciencias Naturales", "eje": "Ciencias de la Tierra y el Universo", "oa": "OA 11", "dificultad": "Fácil", "pregunta": "¿Cuál es el planeta en el que vivimos?", "opciones": ["Marte", "Venus", "Tierra", "Júpiter"], "respuesta_correcta": "Tierra", "retroalimentacion": "Vivimos en la Tierra, el tercer planeta desde el Sol."},
    {"modulo_eduhome": "Ciencias Naturales", "eje": "Ciencias Físicas", "oa": "OA 8", "dificultad": "Media", "pregunta": "¿Cuál de estos materiales es transparente?", "opciones": ["Madera", "Metal", "Vidrio", "Piedra"], "respuesta_correcta": "Vidrio", "retroalimentacion": "El vidrio permite que la luz pase a través de él."},
    {"modulo_eduhome": "Ciencias Naturales", "eje": "Ciencias de la Vida", "oa": "OA 6", "dificultad": "Fácil", "pregunta": "¿Qué animal es un mamífero?", "opciones": ["Pez", "Gallina", "Perro", "Mosca"], "respuesta_correcta": "Perro", "retroalimentacion": "Los mamíferos, como los perros, nacen del vientre de la madre y toman leche."},
    {"modulo_eduhome": "Ciencias Naturales", "eje": "Ciencias Físicas", "oa": "OA 9", "dificultad": "Difícil", "pregunta": "¿Qué pasa si calentamos mucho el hielo?", "opciones": ["Se vuelve más duro", "Se derrite y se vuelve líquido", "Desaparece", "Se convierte en piedra"], "respuesta_correcta": "Se derrite y se vuelve líquido", "retroalimentacion": "El calor hace que el agua en estado sólido (hielo) pase a estado líquido."},

    # --- Historia, Geografía y Ciencias Sociales (min 5) ---
    {"modulo_eduhome": "Historia, Geografía y Ciencias Sociales", "eje": "Geografía", "oa": "OA 7", "dificultad": "Fácil", "pregunta": "¿En qué continente se encuentra Chile?", "opciones": ["Europa", "Asia", "África", "América"], "respuesta_correcta": "América", "retroalimentacion": "Chile está ubicado en América del Sur."},
    {"modulo_eduhome": "Historia, Geografía y Ciencias Sociales", "eje": "Geografía", "oa": "OA 8", "dificultad": "Media", "pregunta": "¿Cuál es la capital de Chile?", "opciones": ["Valparaíso", "Concepción", "Santiago", "Antofagasta"], "respuesta_correcta": "Santiago", "retroalimentacion": "Santiago es la ciudad capital de Chile."},
    {"modulo_eduhome": "Historia, Geografía y Ciencias Sociales", "eje": "Historia", "oa": "OA 1", "dificultad": "Fácil", "pregunta": "¿Quiénes vivían en Chile antes de la llegada de los españoles?", "opciones": ["Solo dinosaurios", "Los pueblos originarios", "Nadie", "Los ingleses"], "respuesta_correcta": "Los pueblos originarios", "retroalimentacion": "Los pueblos originarios, como los Mapuches y Aymaras, habitaban este territorio."},
    {"modulo_eduhome": "Historia, Geografía y Ciencias Sociales", "eje": "Geografía", "oa": "OA 7", "dificultad": "Media", "pregunta": "¿Qué gran océano baña las costas de Chile?", "opciones": ["Océano Atlántico", "Océano Índico", "Océano Pacífico", "Océano Ártico"], "respuesta_correcta": "Océano Pacífico", "retroalimentacion": "Todo el largo de Chile limita al oeste con el Océano Pacífico."},
    {"modulo_eduhome": "Historia, Geografía y Ciencias Sociales", "eje": "Formación Ciudadana", "oa": "OA 11", "dificultad": "Difícil", "pregunta": "¿Por qué son importantes las normas de convivencia en la sala de clases?", "opciones": ["Para tener más recreos", "Para que todos se respeten y aprendan mejor", "Para pintar las paredes", "Para no hacer tareas"], "respuesta_correcta": "Para que todos se respeten y aprendan mejor", "retroalimentacion": "Las normas nos ayudan a mantener el respeto y el orden."},

    # --- English (min 5) ---
    {"modulo_eduhome": "English", "eje": "Vocabulario", "oa": "OA 1", "dificultad": "Fácil", "pregunta": "¿Cómo se dice 'Rojo' en inglés?", "opciones": ["Blue", "Green", "Red", "Yellow"], "respuesta_correcta": "Red", "retroalimentacion": "El color rojo se dice 'Red'."},
    {"modulo_eduhome": "English", "eje": "Vocabulario", "oa": "OA 1", "dificultad": "Fácil", "pregunta": "¿Cómo se dice 'Hola' en inglés?", "opciones": ["Goodbye", "Hello", "Please", "Thank you"], "respuesta_correcta": "Hello", "retroalimentacion": "Hola en inglés es 'Hello'."},
    {"modulo_eduhome": "English", "eje": "Gramática", "oa": "OA 3", "dificultad": "Media", "pregunta": "¿Qué significa 'My name is...'?", "opciones": ["Me gusta...", "Yo tengo...", "Mi nombre es...", "Yo soy..."], "respuesta_correcta": "Mi nombre es...", "retroalimentacion": "Esta frase se usa para presentarse."},
    {"modulo_eduhome": "English", "eje": "Vocabulario", "oa": "OA 1", "dificultad": "Media", "pregunta": "¿Cuál de estos es un número en inglés?", "opciones": ["Apple", "Book", "Seven", "Cat"], "respuesta_correcta": "Seven", "retroalimentacion": "Seven es el número 7."},
    {"modulo_eduhome": "English", "eje": "Vocabulario", "oa": "OA 2", "dificultad": "Fácil", "pregunta": "¿Qué animal es 'Cat'?", "opciones": ["Perro", "Gato", "Pájaro", "Pez"], "respuesta_correcta": "Gato", "retroalimentacion": "Cat significa Gato."},

    # --- English With Fun (min 5) ---
    {"modulo_eduhome": "English With Fun", "eje": "Vocabulario", "oa": "OA 2", "dificultad": "Media", "pregunta": "¿Qué animal es un 'Dog'?", "opciones": ["Gato", "Perro", "Caballo", "Pájaro"], "respuesta_correcta": "Perro", "retroalimentacion": "'Dog' es la palabra en inglés para 'Perro'."},
    {"modulo_eduhome": "English With Fun", "eje": "Vocabulario", "oa": "OA 1", "dificultad": "Fácil", "pregunta": "¿Qué color es 'Blue'?", "opciones": ["Rojo", "Azul", "Amarillo", "Verde"], "respuesta_correcta": "Azul", "retroalimentacion": "Blue es el color Azul."},
    {"modulo_eduhome": "English With Fun", "eje": "Vocabulario", "oa": "OA 3", "dificultad": "Media", "pregunta": "¿Qué parte del cuerpo es 'Head'?", "opciones": ["Mano", "Pie", "Cabeza", "Ojo"], "respuesta_correcta": "Cabeza", "retroalimentacion": "Head significa Cabeza."},
    {"modulo_eduhome": "English With Fun", "eje": "Vocabulario", "oa": "OA 2", "dificultad": "Media", "pregunta": "¿Qué comida es 'Apple'?", "opciones": ["Plátano", "Manzana", "Naranja", "Uva"], "respuesta_correcta": "Manzana", "retroalimentacion": "Apple es una Manzana."},
    {"modulo_eduhome": "English With Fun", "eje": "Expresión", "oa": "OA 4", "dificultad": "Difícil", "pregunta": "Si estás feliz, puedes decir: 'I am...'", "opciones": ["Sad", "Angry", "Happy", "Tired"], "respuesta_correcta": "Happy", "retroalimentacion": "Happy significa Feliz."},

    # --- Educación Artística (min 5) ---
    {"modulo_eduhome": "Educación Artística", "eje": "Creación", "oa": "OA 1", "dificultad": "Fácil", "pregunta": "¿Cuáles son los colores primarios?", "opciones": ["Verde, Morado, Naranja", "Blanco, Negro, Gris", "Rojo, Azul, Amarillo", "Rosa, Celeste, Lila"], "respuesta_correcta": "Rojo, Azul, Amarillo", "retroalimentacion": "Los colores primarios son el rojo, el azul y el amarillo."},
    {"modulo_eduhome": "Educación Artística", "eje": "Creación", "oa": "OA 2", "dificultad": "Media", "pregunta": "¿Qué color obtienes si mezclas rojo y amarillo?", "opciones": ["Verde", "Naranja", "Morado", "Café"], "respuesta_correcta": "Naranja", "retroalimentacion": "La mezcla de rojo y amarillo crea el color naranja."},
    {"modulo_eduhome": "Educación Artística", "eje": "Materiales", "oa": "OA 3", "dificultad": "Fácil", "pregunta": "¿Con qué material puedes modelar figuras 3D?", "opciones": ["Agua", "Lápiz", "Greda o Plasticina", "Papel"], "respuesta_correcta": "Greda o Plasticina", "retroalimentacion": "La plasticina nos permite crear objetos con volumen."},
    {"modulo_eduhome": "Educación Artística", "eje": "Apreciación", "oa": "OA 4", "dificultad": "Media", "pregunta": "¿Qué hace un escultor?", "opciones": ["Pinta cuadros", "Canta", "Crea estatuas y figuras", "Escribe poemas"], "respuesta_correcta": "Crea estatuas y figuras", "retroalimentacion": "Un escultor moldea o talla materiales para crear arte."},
    {"modulo_eduhome": "Educación Artística", "eje": "Creación", "oa": "OA 1", "dificultad": "Difícil", "pregunta": "¿Qué son las texturas visuales?", "opciones": ["Cosas que hacen ruido", "Dibujos que parecen tener volumen o rugosidad pero son planos", "La música de un video", "El olor de la pintura"], "respuesta_correcta": "Dibujos que parecen tener volumen o rugosidad pero son planos", "retroalimentacion": "Las texturas visuales engañan al ojo para que parezca que se pueden sentir."},

    # --- Teoría Musical (min 5) ---
    {"modulo_eduhome": "Teoría Musical", "eje": "Apreciación", "oa": "OA 3", "dificultad": "Media", "pregunta": "¿Qué instrumento tiene teclas blancas y negras?", "opciones": ["Guitarra", "Batería", "Piano", "Flauta"], "respuesta_correcta": "Piano", "retroalimentacion": "El piano tiene un teclado con teclas blancas y negras."},
    {"modulo_eduhome": "Teoría Musical", "eje": "Lenguaje Musical", "oa": "OA 1", "dificultad": "Fácil", "pregunta": "¿Cuántas líneas tiene un pentagrama?", "opciones": ["3", "4", "5", "6"], "respuesta_correcta": "5", "retroalimentacion": "Penta significa cinco, así que el pentagrama tiene 5 líneas."},
    {"modulo_eduhome": "Teoría Musical", "eje": "Lenguaje Musical", "oa": "OA 1", "dificultad": "Media", "pregunta": "¿Cuál de estas es una nota musical?", "opciones": ["Sol", "Luna", "Estrella", "Nube"], "respuesta_correcta": "Sol", "retroalimentacion": "Las notas son Do, Re, Mi, Fa, Sol, La, Si."},
    {"modulo_eduhome": "Teoría Musical", "eje": "Lenguaje Musical", "oa": "OA 2", "dificultad": "Difícil", "pregunta": "¿Qué símbolo se pone al principio del pentagrama?", "opciones": ["Una letra A", "La llave de Sol", "Un número 1", "Un punto"], "respuesta_correcta": "La llave de Sol", "retroalimentacion": "La llave de Sol indica cómo se leerán las notas."},
    {"modulo_eduhome": "Teoría Musical", "eje": "Cualidades del Sonido", "oa": "OA 3", "dificultad": "Media", "pregunta": "¿Qué cualidad diferencia un sonido fuerte de uno suave?", "opciones": ["La altura", "La intensidad (volumen)", "La duración", "El timbre"], "respuesta_correcta": "La intensidad (volumen)", "retroalimentacion": "La intensidad nos dice si el sonido es muy fuerte o muy suavecito."},

    # --- Interpretación Musical (min 5) ---
    {"modulo_eduhome": "Interpretación Musical", "eje": "Apreciación", "oa": "OA 4", "dificultad": "Fácil", "pregunta": "¿Con qué parte del cuerpo aplaudimos al ritmo de la música?", "opciones": ["Los pies", "Las manos", "La cabeza", "Los hombros"], "respuesta_correcta": "Las manos", "retroalimentacion": "Usamos las manos para aplaudir."},
    {"modulo_eduhome": "Interpretación Musical", "eje": "Canto", "oa": "OA 4", "dificultad": "Fácil", "pregunta": "¿Qué usamos para cantar?", "opciones": ["Nuestra voz", "Los pies", "Los ojos", "Las orejas"], "respuesta_correcta": "Nuestra voz", "retroalimentacion": "La voz es nuestro instrumento musical natural."},
    {"modulo_eduhome": "Interpretación Musical", "eje": "Interpretación", "oa": "OA 5", "dificultad": "Media", "pregunta": "¿Qué es un coro?", "opciones": ["Un solo cantante", "Un grupo de personas cantando juntas", "Una guitarra sola", "Un baile"], "respuesta_correcta": "Un grupo de personas cantando juntas", "retroalimentacion": "Un coro está formado por muchas voces cantando a la vez."},
    {"modulo_eduhome": "Interpretación Musical", "eje": "Instrumentos", "oa": "OA 6", "dificultad": "Media", "pregunta": "¿Cómo se toca un tambor?", "opciones": ["Soplando", "Golpeándolo o percutiendo", "Frotando cuerdas", "Apretando teclas"], "respuesta_correcta": "Golpeándolo o percutiendo", "retroalimentacion": "El tambor es un instrumento de percusión."},
    {"modulo_eduhome": "Interpretación Musical", "eje": "Interpretación", "oa": "OA 5", "dificultad": "Difícil", "pregunta": "Cuando sigues el 'pulso' de una canción, estás...", "opciones": ["Durmiendo", "Marcando el latido constante de la música", "Cantando muy alto", "Tocando la flauta"], "respuesta_correcta": "Marcando el latido constante de la música", "retroalimentacion": "El pulso es como el latido del corazón de una canción."},

    # --- Robótica (min 5) ---
    {"modulo_eduhome": "Robótica", "eje": "Tecnología", "oa": "OA 1", "dificultad": "Difícil", "pregunta": "¿Qué le dice al robot lo que tiene que hacer?", "opciones": ["Un motor", "Un código o programa", "Una rueda", "Un cable"], "respuesta_correcta": "Un código o programa", "retroalimentacion": "Los robots siguen instrucciones escritas en forma de código."},
    {"modulo_eduhome": "Robótica", "eje": "Componentes", "oa": "OA 2", "dificultad": "Media", "pregunta": "¿Qué parte de un robot le permite moverse?", "opciones": ["La batería", "Los sensores", "Los motores y ruedas", "Las luces"], "respuesta_correcta": "Los motores y ruedas", "retroalimentacion": "Los motores convierten la energía en movimiento para las ruedas o brazos."},
    {"modulo_eduhome": "Robótica", "eje": "Sensores", "oa": "OA 3", "dificultad": "Difícil", "pregunta": "¿Cómo puede un robot 'ver' u 'oír'?", "opciones": ["Con ojos humanos", "Adivinando", "Usando sensores", "Con un reloj"], "respuesta_correcta": "Usando sensores", "retroalimentacion": "Los sensores le dan información del entorno (luz, distancia, sonido)."},
    {"modulo_eduhome": "Robótica", "eje": "Conceptos", "oa": "OA 1", "dificultad": "Fácil", "pregunta": "¿Qué necesita un robot para tener energía?", "opciones": ["Agua", "Baterías o electricidad", "Comida", "Sol solamente"], "respuesta_correcta": "Baterías o electricidad", "retroalimentacion": "Las máquinas electrónicas funcionan con energía eléctrica."},
    {"modulo_eduhome": "Robótica", "eje": "Programación", "oa": "OA 4", "dificultad": "Media", "pregunta": "En programación, ¿qué es un 'Bug'?", "opciones": ["Un insecto de verdad", "Un error en el código", "Una función nueva", "El nombre del robot"], "respuesta_correcta": "Un error en el código", "retroalimentacion": "Cuando el programa falla, se dice que tiene un 'bug' (error)."},

    # --- Educación Socioemocional (min 5) ---
    {"modulo_eduhome": "Educación Socioemocional", "eje": "Autoconocimiento", "oa": "OA 1", "dificultad": "Fácil", "pregunta": "¿Qué emoción sientes cuando te dan un regalo sorpresa que te gusta mucho?", "opciones": ["Tristeza", "Miedo", "Alegría", "Enojo"], "respuesta_correcta": "Alegría", "retroalimentacion": "La alegría es una emoción positiva que sentimos cuando ocurren cosas buenas."},
    {"modulo_eduhome": "Educación Socioemocional", "eje": "Empatía", "oa": "OA 2", "dificultad": "Media", "pregunta": "Si un compañero se cae y llora, ¿qué es lo más empático que puedes hacer?", "opciones": ["Reírte", "Ignorarlo", "Preguntarle si está bien y ayudarlo", "Empujarlo"], "respuesta_correcta": "Preguntarle si está bien y ayudarlo", "retroalimentacion": "La empatía es entender lo que siente el otro y apoyarlo."},
    {"modulo_eduhome": "Educación Socioemocional", "eje": "Regulación", "oa": "OA 3", "dificultad": "Fácil", "pregunta": "Cuando estás muy enojado, ¿qué puedes hacer para calmarte?", "opciones": ["Gritar fuerte", "Respirar profundo y contar hasta 10", "Romper cosas", "Pegarle a la pared"], "respuesta_correcta": "Respirar profundo y contar hasta 10", "retroalimentacion": "Respirar hondo ayuda a que tu cuerpo y mente se relajen."},
    {"modulo_eduhome": "Educación Socioemocional", "eje": "Resolución de conflictos", "oa": "OA 4", "dificultad": "Media", "pregunta": "Si tú y tu amigo quieren jugar juegos distintos, ¿cuál es la mejor solución?", "opciones": ["Pelear", "No jugar más", "Llegar a un acuerdo y jugar un rato cada uno", "Obligarlo a jugar el tuyo"], "respuesta_correcta": "Llegar a un acuerdo y jugar un rato cada uno", "retroalimentacion": "Llegar a un acuerdo es la mejor forma de resolver un conflicto pacíficamente."},
    {"modulo_eduhome": "Educación Socioemocional", "eje": "Autoconcepto", "oa": "OA 1", "dificultad": "Difícil", "pregunta": "¿Qué significa tener buena autoestima?", "opciones": ["Creer que eres mejor que todos", "Quererte y aceptarte como eres", "Estar siempre triste", "No hablar con nadie"], "respuesta_correcta": "Quererte y aceptarte como eres", "retroalimentacion": "La autoestima es el aprecio y amor que te tienes a ti mismo."},

    # --- Taller de Funciones Ejecutivas (min 5) ---
    {"modulo_eduhome": "Taller de Funciones Ejecutivas", "eje": "Organización", "oa": "OA 2", "dificultad": "Media", "pregunta": "Si tienes que hacer la tarea, jugar y cenar, ¿qué es mejor hacer primero?", "opciones": ["Jugar sin parar", "La tarea, luego jugar y después cenar", "No cenar y jugar", "Empezar la tarea y no terminarla"], "respuesta_correcta": "La tarea, luego jugar y después cenar", "retroalimentacion": "Organizar tu tiempo cumpliendo primero tus responsabilidades es un buen hábito."},
    {"modulo_eduhome": "Taller de Funciones Ejecutivas", "eje": "Planificación", "oa": "OA 1", "dificultad": "Fácil", "pregunta": "Si tienes un examen mañana, ¿qué debes hacer hoy?", "opciones": ["Ver tele todo el día", "Estudiar un rato y repasar", "Ir a dormir muy tarde", "Llorar"], "respuesta_correcta": "Estudiar un rato y repasar", "retroalimentacion": "Planificar tu tiempo de estudio te ayuda a estar preparado."},
    {"modulo_eduhome": "Taller de Funciones Ejecutivas", "eje": "Memoria de Trabajo", "oa": "OA 3", "dificultad": "Difícil", "pregunta": "Si te dicen: 'Trae tu cuaderno, tu lápiz y tu goma', ¿cuántas cosas debes recordar?", "opciones": ["1", "2", "3", "4"], "respuesta_correcta": "3", "retroalimentacion": "Debes recordar 3 objetos: cuaderno, lápiz y goma."},
    {"modulo_eduhome": "Taller de Funciones Ejecutivas", "eje": "Flexibilidad", "oa": "OA 4", "dificultad": "Media", "pregunta": "Si vas a salir a jugar pelota, pero empieza a llover fuerte, ¿qué haces?", "opciones": ["Llorar porque se arruinó el día", "Salir igual y enfermarme", "Buscar un juego divertido para hacer dentro de casa", "Enojarme con el cielo"], "respuesta_correcta": "Buscar un juego divertido para hacer dentro de casa", "retroalimentacion": "Ser flexible significa adaptarse a los cambios cuando los planes fallan."},
    {"modulo_eduhome": "Taller de Funciones Ejecutivas", "eje": "Control Inhibitorio", "oa": "OA 5", "dificultad": "Media", "pregunta": "Si estás en clases y tienes muchas ganas de contar un chiste, debes...", "opciones": ["Gritarlo de inmediato", "Esperar al recreo o pedir la palabra en el momento adecuado", "Interrumpir a la profesora", "Hacer ruidos raros"], "respuesta_correcta": "Esperar al recreo o pedir la palabra en el momento adecuado", "retroalimentacion": "Controlar nuestros impulsos ayuda a mantener el respeto en clases."},

    # --- Taller de Movimiento y Coordinación (min 5) ---
    {"modulo_eduhome": "Taller de Movimiento y Coordinación", "eje": "Motricidad", "oa": "OA 3", "dificultad": "Fácil", "pregunta": "¿Qué haces cuando saltas la cuerda?", "opciones": ["Duermes", "Mueves los pies y las manos coordinadamente", "Te quedas quieto", "Cantas bajito"], "respuesta_correcta": "Mueves los pies y las manos coordinadamente", "retroalimentacion": "Saltar requiere mover las manos y saltar al mismo tiempo."},
    {"modulo_eduhome": "Taller de Movimiento y Coordinación", "eje": "Equilibrio", "oa": "OA 2", "dificultad": "Fácil", "pregunta": "¿Qué animal se caracteriza por pararse en una sola pata, mostrando buen equilibrio?", "opciones": ["El elefante", "El flamenco", "El gusano", "El león"], "respuesta_correcta": "El flamenco", "retroalimentacion": "El flamenco puede mantener su equilibrio en una sola pierna mucho tiempo."},
    {"modulo_eduhome": "Taller de Movimiento y Coordinación", "eje": "Motricidad fina", "oa": "OA 4", "dificultad": "Media", "pregunta": "¿Cuál de estas actividades usa 'motricidad fina'?", "opciones": ["Correr rápido", "Saltar muy alto", "Enhebrar una aguja o escribir", "Patear un balón"], "respuesta_correcta": "Enhebrar una aguja o escribir", "retroalimentacion": "La motricidad fina usa los músculos pequeños de las manos con precisión."},
    {"modulo_eduhome": "Taller de Movimiento y Coordinación", "eje": "Motricidad gruesa", "oa": "OA 5", "dificultad": "Fácil", "pregunta": "¿Qué deporte requiere correr y patear un balón?", "opciones": ["Ajedrez", "Fútbol", "Natación", "Ciclismo"], "respuesta_correcta": "Fútbol", "retroalimentacion": "El fútbol es un deporte de mucho movimiento de piernas."},
    {"modulo_eduhome": "Taller de Movimiento y Coordinación", "eje": "Salud", "oa": "OA 1", "dificultad": "Media", "pregunta": "¿Por qué es importante hacer deporte y moverse?", "opciones": ["Para estar aburrido", "Para enfermarse", "Para mantener los músculos y el corazón sanos", "Para ver más televisión"], "respuesta_correcta": "Para mantener los músculos y el corazón sanos", "retroalimentacion": "El ejercicio fortalece todo nuestro cuerpo."}
]

def main():
    preguntas_finales = []
    contador_id = 1

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
