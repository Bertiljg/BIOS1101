import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("ant_species_elevation.csv")

høyde_over_havet = list(data["Elevation"])
maurarter = list(data["Number of ant species"])

plt.plot(høyde_over_havet, maurarter, "o")
plt.title("Antallet maurarter ved ulike høydemeter i Spring Mountains")
plt.xlabel("Meter over havet (m)")
plt.ylabel("Antallet maurarter")
plt.show()
