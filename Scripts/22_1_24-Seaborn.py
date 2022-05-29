from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np
from math import nan
import textwrap

# region  #* urban characteristics
# title = "Urban Characteristics - Winter - Second Order"
# data =[6.01021856e-01, 1.65082396e-01, 2.33660065e-01, 2.05898400e-03,
#        1.88796953e-04, 1.36925895e-02, 3.62040993e-03]
# error = [5.00805623e-02, 1.52007149e-02, 2.14246140e-02, 2.29365805e-04,
#        2.60131293e-05, 1.54325164e-03, 3.35143318e-04]
# # uc - s - 2nd
# arr = [[        nan, -0.03163857, -0.01259029, -0.02209727, -0.02130441,
#         -0.01990062, -0.02106891],
#        [        nan,         nan, -0.00146443,  0.00325344,  0.00109787,
#          0.00139228,  0.00266224],
#        [        nan,         nan,         nan,  0.00557354,  0.00637656,
#          0.00619035,  0.00640569],
#        [        nan,         nan,         nan,         nan, -0.00167502,
#         -0.00182544, -0.00175901],
#        [        nan,         nan,         nan,         nan,         nan,
#         -0.00057633, -0.00060616],
#        [        nan,         nan,         nan,         nan,         nan,
#                 nan,  0.00034592],
#        [        nan,         nan,         nan,         nan,         nan,
#                 nan,         nan]]
#endregion


#region  #* building characteristics 
       # bc - w - to
title = "Building Characteristics - Winter - Total Order"
data =[1.18637989e-01, 1.93739897e-01, 9.92413493e-02, 1.89442882e-03,
       4.64096982e-01, 0.00000000e+00, 1.42638465e-01, 2.68631823e-04,
       1.24303768e-04, 3.46868790e-05, 2.85373440e-04, 4.94588937e-04,
       4.63841262e-04, 2.84498061e-05, 8.66296596e-04, 2.26405746e-03]

error = [1.71317828e-02, 2.36559059e-02, 1.03935899e-02, 2.64822827e-04,
       4.53474197e-02, 0.00000000e+00, 1.29864253e-02, 3.25205913e-05,
       2.11344819e-05, 1.21511366e-05, 4.23254852e-05, 7.55458998e-05,
       1.66170155e-04, 1.14925103e-05, 1.15898885e-04, 3.26065310e-04]
# bc - w - 2nd"""
arr = [[            nan, -3.93720282e-03,  8.85914698e-04,
        -5.45357748e-03, -4.34906847e-03, -6.07837899e-03,
        -7.84642502e-03, -6.17007491e-03, -6.27752764e-03,
        -5.99784416e-03, -6.15760076e-03, -5.78381408e-03,
        -5.93919379e-03, -6.04380154e-03, -5.89805099e-03,
        -5.99828185e-03],
       [            nan,             nan, -8.71330636e-03,
        -6.64872581e-03, -1.02581308e-02, -6.53602081e-03,
        -7.60135663e-03, -6.64719390e-03, -6.78068914e-03,
        -6.71722419e-03, -6.67279872e-03, -5.79369972e-03,
        -6.66776530e-03, -6.44104223e-03, -6.43622764e-03,
        -4.63776221e-03],
       [            nan,             nan,             nan,
         3.20535308e-03, -4.40524701e-05,  3.14407657e-03,
        -3.10831543e-03,  2.86286118e-03,  2.97009507e-03,
         3.11869059e-03,  2.92654498e-03,  3.03749922e-03,
         3.11212525e-03,  3.04625301e-03,  3.10271493e-03,
         1.88681399e-03],
       [            nan,             nan,             nan,
                    nan, -2.10232656e-03, -2.46582754e-03,
        -1.90937279e-04, -2.49274544e-03, -2.47545671e-03,
        -2.47655093e-03, -2.51813142e-03, -2.52075756e-03,
        -2.48946277e-03, -2.47742631e-03, -2.45225918e-03,
        -2.70546245e-03],
       [            nan,             nan,             nan,
                    nan,             nan, -2.23245821e-03,
        -5.63352311e-03, -2.66577064e-03, -2.15542489e-03,
        -2.30839731e-03, -1.20738981e-03, -2.29132743e-03,
        -1.99369869e-03, -2.54562492e-03, -2.90803168e-03,
        -3.20106469e-03],
       [            nan,             nan,             nan,
                    nan,             nan,             nan,
         0.00000000e+00, -7.58941521e-19, -2.43945489e-19,
         1.21972744e-19, -1.73472348e-18,  1.08420217e-18,
        -4.33680869e-19, -4.06575815e-19, -1.08420217e-18,
        -3.25260652e-19],
       [            nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,  4.19588502e-03,  3.90854197e-03,
         3.75009844e-03,  3.99673637e-03,  3.91707692e-03,
         3.96806772e-03,  3.56473701e-03,  4.62000597e-03,
         4.33660213e-03],
       [            nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan, -2.91618571e-04,
        -2.92275105e-04, -2.95338930e-04, -2.79363270e-04,
        -2.64481833e-04, -3.00153513e-04, -2.91180882e-04,
        -2.92275105e-04],
       [            nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,             nan,
         1.07609408e-04,  1.09141320e-04,  9.68860194e-05,
         9.92933107e-05,  1.06734029e-04,  1.20302398e-04,
         1.21396622e-04],
       [            nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,  4.96981796e-05,  4.70720437e-05,
         5.45127622e-05,  4.48835971e-05,  4.51024417e-05,
         4.94793350e-05],
       [            nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,  1.22216652e-03,
         1.18168025e-03,  1.17927296e-03,  1.24492636e-03,
         1.12828216e-03],
       [            nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,             nan,
        -1.40018017e-04, -1.29513473e-04, -1.67373600e-04,
        -2.90145455e-04],
       [            nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,  8.82704414e-04,  8.61914172e-04,
         7.86193918e-04],
       [            nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan, -3.45429705e-04,
        -3.21356792e-04],
       [            nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,             nan,
        -1.10654847e-03],
       [            nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan]]

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
#plt.show()
