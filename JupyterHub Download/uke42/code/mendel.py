import numpy as np

plante1_p = ["P", "p"]
plante2_p = ["P", "p"]
hvit = 0
N = 1000

n = 0
while n < N:
    allel_plante1 = np.random.choice(plante1_p)
    allel_plante2 = np.random.choice(plante2_p)
    genotype = allel_plante1 + allel_plante2
    if genotype == "pp":
        hvit = hvit + 1
    n = n + 1

print(f"Sannsynligheten for å få hvite blomster er: {hvit/N}")
