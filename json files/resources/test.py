import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

print(f"Python Version: {sys.version}")
print(f"Matplotlib Version: {matplotlib.__version__}")

# Generate simple plot
fig, ax = plt.subplots()
ax.plot([1, 2, 3], [4, 5, 6])
ax.set_title("Test Plot")

# Force save directly
plt.savefig("test_output.png")
print("Saved 'test_output.png' successfully.")