from fitter import Fitter, get_common_distributions, get_distributions
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

dataset = pd.read_csv("E:\\ARCHIVE\\BAP\\__Project\\csvexport\\dists3.csv")

dataset = dataset.apply (pd.to_numeric, errors='coerce')

dataset = dataset.dropna()
dataset.to_numpy()

dataset= dataset[dataset["wall_u"] > 0]

dataset = pd.DataFrame(np.sort(dataset.values, axis=0), index=dataset.index, columns=dataset.columns)

dataset.loc[~(dataset==0).all(axis=1)]

#dataset = np.random.beta(20, 13.3, 100000)


sns.set_style('white')
sns.set_context("paper", font_scale = 2)
sns.displot(data=dataset, kind="hist", bins = 193, aspect = 1.5)
plt.show()

#dataset = dataset['window_u']
print(dataset)

f = Fitter(dataset, bins=193, distributions=['normal', 'lognorm', 'uniform'])
f.fit()
f.summary()
plt.show()

print(f.get_best(method = 'sumsquare_error'))