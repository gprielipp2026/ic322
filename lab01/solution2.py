words = {}
with open("words.txt", "r") as fh:
    # loop through lines in file
    for line in fh:
        strings = line.split()
        # count all words per line
        for string in strings:
            string = string.lower()
            if string in words:
                words[string] += 1
            else:
                words[string] = 1
# make it flat (key,pair)
words = [x for x in words.items()]
# sort based on pair
words.sort(reverse=True, key=lambda x: x[1])
for word, count in words[:5]:
    print(word + ": " + str(count))
