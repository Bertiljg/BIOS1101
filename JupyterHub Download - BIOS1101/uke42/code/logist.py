import matplotlib.pyplot as plt

xs = []
ns = range(____) # Her bruker vi range kommandoet!

xs.append(____)

r = ____
K = ____

n = 1
while ____:
    x_n = ____
    xs.append(x_n)
    n = n + 1

plt.plot(____, ____)
____ # her kan du legge til andre elementer til plottet
plt.axhline(K, ls = ":")
plt.show()
