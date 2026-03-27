# Ayudantia Python para minería:
# Javier Ortega A.
# Python aplicado a la mineria, 2026 - 1

# LISTAS
# EJERCICIO 1: CONTROL DE TURNO
# Una lista registra las toneladas extraídas por cada camión durante un turno 
# de 12 horas, se debe: Agregar nuevos datos, corregir datos erroneos
# e identificar el viaje con mayor tonelaje.

#Creación de la lista
toneladas_viaje = [240.5, 238.0, 242.3, 180.0, 245.1]

print(f"Viajes registrados: {toneladas_viaje}")
print(f"Viaje con mayor tonelaje: {max(toneladas_viaje)} ton")
print(f"Número de viajes: {len(toneladas_viaje)}")

#Agregar nuevos viajes
toneladas_viaje.append(239.8)
toneladas_viaje.append(241.2)
print(f"Después de 2 viajes más: {toneladas_viaje}")

# Corrección de error: El cuarto viaje (índice 3) estaba mal pesado
# Los índices empiezan en 0, entonces el cuarto elemento es índice 3
toneladas_viaje[3] = 240.1  # Corrección del peso
print(f"Corregido a: {toneladas_viaje[3]} ton")

# Cálculo de producción total
tonelaje_total = sum(toneladas_viaje)
print(f"Producción total del turno: {tonelaje_total} toneladas")

# Promedio por viaje
promedio = tonelaje_total / len(toneladas_viaje)
print(f"Promedio por viaje: {promedio} ton")

# DICCIONARIOS
# EJERCICIO 1: FICHA TÉCNICA DE EQUIPO
# Diccionario para una pala con datos clave, se debe: Actualizar datos y 
# verificar el contenido de un dato particular

# Creación del diccionario
pala_5230 = {
    'modelo': 'Komatsu PC5500-6',
    'capacidad_balde': 29.0,  # metros cúbicos
    'horometro': 45231.5,  # horas
    'estado': 'Operativo',
    'operador': 'Juan Pérez',
    'ultimo_mantenimiento': '2024-03-15',
    'proximo_mantenimiento': 45500.0  # horómetro objetivo
}

print(f"Equipo: {pala_5230['modelo']}")   
print(f"Operador actual: {pala_5230['operador']}")

# Actualizar horómetro después del turno
horas_trabajadas = 12.5
pala_5230['horometro'] += horas_trabajadas
print(f"Horómetro actualizado: {pala_5230['horometro']} horas")

# Cambiar de operador
pala_5230['operador'] = 'Carlos Rodríguez'
print(f"Nuevo operador: {pala_5230['operador']}")

# Verificar disponibilidad para mantenimiento
horas_faltantes = pala_5230['proximo_mantenimiento'] - pala_5230['horometro']

if pala_5230['estado'] == 'Operativo' and horas_faltantes > 0:
    print(f"Estado: Disponible para operación")
    print(f"Horas hasta mantenimiento: {horas_faltantes}")
else:
    print("Equipo requiere mantenimiento inmediato")

# Agregar nueva clave
pala_5230['consumo_diesel_promedio'] = 850.5  # litros/hora
print(f"Consumo registrado: {pala_5230['consumo_diesel_promedio']} L/h")

# Eliminar clave obsoleta 
if 'fallas_reportadas' in pala_5230:
    del pala_5230['fallas_reportadas']
    print("Registro de fallas anteriores eliminado")

# Mostrar todas las características
print("Resumen")
for clave, valor in pala_5230.items():
    print(f"{clave}: {valor}")

#TUPLAS
#EJERCICIO 1: BARRENOS
#Una vez medidas, no deben cambiar.

barreno_1_diseño = (10542.50, 8234.75, 1250.00)  # Coordenadas de diseño
barreno_1_real = (10542.48, 8234.80, 1249.95)    # Mediciones reales

# Cálculo de desviación en 3D
# Desviación = raíz((x2-x1)² + (y2-y1)² + (z2-z1)²)

dx = barreno_1_real[0] - barreno_1_diseño[0]
dy = barreno_1_real[1] - barreno_1_diseño[1]
dz = barreno_1_real[2] - barreno_1_diseño[2]

desviacion = (dx**2 + dy**2 + dz**2)**0.5
print(f"Desviación del barreno 1: {desviacion:} metros")

# Verificar si está dentro de tolerancia (ej. 0.30m)
if desviacion <= 0.30:
    print("Dentro de tolerancia")
else:
    print("Barreno fuera de tolerancia")

barreno_1_real[0] = 10542.55  # Intentar modificar X

# Desempaquetado de la tupla
x_dis, y_dis, z_dis = barreno_1_diseño
print(f"Coordenada Norte (Y): {y_dis}")

# Tupla de tuplas
patron_banco = (
    (10542.50, 8234.75, 1250.00),  # Barreno 1
    (10544.50, 8234.75, 1250.00),  # Barreno 2  
    (10546.50, 8234.75, 1250.00),  # Barreno 3
)

print(f"Patrón completo: {len(patron_banco)} barrenos definidos")

# CONDICIONAL IF
# EJERCICIO 1: CLASIFICACIÓN DE MINERAL (SIMPLIFICADO)

# Datos de entrada del camión
ley_au = 1.8  # g/ton
ley_ag = 8.5  # g/ton
tonelaje = 240.5  # Toneladas métricas

# Leyes de corte definidas por plani
ley_corte_alta = 1.5      # Va directo a procesamiento
ley_corte_baja = 0.8      # Va a stockpile de baja ley

# Decisión de clasificación
if ley_au >= ley_corte_alta:
    destino = "Chancador (Procesamiento directo)"
    color = "Verde"
    prioridad = "Alta"
    
elif ley_au >= ley_corte_baja:
    destino = "Stockpile (Espera de blending)"
    color = "Amarillo"
    prioridad = "Media"
    
else:
    destino = "Botadero"
    color = "Rojo"
    prioridad = "Baja"

print(f"Destino: {destino}")
print(f"Código de prioridad: {color}")

# Cálculo económico simple
if ley_au >= ley_corte_baja:
    precio_au = 130000  # USD/kg 
    contenido_au = tonelaje * (ley_au / 1000)  # kg de oro
    valor_aprox = contenido_au * (precio_au * 0.85)  # 85% recuperación
    
    print(f"Contenido metal: {contenido_au} kg Au")
    print(f"Valor estimado: ${valor_aprox} USD")
else:
    # Calcular costo de transporte a botadero
    distancia_botadero = 3.5  # km
    costo_transporte = tonelaje * 0.15 * distancia_botadero  # $0.15/ton/km
    print(f"Costo de envío a botadero: ${costo_transporte} USD")

# CICLO FOR 
# EJERCICIO 1: REPORTE DE SONDAJES

# Datos de sondeos
sondajes = ['DDH-24-15', 'DDH-24-16', 'DDH-24-17', 'DDH-24-18', 'DDH-24-19']
profundidades = [125.5, 98.0, 150.2, 87.5, 110.0]  # metros
ley_promedio = [2.3, 1.8, 3.1, 0.9, 2.0]  # g/ton Au

# Usando range para iterar
for i in range(len(sondajes)):
    id_sondaje = sondajes[i]
    prof = profundidades[i]
    ley = ley_promedio[i]
    
    # Determinar estado basado en la ley
    if ley >= 2.0:
        estado = "Mineral alto"
    elif ley >= 1.0:
        estado = "Mineral bajo"
    else:
        estado = "Esteril"
    
    print(f"{id_sondaje:<10} {prof:<10} {ley:<10} {estado:<10}")

# Calcular profundidad total perforada
total_metros = 0
for prof in profundidades:
    total_metros += prof

print(f"Metraje total: {total_metros} m")

# CICLO FOR 
# EJERCICIO 1: DESCARGA DE TOLVA

# Control de nivel de tolva de alimentación al molino
nivel_tolva = 85.0  # Porcentaje de llenadO
nivel_critico_bajo = 20.0
nivel_critico_alto = 95.0
consumo_por_ciclo = 5.0  # % que baja por ciclo de alimentación al molino

print(f"Nivel inicial: {nivel_tolva}%")
print("Iniciando alimentacion")

ciclos = 0

# Mientras haya suficiente mineral (nivel > critico)
while nivel_tolva > nivel_critico_bajo:
    # Simular consumo del molino
    nivel_tolva -= consumo_por_ciclo
    ciclos += 1
    
    # Mostrar estado cada 5 ciclos
    if ciclos % 5 == 0:
        print(f"Ciclo {ciclos}: Nivel {nivel_tolva}%")
    
    # Alerta si baja mucho
    if nivel_tolva <= 30.0 and nivel_tolva > nivel_critico_bajo:
        print(f"Alerta: Nivel bajando a {nivel_tolva}%")
    
    # Detencion de seguridad si baja demasiado
    if nivel_tolva < 0:
        print(f"Tolva vacía - Detener el proceso")
        break  # Rompe el ciclo inmediatamente

print(f"Parada automática alcanzada")
print(f"Ciclos completados: {ciclos}")
print(f"Nivel final: {nivel_tolva}%")
print("Requerir carga desde stockpile")

# FUNCIONES
# EJERCICIO 1: REGISTRO OPERACIONAL

def registrar_descarga(camion_id, toneladas, ley_au, destino="Pendiente"):
    """
    Procedimiento que valida y registra la descarga de un camión.
    No retorna valores, solo imprime y valida (efecto lateral).
    """
    # Validaciones de entrada (guard clauses)
    if toneladas <= 0:
        print(f"Error {camion_id}: Tonelaje debe ser positivo")
        return  # Sale si hay error
    
    if ley_au < 0:
        print(f"Error {camion_id}: Ley no puede ser negativa")
        return
    
    # Lógica
    if ley_au >= 1.5:
        destino_final = "Chancador"
    elif ley_au >= 0.8:
        destino_final = "Stockpile"
    else:
        destino_final = "Botadero"
    
    # Simulando guardar en base de datos
    print(f"Camión: {camion_id}")
    print(f"Peso: {toneladas} TM")
    print(f"Ley: {ley_au} g/TM")
    print(f"Destino asignado: {destino_final}")
    print(f"Estado: {destino}")

# Llamadas a la función
registrar_descarga("CAT-773", 245.5, 1.8)
registrar_descarga("CAT-797", -10.0, 0.5)  # Error 
registrar_descarga("KOM-785", 290.0, 0.6, "EN RUTA")  # Con parámetro opcional



# EJERCICIO 2: FUNCION DE CALCULO GEOMECANICO    

def calcular_volumen(largo, ancho, alto, factor_esponjamiento = 1.35):
    """
    Calcula volumen real de material movido considerando esponjamiento post voladura
    Retorna el volumen esponjado
    """
    volumen_in_situ = largo * ancho * alto
    volumen_esponjado = volumen_in_situ * factor_esponjamiento
    
    return volumen_esponjado  # Retorna valor

def calcular_tonelaje(volumen_m3, densidad_aparente=2.65):
    """
    Convierte volumen a tonelaje usando densidad.
    """
    return volumen_m3 * densidad_aparente

vol = calcular_volumen(15, 10, 12, 1.40)  # Banco con esponjamiento 1.40
ton = calcular_tonelaje(vol, 2.70)  # Densidad del mineral

print(f"Volumen esponjado: {vol:} m3")
print(f"Tonelaje calculado: {ton:} ton")

# Uso en lista de bancos
bancos = [(15, 10, 12), (20, 15, 8), (12, 12, 10)]
total_tonelaje = 0

for largo, ancho, alto in bancos:
    vol = calcular_volumen(largo, ancho, alto)
    ton = calcular_tonelaje(vol)
    total_tonelaje += ton
    print(f"Banco: {ton:} ton")

print(f"Producción total: {total_tonelaje} ton")
