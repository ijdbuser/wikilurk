import json

open_file = open("wtf.txt", "r")

line = open_file.read()
print(line.find("['Exclamation mark -> Factorial ']"))

with open("output2.txt", "w") as output:
    kekw = "[" + line[27916869:].replace("'", '"')
    output.write(kekw)
    print(line[10450])

with open("output2.txt", "r") as file:
    kek = json.load(file)
