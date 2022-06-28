from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np
from math import nan
import textwrap

# region  #* urban characteristics
title = "Building Characteristics - Summer - Second Order"
data =[1.19135289e-01, 1.91568729e-01, 9.82857705e-02, 1.85588887e-03,
       4.62618080e-01, 0.00000000e+00, 1.45303429e-01, 2.73464966e-04,
       1.17464412e-04, 1.11749927e-04, 2.87336024e-04, 5.55428397e-04,
       4.30588881e-04, 3.59963708e-05, 8.40273492e-04, 2.32677220e-03]
error = [1.15169117e-02, 1.45838038e-02, 7.34975397e-03, 1.44192407e-04,
       2.88344405e-02, 0.00000000e+00, 9.20142865e-03, 2.87910063e-05,
       1.51848077e-05, 1.23400240e-05, 2.50878853e-05, 6.24916441e-05,
       1.05148098e-04, 1.59318099e-05, 8.41705373e-05, 2.11246662e-04]
# uc - s - 2nd
arr = [[            nan,  1.44969852e-03,  7.52120161e-05,
         6.59807473e-03,  6.95652662e-04,  3.88387568e-03,
        -2.92659871e-04,  2.29159438e-03,  1.28314956e-03,
         2.54965377e-03,  5.64453616e-03,  1.04339226e-03,
        -3.34754664e-04,  3.40592233e-04,  2.47644543e-03,
         7.92653707e-04],
       [            nan,             nan,  1.00549159e-02,
         1.22310336e-02,  1.11438898e-02,  7.61524806e-03,
         1.74269953e-02,  8.93848873e-03,  9.93229189e-03,
         9.88287626e-03,  9.44545646e-03,  9.61017521e-03,
         7.17599805e-03,  8.94946998e-03,  7.65551265e-03,
         9.31368145e-03],
       [            nan,             nan,             nan,
         3.09836897e-03,  2.15032102e-03,  1.63420225e-03,
         6.97658055e-03,  2.62983562e-03,  3.49735440e-03,
         2.90985750e-03,  3.40401377e-03,  3.29786168e-03,
         2.68474187e-03,  2.97025438e-03,  1.45484183e-03,
         3.25027626e-03],
       [            nan,             nan,             nan,
                    nan, -8.73553973e-04, -1.98632068e-03,
         3.28650971e-03, -1.97716963e-03, -1.21397273e-03,
        -1.91311234e-03, -2.98012383e-03, -1.69714775e-03,
        -1.33110607e-03, -2.03756651e-03, -2.52440194e-03,
        -1.69714775e-03],
       [            nan,             nan,             nan,
                    nan,             nan, -4.75766145e-03,
         5.17487950e-03, -4.16101352e-03, -3.74555621e-03,
        -4.43371457e-03, -4.28180727e-03, -4.39894061e-03,
        -4.95166354e-03, -4.74484999e-03, -3.74921663e-03,
        -4.58745207e-03],
       [            nan,             nan,             nan,
                    nan,             nan,             nan,
         2.27846439e-03,  5.34772387e-03,  4.24593842e-03,
         3.50836443e-03,  6.15118535e-03,  5.25621345e-03,
         4.99998427e-03,  4.41065717e-03,  2.90988629e-03,
         5.25438324e-03],
       [            nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,  1.94970462e-03,  5.60463078e-03,
         2.65433485e-03,  1.81243899e-03,  8.77202500e-04,
        -8.30381931e-04,  8.00333748e-04,  1.74655149e-03,
         1.30181085e-03],
       [            nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,  5.53040315e-03,
         4.47986353e-03,  3.41834266e-03,  5.34921252e-03,
         3.73496871e-03,  4.93375521e-03,  4.63177083e-03,
         4.45241040e-03],
       [            nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,             nan,
         3.28247894e-03,  2.95121122e-03,  2.96219247e-03,
         2.51745183e-03,  2.64739663e-03,  4.27811231e-03,
         3.29162998e-03],
       [            nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,  1.43604737e-03,  9.62023391e-04,
         1.32623486e-03,  8.37569221e-04, -1.19629770e-04,
         4.33093165e-04],
       [            nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan, -5.53753750e-04,
        -6.87358962e-04, -6.63566253e-04, -7.91680841e-04,
        -1.91372488e-04],
       [            nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,             nan,
         2.34191954e-03,  1.38838097e-03,  1.12849138e-03,
         2.08752058e-03],
       [            nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan, -8.54226832e-04, -1.93038937e-03,
        -3.21636189e-04],
       [            nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan, -4.98436473e-04,
        -6.11909394e-04],
       [            nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,             nan,
         3.49203186e-03],
       [            nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan]]
#endregion


#region  #* building characteristics 
       # bc - w - to
# title = "Building Characteristics - Summer - Second Order"
# data =[1.18637989e-01, 1.93739897e-01, 9.92413493e-02, 1.89442882e-03,
#        4.64096982e-01, 0.00000000e+00, 1.42638465e-01, 2.68631823e-04,
#        1.24303768e-04, 3.46868790e-05, 2.85373440e-04, 4.94588937e-04,
#        4.63841262e-04, 2.84498061e-05, 8.66296596e-04, 2.26405746e-03]

# error = [1.71317828e-02, 2.36559059e-02, 1.03935899e-02, 2.64822827e-04,
#        4.53474197e-02, 0.00000000e+00, 1.29864253e-02, 3.25205913e-05,
#        2.11344819e-05, 1.21511366e-05, 4.23254852e-05, 7.55458998e-05,
#        1.66170155e-04, 1.14925103e-05, 1.15898885e-04, 3.26065310e-04]
# # bc - w - 2nd"""
# arr = [[            nan,  9.22637434e-03, -9.36371143e-05,
#         -1.64697236e-03, -1.06447164e-03, -1.45280545e-03,
#          4.17803480e-03,  3.78970099e-03,  1.45969813e-03,
#         -4.81970925e-04,  3.20720028e-03, -1.45280545e-03,
#         -3.39447451e-03, -1.25863855e-03, -6.30697809e-03,
#          4.88863602e-04],
#        [            nan,             nan,  2.70893721e-02,
#          1.42743563e-02,  3.13610440e-02,  1.71868599e-02,
#          3.62152166e-02,  1.87401952e-02,  2.00993635e-02,
#          1.48568571e-02,  2.02935304e-02,  1.40801894e-02,
#          1.91285290e-02,  1.83518614e-02,  2.10701980e-02,
#          2.59243707e-02],
#        [            nan,             nan,             nan,
#          1.36385019e-02,  4.35152368e-04,  1.57743379e-02,
#          1.96576760e-02,  1.71335062e-02,  1.59685048e-02,
#          1.32501681e-02,  1.57743379e-02,  1.22793336e-02,
#          1.53860041e-02,  1.22793336e-02,  1.16968329e-02,
#          1.26676674e-02],
#        [            nan,             nan,             nan,
#                     nan,  4.01761619e-04,  2.07594714e-04,
#          1.34278085e-05,  2.07594714e-04,  2.07594714e-04,
#          2.07594714e-04,  1.34278085e-05,  2.07594714e-04,
#          2.07594714e-04,  1.34278085e-05,  2.07594714e-04,
#          2.07594714e-04],
#        [            nan,             nan,             nan,
#                     nan,             nan,  1.02567401e-02,
#          2.57900926e-02,  8.31507109e-03,  9.67423943e-03,
#          1.27809099e-02,  1.37517444e-02,  5.40256751e-03,
#          1.25867430e-02,  3.84923227e-03,  8.50923800e-03,
#          1.20042423e-02],
#        [            nan,             nan,             nan,
#                     nan,             nan,             nan,
#          3.60896190e-03,  6.96458316e-04,  5.02291410e-04,
#          1.13957600e-04, -8.02093058e-05, -8.02093058e-05,
#         -8.02093058e-05,  5.02291410e-04,  8.90625221e-04,
#          1.13957600e-04],
#        [            nan,             nan,             nan,
#                     nan,             nan,             nan,
#                     nan, -1.39263060e-02, -1.35379721e-02,
#         -1.41204729e-02, -1.78096441e-02, -1.80038110e-02,
#         -1.29554714e-02, -1.39263060e-02, -6.74213045e-03,
#         -1.37321390e-02],
#        [            nan,             nan,             nan,
#                     nan,             nan,             nan,
#                     nan,             nan,  1.23867561e-03,
#          2.67841079e-04, -3.14659637e-04,  6.56174890e-04,
#          2.01534323e-03,  1.62700942e-03,  7.36741741e-05,
#          2.40367704e-03],
#        [            nan,             nan,             nan,
#                     nan,             nan,             nan,
#                     nan,             nan,             nan,
#          1.40598689e-03,  2.57098833e-03,  1.21181999e-03,
#          1.79432071e-03,  2.37682142e-03,  2.37682142e-03,
#          2.37682142e-03],
#        [            nan,             nan,             nan,
#                     nan,             nan,             nan,
#                     nan,             nan,             nan,
#                     nan,  2.56445320e-03,  8.16951047e-04,
#          2.56445320e-03,  2.17611938e-03,  1.20528486e-03,
#          2.95278701e-03],
#        [            nan,             nan,             nan,
#                     nan,             nan,             nan,
#                     nan,             nan,             nan,
#                     nan,             nan,  1.29826846e-02,
#          1.24001839e-02,  1.37593522e-02,  1.14293493e-02,
#          1.47301867e-02],
#        [            nan,             nan,             nan,
#                     nan,             nan,             nan,
#                     nan,             nan,             nan,
#                     nan,             nan,             nan,
#         -8.71019826e-05, -8.71019826e-05,  6.89565639e-04,
#          3.01231828e-04],
#        [            nan,             nan,             nan,
#                     nan,             nan,             nan,
#                     nan,             nan,             nan,
#                     nan,             nan,             nan,
#                     nan,  5.19533034e-03,  8.49616773e-03,
#          8.10783392e-03],
#        [            nan,             nan,             nan,
#                     nan,             nan,             nan,
#                     nan,             nan,             nan,
#                     nan,             nan,             nan,
#                     nan,             nan,  3.31426520e-03,
#          3.31426520e-03],
#        [            nan,             nan,             nan,
#                     nan,             nan,             nan,
#                     nan,             nan,             nan,
#                     nan,             nan,             nan,
#                     nan,             nan,             nan,
#         -2.13547841e-03],
#        [            nan,             nan,             nan,
#                     nan,             nan,             nan,
#                     nan,             nan,             nan,
#                     nan,             nan,             nan,
#                     nan,             nan,             nan,
#                     nan]]

#endregion

#uc
# labels = ['Building Height', 'Facade to Site Ratio', 'Building Density', 'Urban Road Volumetric Heat Capacity',
#           'Urban Road Albedo', 'Sensible Anthropogenic Heat', 'Urban Road Thermal Conductivity']
#bc
labels = ['Glazing Ratio', 'Wall U Value', 'Window U Value', 'Window SHGC', 'Infiltration Rate', 'Chiller COP', 'Thermostat Setpoint', 'Equipment Load Density',
          'Lighting Load Density', 'Occupancy Density', 'Wall Albedo', 'Roof Albedo', 'Wall Emissivity', 'Roof Emissivity', 'Floor Height', 'Roof U Value'] 
          

for label in labels:
  if (len(label.split()) > 2):
    labelsplit = label.split()
    labellist = labelsplit[:2] + ["\n"] + labelsplit[2:]
    labelfinal = ""
    for x in labellist:
      labelfinal = labelfinal + str(x) + " "
    labels[labels.index(label)] = str(labelfinal)

# Seaborn setting
sns.set(style='whitegrid', rc={"grid.linewidth": 0.1})
sns.set_context("paper", font_scale=0.9)
# (3.1, 3) Two column paper. Each column is about 3.15 inch wide.
plt.figure(figsize=(10, 6))
plt.xlim(0, 1)
color = sns.color_palette("Set2", 6)

p = sns.barplot(x=data, y=labels, palette=color,  linewidth=0.7)
p.axes.set_title(title,fontsize=15)

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
           c='r', capsize=0.2
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
ax.tick_params(labelsize=6 )
ax.axes.set_title(title,fontsize=9)
plt.subplots_adjust(left = 0.279, bottom= 0.376)
plt.xticks(rotation=90)
plt.show()
