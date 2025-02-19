import seaborn as sns
import matplotlib.pyplot as plt

# Convert K-Core data: 1 if genre is in the core, 0 otherwise
binary_k_core_df = k_core_df.notna().astype(int)

# Plot Heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(binary_k_core_df, cmap="Blues", linewidths=0.5, annot=False, cbar=True)

plt.title("K-Core Heatmap: Genre Persistence Over Time")
plt.xlabel("Decades")
plt.ylabel("Genres")

# Display the heatmap
plt.show()
