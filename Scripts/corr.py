import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

base_path = "E:\\ARCHIVE\\BAP\\__Project\\csvexport\\"


df = pd.read_csv(base_path + "sobol-weekly-4-25-bc-s.csv", encoding='latin-1')
#temp = df['temp_average']
#glazing = df['glazing_ratio']

#C = np.corrcoef(glazing,temp)

df = df.iloc[:]
df.round(decimals=1)

correlation_mat = df.corr()

p = sns.heatmap(correlation_mat, annot = True, vmin=-1, vmax=1)
p.axes.set_title("Building Characteristics - Winter",fontsize=20)
plt.subplots_adjust(bottom = 0.214)
plt.show()