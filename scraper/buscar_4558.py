import re

with open("output/pilascolombia_com_rendered.html", encoding="utf-8") as f:
    contenido = f.read()

for m in re.finditer(r"4558", contenido):
    i = m.start()
    print("---")
    print(contenido[max(0, i - 80):i + 80])
