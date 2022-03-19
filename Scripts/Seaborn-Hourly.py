from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np
from math import nan
import pandas as pd

base_path = "E:\\ARCHIVE\\BAP\\__Project\\csvexport\\"


df = pd.read_csv(base_path + "sobol-hourly-3-10-uc-w-ST.csv", encoding='latin-1')
df = df.iloc[: , 1:]
# Seaborn setting
sns.set(style='whitegrid', rc={"grid.linewidth": 0.1})
sns.set_context("paper", font_scale=0.9)

# (3.1, 3) Two column paper. Each column is about 3.15 inch wide.
#plt.figure(figsize=(10, 6))
#plt.xlim(0, 1)

plt.xlim(0, 23)
color = sns.color_palette("Set2", 6)

p = sns.lineplot(data=df)

#labels
p.axes.set_title("Urban Characteristics - Winter",fontsize=20)
p.set_xlabel("Hour",fontsize=15)
p.set_ylabel("Sensitivy Index",fontsize=15)
p.tick_params(labelsize=10)

plt.xticks(rotation=90)
plt.tight_layout()

p.yaxis.grid(True, clip_on=False)
p.set(xticks=range(0,24))

leg = p.legend()
leg_lines = leg.get_lines()
for leg_line in leg_lines:   
    leg_line.set_linestyle("solid")
    
for line in p.lines:
    line.set_linestyle("solid")
    
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., fontsize=15)
plt.subplots_adjust(right = 0.76)

#sns.despine(left=True, bottom=True)
#plt.savefig('test.pdf', bbox_inches='tight')
plt.show()