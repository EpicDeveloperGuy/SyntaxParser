import sys
import math

G_A, X_A = {}, {}
G_B, X_B = {}, {}

def makeRules(G, X, file):
    with open(file, "r") as f:
        for line in f.readlines():
            Line = line[2:]
            Line = Line.split(" : ")
            k1 = Line[0].strip()
            k2 = Line[1].split(" ")[0].strip()
            k2 = (" ".join(Line[1].split(" ")[:-1])).strip()
            val = float(Line[1].strip().split(" ")[-1].strip())
            if line[0] == "G":
                if k1 == "<UNK-NT>":
                    k1 = "<unk>"
                d = k2.split()
                for n,i in enumerate(d):
                    if i  == "<UNK-T>":
                        d[n] = "<unk>"
                    if i[:8]  == "<UNK-NT>":
                        d[n] = "<unk>"+i[8:]
                k2 = (" ".join(d)).strip()
                G[(k1, k2)] = val
            else:
                if k2 == "<UNK-T>":
                    k2 = "<unk>"
                if k1[:8] == "<UNK-NT>":
                    k1 = "<unk>"+k1[8:]
                X[(k1, k2)] = val

makeRules(G_A, X_A, sys.argv[1])
makeRules(G_B, X_B, sys.argv[2])

print("--LEN--")
print(sys.argv[1], len(G_A), len(X_A))
print(sys.argv[2], len(G_B), len(X_B))
print("\n--G--")
(k1, k2) = (G_A, G_B) if len(G_A) > len(G_B) else (G_B, G_A)
for i in k1:
    if i not in k2 or k1[i] != k2[i]:
        print(i)
print("\n--X--")
(k1, k2) = (X_A, X_B) if len(X_A) > len(X_B) else (X_B, X_A)
for i in k1:
    if i not in k2 or k1[i] != k2[i]:
        print(i)