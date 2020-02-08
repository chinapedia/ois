

with open("../data/test_truth.txt", "r") as ifile:
    categorySet = set()
    lines = ifile.readlines()
    dataSize = 0.0
    hitCount = 0.0
    for line in lines:
        dataSize += 1
        d = line.strip('\n').split("\t")
        print (d)
        if (d[0] == d[1]):
            hitCount += 1

print (hitCount / dataSize)