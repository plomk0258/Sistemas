import pandas as pd
import random

def generar_dataset_sentimientos():
    """
    Genera un dataset de 5000 comentarios en español para análisis de sentimientos
    con las columnas 'texto' y 'sentimiento' que requiere el código
    """
    
    # Comentarios positivos
    comentarios_positivos = [
        "Excelente producto, superó todas mis expectativas. Lo recomiendo totalmente.",
        "Increíble servicio al cliente, muy atentos y profesionales.",
        "La calidad es fantástica, definitivamente vale la pena el precio.",
        "Muy satisfecho con mi compra, funciona perfectamente.",
        "Producto de primera calidad, llegó rápido y bien empacado.",
        "Maravilloso, exactamente lo que necesitaba.",
        "Servicio impecable, personal muy amable y eficiente.",
        "Calidad excepcional, materiales resistentes y duraderos.",
        "Muy contento con el resultado, funciona mejor de lo esperado.",
        "Excelente relación calidad-precio, totalmente recomendado.",
        "Perfecto, cumple con todas las especificaciones.",
        "Fantástico diseño, muy elegante y funcional.",
        "Gran producto, fácil de usar y muy práctico.",
        "Buenísima calidad, se nota la diferencia con otros productos.",
        "Extraordinario, supera por mucho a la competencia.",
        "Muy buena inversión, estoy encantado con el producto.",
        "Excelente acabado, detalles muy cuidados.",
        "Funciona de maravilla, sin ningún problema.",
        "Producto premium, calidad superior en todos los aspectos.",
        "Muy recomendable, cumple y supera las expectativas.",
        "Brillante idea, soluciona perfectamente mi problema.",
        "Increíblemente útil, no puedo vivir sin él ahora.",
        "Calidad top, materiales de primera.",
        "Servicio cinco estrellas, personal súper capacitado.",
        "Producto innovador, tecnología de vanguardia.",
        "Muy satisfactorio, rendimiento excelente.",
        "Genial, fácil instalación y uso intuitivo.",
        "Extraordinaria durabilidad, construcción sólida.",
        "Perfecto para mis necesidades, justo lo que buscaba.",
        "Excepcional atención, resolvieron todas mis dudas.",
        "Muy buena experiencia de compra, proceso sencillo.",
        "Producto confiable, marca reconocida y prestigiosa.",
        "Excelente funcionalidad, muy versátil.",
        "Gran satisfacción, producto de alta gama.",
        "Muy eficiente, ahorra tiempo y esfuerzo.",
        "Calidad premium a precio justo.",
        "Fantástico rendimiento, supera las especificaciones.",
        "Muy práctico y útil para el día a día.",
        "Excelente diseño ergonómico, muy cómodo.",
        "Producto revolucionario, cambia completamente la experiencia.",
        "Muy buena atención postventa, siempre disponibles.",
        "Gran calidad de construcción, acabados perfectos.",
        "Funciona como un reloj, muy confiable.",
        "Excelente valor agregado, muchas funciones útiles.",
        "Muy contento, producto que realmente funciona.",
        "Servicio excepcional, entrega rápida y segura.",
        "Calidad insuperable, materiales de lujo.",
        "Muy recomendado, experiencia totalmente positiva.",
        "Producto estrella, el mejor de su categoría.",
        "Excelente inversión, se paga solo con el uso."
    ]
    
    # Comentarios negativos
    comentarios_negativos = [
        "Pésimo producto, se rompió a los pocos días de uso.",
        "Muy decepcionado, no funciona como se anuncia.",
        "Terrible calidad, materiales muy baratos y frágiles.",
        "Servicio al cliente horrible, nadie responde mis consultas.",
        "No lo recomiendo para nada, perdida total de dinero.",
        "Muy malo, no cumple con las especificaciones prometidas.",
        "Deficiente, se descompuso inmediatamente después de comprarlo.",
        "Pésima experiencia, producto defectuoso desde el inicio.",
        "Muy caro para la baja calidad que ofrece.",
        "Terrible, no funciona correctamente desde el primer día.",
        "Muy frustrante, constantemente presenta fallas.",
        "Malo, no vale la pena el precio que cobran.",
        "Decepcionante, esperaba mucho más por ese precio.",
        "Pésimo servicio, personal grosero y poco profesional.",
        "Muy deficiente, calidad inferior a productos similares.",
        "No sirve, es un desperdicio de dinero.",
        "Horrible experiencia, problemas desde el primer uso.",
        "Muy mala calidad, se ve y se siente barato.",
        "Terrible construcción, se rompe con facilidad.",
        "No funciona para nada, completamente inútil.",
        "Pésima atención, nunca resuelven los problemas.",
        "Muy malo, definitivamente no lo volvería a comprar.",
        "Decepcionante calidad, no dura nada.",
        "Horrible, peor producto que he comprado en años.",
        "Muy defectuoso, lleno de errores y fallas.",
        "Pésimo, no recomiendo a nadie que lo compre.",
        "Terrible inversión, se arrepentirán de comprarlo.",
        "Muy mala experiencia, servicio lento e ineficiente.",
        "No funciona bien, problemas constantes de funcionamiento.",
        "Pésima calidad-precio, hay mejores opciones en el mercado.",
        "Muy malo, diseño poco funcional y antiestético.",
        "Horrible durabilidad, se deteriora muy rápido.",
        "Terrible, no cumple con ninguna expectativa.",
        "Muy decepcionante, publicidad engañosa.",
        "Pésimo rendimiento, funciona muy lento.",
        "Malo, interfaz confusa y poco intuitiva.",
        "Muy deficiente, constantemente se congela o falla.",
        "Horrible experiencia de usuario, muy complicado de usar.",
        "Pésima construcción, materiales de mala calidad.",
        "Muy malo, no tiene las funciones que promete.",
        "Terrible soporte técnico, nunca están disponibles.",
        "Decepcionante, no resuelve el problema para el que se compró.",
        "Muy caro y malo, no vale ni la mitad del precio.",
        "Pésimo, mejor buscar alternativas en la competencia.",
        "Horrible, me arrepiento completamente de la compra.",
        "Muy defectuoso, llegó dañado y mal empacado.",
        "Pésima experiencia, proceso de compra muy tedioso.",
        "Malo, no es compatible con otros productos como dice.",
        "Terrible, falso producto, no es lo que se anuncia.",
        "Muy malo, obsoleto y con tecnología anticuada."
    ]
    
    # Comentarios neutrales
    comentarios_neutrales = [
        "El producto está bien, cumple su función básica.",
        "Es correcto, sin más. Funciona como se espera.",
        "Producto promedio, ni bueno ni malo.",
        "Está bien para el precio que tiene.",
        "Es aceptable, cumple con lo mínimo esperado.",
        "Normal, sin características destacables.",
        "Producto estándar, nada fuera de lo común.",
        "Está bien, funciona correctamente pero sin sorpresas.",
        "Es adecuado para uso básico.",
        "Cumple su propósito, sin más.",
        "Producto común, similar a otros del mercado.",
        "Es funcional, hace lo que debe hacer.",
        "Está bien, calidad promedio para el precio.",
        "Es acceptable, no hay mucho que destacar.",
        "Producto básico que cumple su función.",
        "Normal, sin grandes ventajas ni desventajas.",
        "Es correcto, funciona según las especificaciones.",
        "Está bien, producto estándar del mercado.",
        "Es adecuado, cumple con lo prometido.",
        "Producto regular, ni excelente ni malo.",
        "Funciona bien, diseño común y corriente.",
        "Es aceptable para el uso que le doy.",
        "Está bien, calidad estándar de la marca.",
        "Producto típico, nada especial pero funciona.",
        "Es correcto, cumple con las expectativas básicas.",
        "Normal, producto promedio de su categoría.",
        "Está bien, funcionalidad adecuada.",
        "Es aceptable, sin problemas pero tampoco destaca.",
        "Producto común, hace lo que debe.",
        "Está bien para uso ocasional.",
        "Es funcional, diseño simple y efectivo.",
        "Normal, calidad estándar del sector.",
        "Producto básico pero confiable.",
        "Está bien, sin características extraordinarias.",
        "Es correcto, funciona como cualquier otro similar.",
        "Adecuado para necesidades básicas.",
        "Está bien, producto estándar sin sorpresas.",
        "Es aceptable, cumple con lo esencial.",
        "Normal, funcionamiento correcto.",
        "Producto promedio, calidad estándar.",
        "Está bien, hace su trabajo sin problemas.",
        "Es funcional, diseño convencional.",
        "Correcto, sin grandes innovaciones.",
        "Está bien para el uso que se le da.",
        "Producto común, funcionamiento normal.",
        "Es aceptable, calidad media del mercado.",
        "Normal, cumple con los requisitos básicos.",
        "Está bien, producto típico de la marca.",
        "Es adecuado, funciona como se espera.",
        "Producto estándar, sin características especiales."
    ]
    
    # Generar dataset balanceado
    dataset = []
    
    # Calcular cuántos comentarios por categoría (aproximadamente 1667 cada una)
    comentarios_por_categoria = 1667
    resto = 5000 - (comentarios_por_categoria * 3)  # 5000 - 5001 = -1, ajustamos
    
    # Generar comentarios positivos
    for i in range(comentarios_por_categoria):
        base_comment = random.choice(comentarios_positivos)
        # Agregar variaciones para hacer únicos los comentarios
        variations = [
            f"{base_comment}",
            f"Realmente {base_comment.lower()}",
            f"Debo decir que {base_comment.lower()}",
            f"Sinceramente, {base_comment.lower()}",
            f"En mi experiencia, {base_comment.lower()}",
            f"La verdad es que {base_comment.lower()}",
            f"Personalmente creo que {base_comment.lower()}",
            f"Mi opinión: {base_comment.lower()}",
            f"Sin duda, {base_comment.lower()}",
            f"Definitivamente {base_comment.lower()}"
        ]
        
        comment = random.choice(variations)
        dataset.append({'texto': comment, 'sentimiento': 'positivo'})
    
    # Generar comentarios negativos
    for i in range(comentarios_por_categoria):
        base_comment = random.choice(comentarios_negativos)
        variations = [
            f"{base_comment}",
            f"Lamentablemente {base_comment.lower()}",
            f"Desafortunadamente {base_comment.lower()}",
            f"Por desgracia, {base_comment.lower()}",
            f"Tristemente {base_comment.lower()}",
            f"Es una pena que {base_comment.lower()}",
            f"Me molesta que {base_comment.lower()}",
            f"Es frustrante que {base_comment.lower()}",
            f"No puedo creer que {base_comment.lower()}",
            f"Es increíble que {base_comment.lower()}"
        ]
        
        comment = random.choice(variations)
        dataset.append({'texto': comment, 'sentimiento': 'negativo'})
    
    # Generar comentarios neutrales (incluyendo el resto)
    for i in range(comentarios_por_categoria + resto):
        base_comment = random.choice(comentarios_neutrales)
        variations = [
            f"{base_comment}",
            f"En general, {base_comment.lower()}",
            f"Según mi experiencia, {base_comment.lower()}",
            f"Considero que {base_comment.lower()}",
            f"Pienso que {base_comment.lower()}",
            f"Me parece que {base_comment.lower()}",
            f"Diría que {base_comment.lower()}",
            f"En mi opinión, {base_comment.lower()}",
            f"Creo que {base_comment.lower()}",
            f"Es mi impresión que {base_comment.lower()}"
        ]
        
        comment = random.choice(variations)
        dataset.append({'texto': comment, 'sentimiento': 'neutral'})
    
    # Mezclar el dataset
    random.shuffle(dataset)
    
    # Crear DataFrame
    df = pd.DataFrame(dataset)
    
    return df

# Generar el dataset
print("Generando dataset de 5000 comentarios...")
dataset = generar_dataset_sentimientos()

# Guardar como CSV
dataset.to_csv('dataset_sentimientos_5000.csv', index=False, encoding='utf-8')

print(f"Dataset generado exitosamente!")
print(f"Total de comentarios: {len(dataset)}")
print(f"Distribución:")
print(dataset['sentimiento'].value_counts())
print(f"\nPrimeras 5 filas:")
print(dataset.head())
print(f"\nArchivo guardado como: dataset_sentimientos_5000.csv")

# Mostrar estadísticas del dataset
print(f"\n--- ESTADÍSTICAS DEL DATASET ---")
print(f"Columnas: {list(dataset.columns)}")
print(f"Tipos de datos:")
print(dataset.dtypes)
print(f"\nEjemplos por categoría:")
print(f"\nPOSITIVOS:")
positivos = dataset[dataset['sentimiento'] == 'positivo']['texto'].head(3)
for i, texto in enumerate(positivos, 1):
    print(f"{i}. {texto}")

print(f"\nNEGATIVOS:")
negativos = dataset[dataset['sentimiento'] == 'negativo']['texto'].head(3)
for i, texto in enumerate(negativos, 1):
    print(f"{i}. {texto}")

print(f"\nNEUTRALES:")
neutrales = dataset[dataset['sentimiento'] == 'neutral']['texto'].head(3)
for i, texto in enumerate(neutrales, 1):
    print(f"{i}. {texto}")