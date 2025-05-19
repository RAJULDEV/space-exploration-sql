import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(r"C:\Users\swapn\Desktop\space-exploration-sql\results\results_query4.csv")
plt.bar(df["decade"], df["mission_count"])
plt.xlabel("Decade")
plt.ylabel("Number of Missions")
plt.title("Space Missions by Decade")
plt.savefig(r"C:\Users\swapn\Desktop\space-exploration-sql\results\missions_by_decade.png")
plt.show()