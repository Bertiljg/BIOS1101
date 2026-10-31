import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
data = pd.read_csv("ant_species_elevation.csv")
høyde_over_havet = list(data["Elevation"])
maurarter = list(data["Number of ant species"])
a2, b2, c2 = np.polyfit(høyde_over_havet, maurarter, 2)
høyde_fit = np.linspace(1000,2200,100)
maur_fit2 = a2 * høyde_fit**2 + b2 * høyde_fit + c2
plt.plot(høyde_over_havet, maurarter, "o")
plt.plot(høyde_fit, maur_fit2, "-", label = "Kvadratisk regresjonsmodell")
plt.title("Antallet maurarter ved ulike høydemeter i Spring Mountains")
plt.xlabel("Meter over havet (m)")
plt.ylabel("Antallet maurarter")
plt.legend()
plt.show()
