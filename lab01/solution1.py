numbers = []
with open("numbers.txt", "r") as fh:
    for line in fh:
        numbers.append(float(line.strip()))
numbers.sort()
for el in numbers:
    print(el)
