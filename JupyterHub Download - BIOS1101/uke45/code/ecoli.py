import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("ecoli_39_grader.csv")
t = list(data["t"])
E = list(data["E"])

plt.plot(t, E, "o-")
plt.xlabel("Tid, t (minuter)")
plt.ylabel("Populasjonsstørrelse, E")
plt.title("Bakteriell vekst")
plt.show()
