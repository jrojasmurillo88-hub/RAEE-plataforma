import re

with open("output/pilascolombia_com_rendered.html", encoding="utf-8") as f:
    contenido = f.read()

idx = contenido.find('"ciu_munic"')
inicio = contenido.rfind("[", 0, idx)
print("Primeros 300 caracteres desde el inicio del array:")
print(contenido[inicio:inicio + 300])
print()
print("Conteo aprox. de registros (por campo 'nombre'):", contenido.count('"nombre":'))
print("Conteo aprox. de registros (por campo 'status_id'):", contenido.count('"status_id"'))
print("Conteo aprox. de registros (por campo 'ciu_munic'):", contenido.count('"ciu_munic"'))

# Intentar encontrar el cierre del array
fin = contenido.find("];", inicio)
if fin == -1:
    fin = contenido.find("]", inicio)
print()
print("Longitud del bloque (caracteres):", fin - inicio if fin != -1 else "no encontrado")
