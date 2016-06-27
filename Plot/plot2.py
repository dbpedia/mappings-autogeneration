import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv("data2.csv")

grid_size = (1, 2)
plt.subplot2grid(grid_size, (0, 0), rowspan=1, colspan=1)
plt.plot(data["C"], data["precision"], marker="o")
plt.ylabel('Precision')
plt.xlabel('C')
plt.grid(True)

plt.subplot2grid(grid_size, (0, 1), rowspan=1, colspan=1)
plt.plot(data["C"], data["recall"], marker="o")
plt.ylabel('Recall')
plt.xlabel('C')
plt.grid(True)

plt.suptitle("Performance on bulgarian given 6 pivot languages with L = 0.5")
plt.show()
