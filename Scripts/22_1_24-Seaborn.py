from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np
from math import nan
#with open("E:\\ARCHIVE\\BAP\\__Project\\txtexport\\sobol-urban_characteristics-1-22-uc-w.txt", "r") as reader:
#    print(reader.read())


#region __SETVARS__
#region __Urban Characteristics - Winter__
""" title = "Urban Characteristics - Winter"
       # uc - w - to
data = [6.36609664e-01, 1.73635971e-01, 2.08944078e-01, 4.23820357e-03,
       2.69171884e-04, 1.28723457e-02, 6.10045043e-03]
error = [5.72584255e-02, 1.67711259e-02, 2.37210310e-02, 5.26991760e-04,
       3.66723575e-05, 1.36850744e-03, 6.23816297e-04]
        # uc - w - 2nd
arr = [[        nan, -0.04958324, -0.0222538 , -0.0316588 , -0.03419532,
        -0.03516461, -0.03425091],
       [        nan,         nan,  0.00588363,  0.00750888,  0.00828909,
         0.00823251,  0.00864467],
       [        nan,         nan,         nan,  0.00776457,  0.0085031 ,
         0.00896647,  0.00789076],
       [        nan,         nan,         nan,         nan,  0.00104198,
         0.00113671,  0.00116203],
       [        nan,         nan,         nan,         nan,         nan,
        -0.00022336, -0.00038441],
       [        nan,         nan,         nan,         nan,         nan,
                nan,  0.00022295],
       [        nan,         nan,         nan,         nan,         nan,
                nan,         nan]] """

""" title = "Urban Characteristics - Winter"
       # uc - w - to
data =[0.29759007, 0.11030094, 0.30194986, 0.0696635 , 0.00248818,
       0.09028254, 0.15924515]
error = [0.02850278, 0.00960328, 0.02667759, 0.00643377, 0.00031487,
       0.00829487, 0.01429252]
        # uc - w - 2nd
arr = [[            nan, -1.96457579e-02, -1.26298931e-02,
        -1.29717930e-02, -1.57012947e-02, -1.15133360e-02,
        -1.27536755e-02],
       [            nan,             nan,  4.37438416e-03,
         3.00301136e-03,  3.43695263e-03,  4.39354712e-03,
         3.59698929e-03],
       [            nan,             nan,             nan,
         4.07082530e-03,  5.09526704e-03,  5.16355822e-03,
         4.43107424e-03],
       [            nan,             nan,             nan,
                    nan,  2.27066338e-03,  2.39074636e-03,
         2.23618484e-03],
       [            nan,             nan,             nan,
                    nan,             nan,  8.83115110e-05,
         2.92688624e-05],
       [            nan,             nan,             nan,
                    nan,             nan,             nan,
         1.27823002e-03],
       [            nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan]] """

#endregion
#region __Urban Characteristics - Summer__
       # uc - s - to
""" title = "Urban Characteristics - Summer"
data = [0.36264666, 0.08167319, 0.20944607, 0.13204661, 0.00080408,
       0.04011318, 0.20603495]
error = [0.02867638, 0.00685635, 0.01772947, 0.01115722, 0.00010567,
       0.00402506, 0.01801403]
# uc - s - 2nd
arr = [[        nan, -0.00535842,  0.00352694, -0.00197054, -0.00354302,
        -0.00285278, -0.00098688],
       [        nan,         nan,  0.00200531,  0.00148061,  0.00155637,
         0.00099119,  0.0026226 ],
       [        nan,         nan,         nan,  0.00424754,  0.00316047,
         0.00400984,  0.00201568],
       [        nan,         nan,         nan,         nan, -0.00320313,
        -0.00322317, -0.00155208],
       [        nan,         nan,         nan,         nan,         nan,
        -0.00147902, -0.0010381 ],
       [        nan,         nan,         nan,         nan,         nan,
                nan,  0.00228608],
       [        nan,         nan,         nan,         nan,         nan,
                nan,         nan]] """
                
title = "Urban Characteristics - Winter - UHII"
data = [6.01021856e-01, 1.65082396e-01, 2.33660065e-01, 2.05898400e-03,
       1.88796953e-04, 1.36925895e-02, 3.62040993e-03]
error = [5.00805623e-02, 1.52007149e-02, 2.14246140e-02, 2.29365805e-04,
       2.60131293e-05, 1.54325164e-03, 3.35143318e-04]
# uc - s - 2nd
arr = [[        nan, -0.02032214, -0.00567168, -0.01593407, -0.01301886,
        -0.01260632, -0.01269754],
       [        nan,         nan, -0.00921614, -0.00968526, -0.01072775,
        -0.01269923, -0.01053605],
       [        nan,         nan,         nan,  0.00588044,  0.00574155,
         0.00538731,  0.00508039],
       [        nan,         nan,         nan,         nan, -0.0003252 ,
        -0.0013286 , -0.00013796],
       [        nan,         nan,         nan,         nan,         nan,
         0.00106155,  0.00079818],
       [        nan,         nan,         nan,         nan,         nan,
                nan, -0.00114689],
       [        nan,         nan,         nan,         nan,         nan,
                nan,         nan]]
#endregion
#region __Building Characteristics - Winter__
       # bc - w - to
title = "Building Characteristics - Winter - UHII"
data = [1.18637989e-01, 1.93739897e-01, 9.92413493e-02, 1.89442882e-03,
       4.64096982e-01, 0.00000000e+00, 1.42638465e-01, 2.68631823e-04,
       1.24303768e-04, 3.46868790e-05, 2.85373440e-04, 4.94588937e-04,
       4.63841262e-04, 2.84498061e-05, 8.66296596e-04, 2.26405746e-03]

error = [1.71317828e-02, 2.36559059e-02, 1.03935899e-02, 2.64822827e-04,
       4.53474197e-02, 0.00000000e+00, 1.29864253e-02, 3.25205913e-05,
       2.11344819e-05, 1.21511366e-05, 4.23254852e-05, 7.55458998e-05,
       1.66170155e-04, 1.14925103e-05, 1.15898885e-04, 3.26065310e-04]
# bc - w - 2nd"""
"""
arr = [[            nan, -1.02152745e-02,  8.75475691e-03,
        -9.66498537e-03, -6.91771017e-03, -1.00265543e-02,
        -7.00367113e-03, -9.77075674e-03, -9.73217857e-03,
        -9.94418472e-03, -1.00205301e-02, -1.09114193e-02,
        -1.20129244e-02, -1.07332415e-02, -9.91394777e-03,
        -1.06387076e-02],
       [            nan,             nan,  9.11158068e-03,
         6.57515311e-03,  9.19325518e-03,  6.98943397e-03,
         5.22074667e-03,  6.69598503e-03,  6.62438951e-03,
         6.71185653e-03,  7.09926010e-03,  5.77729175e-03,
         4.35882006e-03,  7.30246161e-03,  7.18023949e-03,
         5.87321584e-03],
       [            nan,             nan,             nan,
         1.79306462e-03, -2.47208188e-03,  2.25055765e-03,
         2.66657626e-03,  2.19749819e-03,  2.34717684e-03,
         2.43950957e-03,  2.09856199e-03,  1.95873062e-03,
         2.28878826e-03,  1.43833084e-03,  2.15173730e-03,
         2.14362778e-03],
       [            nan,             nan,             nan,
                    nan,  3.79185846e-04, -3.50787210e-04,
        -7.57074388e-04, -3.50671360e-04, -3.24489181e-04,
        -3.51366462e-04, -5.70207773e-04, -3.14062649e-04,
        -5.49702261e-04, -4.44510143e-04, -3.13251697e-04,
        -5.08691237e-04],
       [            nan,             nan,             nan,
                    nan,             nan, -2.84381770e-03,
         8.90896862e-03, -2.63934184e-03, -3.01921513e-03,
        -3.17723501e-03, -2.85540274e-03, -2.67907851e-03,
        -2.86826213e-03, -9.05182815e-05, -3.09961528e-03,
         1.41935933e-03],
       [            nan,             nan,             nan,
                    nan,             nan,             nan,
         0.00000000e+00,  7.31836466e-19, -1.51788304e-18,
         7.04731412e-19,  7.58941521e-19,  4.33680869e-19,
         0.00000000e+00,  8.67361738e-19,  2.27682456e-18,
         8.67361738e-19],
       [            nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan, -9.61996117e-04, -1.18871525e-03,
        -1.10414450e-03, -1.12302810e-03, -1.17087430e-03,
        -1.71316979e-03, -1.74051047e-03, -6.85808882e-04,
        -5.75403499e-04],
       [            nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,  8.75898709e-04,
         8.58868707e-04,  8.82270478e-04,  8.72770749e-04,
         8.89453200e-04,  9.19574291e-04,  8.57478503e-04,
         7.62017815e-04],
       [            nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,             nan,
        -7.17028004e-04, -7.17491405e-04, -7.29076440e-04,
        -5.01778053e-04, -7.04632016e-04, -7.04284465e-04,
        -7.55374470e-04],
       [            nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan, -1.13649194e-04, -1.17588105e-04,
        -1.53501714e-04, -1.27551236e-04, -1.20252664e-04,
        -1.12374840e-04],
       [            nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan, -1.90929229e-04,
        -3.03883320e-04, -1.22809223e-04, -2.16763857e-04,
        -3.50455161e-04],
       [            nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,             nan,
        -5.75332317e-04, -4.02020193e-04, -5.90161162e-04,
        -6.40556065e-04],
       [            nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,  8.50648026e-04, -1.55628116e-04,
        -1.47307830e-03],
       [            nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,  3.14260882e-03,
         3.28707420e-03],
       [            nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,             nan,
         3.02113240e-04],
       [            nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan]] """
#endregion
#region __Building Characteristics - Summer__
       # bc- s - to
       
""" title = "Building Characteristics - Summer"
data = [0.38671033, 0.01703526, 0.00202169, 0.00289366, 0.0056419 ,
       0.02846277, 0.30894634, 0.0163477 , 0.00550074, 0.00114346,
       0.01219618, 0.00235608, 0.23176034, 0.0073107 , 0.01259146,
       0.00174906]  
error = [0.02637021, 0.00172131, 0.00025307, 0.00033975, 0.00059167,
       0.00262662, 0.01990693, 0.00135511, 0.00051834, 0.00011692,
       0.0016947 , 0.00023089, 0.01707427, 0.00061142, 0.00108863,
       0.00020987]
# bc- s - 2nd   
arr = [[            nan,  6.66515467e-03,  5.88482258e-03,
         4.68216633e-03,  7.49557373e-03,  6.59230091e-03,
         8.50414300e-03,  5.49664863e-03,  5.22913872e-03,
         4.98268810e-03,  1.76951004e-02,  5.06806361e-03,
         9.73981111e-03,  4.25187380e-03,  6.27071985e-03,
         5.29231659e-03],
       [            nan,             nan,  2.29571013e-03,
         2.15171012e-03,  2.52110146e-03,  1.35601043e-03,
        -9.00748687e-04,  2.36457970e-03,  2.30937021e-03,
         2.09706979e-03,  2.48125956e-03,  1.90469033e-03,
        -1.30092483e-04,  2.11755991e-03,  2.46987616e-03,
         2.04584449e-03],
       [            nan,             nan,             nan,
        -1.42945085e-04, -1.46929275e-04, -3.11988580e-04,
        -4.87292945e-04,  1.62699215e-04, -1.08225714e-04,
        -2.12952997e-04, -1.91324536e-04, -1.02534013e-04,
        -2.70439169e-04, -2.14091337e-04, -3.34755380e-04,
        -1.66281055e-04],
       [            nan,             nan,             nan,
                    nan, -9.55113165e-04, -9.98370086e-04,
        -8.47540031e-04, -6.89310767e-04, -8.90796953e-04,
        -1.01430685e-03,  2.00301970e-04, -9.71619095e-04,
        -8.25911571e-04, -8.60630942e-04, -9.11287073e-04,
        -1.11049658e-03],
       [            nan,             nan,             nan,
                    nan,             nan, -1.55366733e-04,
         1.24095746e-04,  4.57004221e-06,  2.31099709e-04,
        -2.35050535e-04, -2.77738286e-04, -1.80979383e-04,
         7.28554304e-04,  2.33526528e-05, -5.57619796e-05,
        -2.36758045e-04],
       [            nan,             nan,             nan,
                    nan,             nan,             nan,
         2.61181417e-03,  1.16384564e-03,  1.79847021e-03,
         7.97869321e-04,  1.47290496e-03,  1.02212231e-03,
         1.70171131e-03,  1.24125276e-03,  1.27824882e-03,
         1.17864406e-03],
       [            nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan, -2.21440004e-03, -2.39539610e-03,
        -1.77500078e-03, -1.68450275e-03, -2.34644748e-03,
        -2.28611546e-03, -2.95716691e-03, -2.89285070e-03,
        -9.98652880e-04],
       [            nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,  3.19338915e-03,
         2.98621126e-03,  2.67829028e-03,  2.86668556e-03,
         2.14440881e-03,  2.82912034e-03,  3.28957888e-03,
         2.93555513e-03],
       [            nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,             nan,
         2.60621481e-04,  3.67056274e-04,  9.84080258e-05,
        -1.20840633e-03,  8.87321355e-05,  4.59830987e-04,
         1.09222256e-04],
       [            nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,  1.33736882e-04,  1.56503683e-04,
         8.69104544e-04,  5.23455693e-05, -9.16544450e-05,
         1.12677591e-04],
       [            nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,  9.46655250e-03,
         9.64982525e-03,  9.73975411e-03,  1.01393115e-02,
         9.46256831e-03],
       [            nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,             nan,
         3.13053241e-04, -4.12069361e-04, -4.72970553e-04,
        -4.74678063e-04],
       [            nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan, -3.98057567e-05,  4.58787178e-04,
        -5.62303833e-04],
       [            nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan, -1.08755323e-03,
        -4.19347627e-04],
       [            nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,             nan,
         7.55639526e-04],
       [            nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan,             nan,             nan,
                    nan]] """
#endregion
#endregion

#uc
labels = ['Building Height', 'Facade to Site Ratio', 'Building Density', 'Urban Road Volumetric Heat Capacity',
          'Urban Road Albedo', 'Sensible Anthropogenic Heat', 'Urban Road Thermal Conductivity']
#bc
labels = ['Glazing Ratio', 'Wall U Value', 'Window U Value', 'Window SHGC', 'Infiltration Rate', 'Chiller COP', 'Thermostat Setpoint', 'Equipment Load Density',
          'Lighting Load Density', 'Occupancy Density', 'Wall Albedo', 'Roof Albedo', 'Wall Emissivity', 'Roof Emissivity', 'Floor Height', 'Roof U Value'] 
          
# Seaborn setting
sns.set(style='whitegrid', rc={"grid.linewidth": 0.1})
sns.set_context("paper", font_scale=0.9)
# (3.1, 3) Two column paper. Each column is about 3.15 inch wide.
plt.figure(figsize=(10, 6))
plt.xlim(0, 1)
color = sns.color_palette("Set2", 6)

p = sns.barplot(x=data, y=labels, palette=color,  linewidth=0.7)
p.axes.set_title(title,fontsize=20)

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

""" np.random.seed(0)
uniform_data = arr
ax = sns.heatmap(uniform_data)
ax.set_yticklabels(labels, rotation=0)
ax.set_xticklabels(labels)
ax.tick_params(labelsize=12)
ax.axes.set_title(title,fontsize=20)
plt.subplots_adjust(left = 0.279, bottom= 0.376)
plt.xticks(rotation=90)
plt.show() """
