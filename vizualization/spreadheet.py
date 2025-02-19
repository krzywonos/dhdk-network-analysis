import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

file_path = 'data/eigenvector_centrality_by_decade.xlsx'
df = pd.read_excel(file_path, index_col=0)

df.index = df.index.map(str)

plt.figure(figsize=(12, 8))
sns.heatmap(df, annot=True, cmap='viridis', fmt=".2f")
plt.title('Eigenvector centrality by genre and decade')
plt.xlabel('Decade')
plt.ylabel('Genres')
plt.show()




