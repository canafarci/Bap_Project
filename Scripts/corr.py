import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

base_path = "E:\\ARCHIVE\\BAP\\__Project\\csvexport\\"


df = pd.read_csv(base_path + "sobol-building_characteristics-10-2-bc-w.csv", encoding='latin-1')
#temp = df['temp_average']
#glazing = df['glazing_ratio']

#C = np.corrcoef(glazing,temp)

df = df.iloc[:]


correlation_mat = df.corr()

sns.heatmap(correlation_mat, annot = True, vmin=-1, vmax=1)

plt.show()