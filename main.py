file = open("speeches/Nomination_Macron.txt", "r")
for line in file:
    print(line)
    line = line.replace("e", "")
    print(line)

print(len({"bonjour":2}))