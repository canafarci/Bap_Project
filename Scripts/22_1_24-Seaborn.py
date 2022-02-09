from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np
from math import nan
#with open("E:\\ARCHIVE\\BAP\\__Project\\txtexport\\sobol-urban_characteristics-1-22-uc-w.txt", "r") as reader:
#    print(reader.read())


labels = ['Building Height', 'Facade to Site Ratio', 'Building Density', 'Urban Road Volumetric Heat Capacity' , 'Urban Road Albedo', 'Sensible Anthropogenic Heat', 'Urban Road Thermal Conductivity']
#labels = ['Glazing Ratio', 'Wall U Value', 'Window U Value', 'Window SHGC', 'Infiltration Rate', 'Chiller COP', 'Thermostat Setpoint', 'Equipment Load Density', 'Lighting Load Density', 'Occupancy Density', 'Wall Albedo', 'Roof Albedo', 'Wall Emissivity', 'Roof Emissivity', 'Floor Height', 'Roof U Value']

data = [0.41726086, 0.18416398, 0.19171091, 0.06012077, 0.0012793 , 0.01578675, 0.11277098] # uc - w
error = [0.0550726 , 0.03587426, 0.03626551, 0.02209828, 0.00540154, 0.01069515, 0.0306871] # uc - w

#data = [3.08160748e-02, 6.98083948e-01, 1.32950957e-01, 1.10003300e-01, 3.53455062e-05, 1.26608873e-03, 3.07087684e-02] # uc - s
#error = [3.55911560e-03, 5.75373144e-02, 1.45860282e-02, 1.20715678e-02, 5.34995014e-06, 1.54892380e-04, 3.26567353e-03] # uc - s

#data = [0.01949286, 0.31098804, 0.01388581, 0.0013662 , 0.60384982, 0. , 0.02599129, 0.00261288, 0.00141963, 0.00070053, 0.00503169, 0.00380398, 0.01216295, 0.00599063, 0.00172622, 0.09856535] #bc - w
#error = [0.00781664, 0.08907654, 0.0052514 , 0.00084872, 0.15909637, 0. ,0.00895345, 0.00111849, 0.00076964, 0.0004931,0.00215545, 0.00133796, 0.00500806, 0.00281415, 0.00069384, 0.03552967] #bc- w

#data = [0.19223831, 0.18851948, 0.02077619, 0.00527678, 0.11704721, 0.0333229 , 0.17577028, 0.03817053, 0.01952348, 0.00963179, 0.13283524, 0.0940089 , 0.32815016, 0.10713889, 0.03810706,0.0381675] #bc- s
#error = [0.02191285, 0.02633707, 0.00345278, 0.00105508, 0.02177904, 0.00584051, 0.01616256, 0.00506463, 0.00283845, 0.0016886, 0.01473716, 0.01473397, 0.03306484, 0.01691468, 0.00656851, 0.00661181] #bc - s

arr = [[        nan, -0.00229778,  0.00056051,  0.00072822,  0.00031161,  0.00039534,  0.00058252],
       [        nan,         nan,  0.00394857,  0.00349225,  0.00221846,        0.00196668,  0.00150342],
       [        nan,         nan,         nan,  0.00109213,  0.00113361,         0.00122868, -0.00031391],
       [        nan,         nan,         nan,         nan,  0.00208048,         0.00252799,  0.00204467],
       [        nan,         nan,         nan,         nan,         nan,        -0.00014774, -0.00012226],
       [        nan,         nan,         nan,         nan,         nan,               nan, -0.00044183],
       [        nan,         nan,         nan,         nan,         nan,               nan,         nan]] # uc - s
       
""" arr = [[        nan,  0.00652729,  0.01322417,  0.00935559,  0.00567269,         0.0046798 ,  0.01125659],
       [        nan,         nan, -0.00589793,  0.00267299,  0.00035865,        -0.00320027, -0.00520218],
       [        nan,         nan,         nan,  0.01195774,  0.00635007,         0.00298905,  0.00858686],
       [        nan,         nan,         nan,         nan,  0.00272759,         0.00233121,  0.00740088],
       [        nan,         nan,         nan,         nan,         nan,        -0.0005075 ,  0.00095807],
       [        nan,         nan,         nan,         nan,         nan,                nan,  0.0015394 ],
       [        nan,         nan,         nan,         nan,         nan,                nan,         nan]] """ # uc - w
       
       

# Seaborn setting                                                                                                                                              
sns.set(style='whitegrid', rc={"grid.linewidth": 0.1})
sns.set_context("paper", font_scale=0.9)                                                  
plt.figure(figsize=(10, 6)) #  (3.1, 3) Two column paper. Each column is about 3.15 inch wide.   
plt.xlim(0, 1)                                                                                                                                                                                                                              
color = sns.color_palette("Set2", 6)

p = sns.barplot(x=data, y=labels, palette=color,  linewidth = 0.7)

# to enhance visibility of error bars, 
# you can draw them twice with different widths and colors:
p.errorbar(y=labels, 
           x=data,
           xerr=error, 
           fmt='none',
           linewidth=3, c='w',
           capsize=0.2
           )

p.errorbar(y=labels, 
           x=data, 
           xerr=error, 
           fmt='none',
           c='r',capsize=0.2
           )

p.set(xlabel='Sensitivity Index', ylabel='Parameter')

plt.xticks(rotation=90)                                                               
plt.tight_layout() 

p.yaxis.grid(True, clip_on=False)    

sns.despine(left=True, bottom=True)                                                   
#plt.savefig('test.pdf', bbox_inches='tight')  
plt.show()

np.random.seed(0)
uniform_data = arr
ax = sns.heatmap(uniform_data)
ax.set_yticklabels(labels, rotation=0)
ax.set_xticklabels(labels)
ax.tick_params(labelsize=12)
plt.xticks(rotation=90)
plt.show()