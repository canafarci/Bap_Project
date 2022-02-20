from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np
from math import nan
#with open("E:\\ARCHIVE\\BAP\\__Project\\txtexport\\sobol-urban_characteristics-1-22-uc-w.txt", "r") as reader:
#    print(reader.read())


#region __SETVARS__
#region __Urban Characteristics - Winter__
       # uc - w - to
""" data = [2.96593986e-01, 6.11846713e-01, 1.10763736e-01, 2.74452963e-02,
        2.63290209e-04, 9.68728378e-03, 7.13918462e-03]
error = [2.72369845e-02, 4.54595674e-02, 1.06176536e-02, 2.53865872e-03,
         6.41272937e-05, 9.82683346e-04, 6.99095304e-04]
# uc - w - 2nd
arr = [[nan,  1.64573572e-02, -1.60642278e-02,
        -9.31802193e-03, -1.11239452e-02, -1.29057267e-02,
        -1.03307992e-02],
       [nan,             nan,  7.23727958e-03,
        2.58743440e-03, -6.52250852e-04, -5.08575228e-03,
        6.90831128e-05],
       [nan,             nan,             nan,
        3.03225452e-03,  2.42260085e-03,  2.40071622e-03,
        1.55273602e-03],
       [nan,             nan,             nan,
        nan, -2.19619355e-03, -2.56276104e-03,
        -1.94901013e-03],
       [nan,             nan,             nan,
        nan,             nan,  5.10697626e-04,
        6.98753299e-04],
       [nan,             nan,             nan,
        nan,             nan,             nan,
        -3.89590294e-03],
       [nan,             nan,             nan,
        nan,             nan,             nan,
        nan]] """

#endregion
#region __Urban Characteristics - Summer__
       # uc - s - to
""" data = [0.20478926, 0.51264657, 0.15828731, 0.06006665, 0.0013826,
        0.02074683, 0.09534309]
error = [0.01984144, 0.04066204, 0.01772111, 0.00593957, 0.00021097,
         0.00223178, 0.00893488]
# uc - s - 2nd
arr = [[nan, -0.00734927,  0.0020354, -0.00388779, -0.00185468,
        0.00063547,  0.00072736],
       [nan,         nan,  0.00345251,  0.0023449, -0.00024139,
        0.000169,  0.00369712],
       [nan,         nan,         nan,  0.00559776,  0.0069772,
        0.00794946,  0.00360273],
       [nan,         nan,         nan,         nan,  0.00184033,
        0.00186703,  0.00272257],
       [nan,         nan,         nan,         nan,         nan,
        0.00182233,  0.00147589],
       [nan,         nan,         nan,         nan,         nan,
        nan,  0.00510871],
       [nan,         nan,         nan,         nan,         nan,
        nan,         nan]] """
#endregion
#region __Building Characteristics - Winter__
       # bc - w - to
"""data = [1.16514812e-02, 4.67923989e-02, 1.11358331e-02, 6.25147811e-04, 7.35338799e-01, 0.00000000e+00, 1.12900133e-01, 4.72918486e-03,
        2.86836495e-03, 1.37014428e-03, 4.28154419e-03, 5.88939312e-03, 1.15180696e-02, 1.79423625e-02, 6.15682692e-03, 1.29555175e-01]
error = [0.00107755, 0.00593948, 0.00094607, 0.00014118, 0.03744104,       0., 0.00770599, 0.00047985, 0.0003517,
         0.00017042,       0.00036507, 0.00044393, 0.00085334, 0.00153413, 0.00055331,       0.01108711] 
# bc - w - 2nd
arr = [[nan, -7.63524540e-05, -1.09781396e-03,
        -2.26673206e-03,  1.03972810e-03, -2.40480388e-03,
        -1.47461890e-03, -2.01257192e-03, -2.39882591e-03,
        -2.45108493e-03, -2.17134165e-03, -2.37729236e-03,
        -2.46747614e-03, -1.81298486e-03, -1.70531712e-03,
        -2.49010244e-03],
       [nan,             nan,  2.80339160e-03,
        3.19086690e-03,  3.33793782e-03,  3.49355787e-03,
        3.22615621e-03,  3.36532078e-03,  3.48828697e-03,
        3.25424624e-03,  3.77381539e-03,  2.89318971e-03,
        3.37939793e-03,  2.72818489e-03,  4.03279647e-03,
        8.90471340e-03],
       [nan,             nan,             nan,
        1.18566927e-03,  1.68608321e-03,  1.28150963e-03,
        4.11853845e-03,  1.79182257e-03,  1.65683615e-03,
        1.46836940e-03,  1.87821387e-03,  1.84838830e-03,
        1.19331850e-03,  2.31492708e-03,  2.34224575e-03,
        2.91298118e-03],
       [nan,             nan,             nan,
        nan, -1.05599016e-03, -1.11114176e-03,
        -7.01875796e-04, -1.13556787e-03, -1.08138047e-03,
        -1.09082952e-03, -1.08028772e-03, -1.01305163e-03,
        -1.17060006e-03, -1.12541175e-03, -1.13286814e-03,
        -9.80462050e-04],
       [nan,             nan,             nan,
        nan,             nan,  8.33316739e-03,
        8.99961462e-03,  6.86952895e-03,  3.61957025e-03,
        7.60970447e-03,  8.55608782e-03,  4.96686325e-03,
        5.53181355e-03,  7.38177026e-03,  6.73974915e-03,
        2.31237577e-02],
       [nan,             nan,             nan,
        nan,             nan,             nan,
        -1.38777878e-17, -1.73472348e-18, -4.33680869e-19,
        -5.42101086e-19, -2.49366500e-18, -2.92734587e-18,
        -1.73472348e-18,  0.00000000e+00, -1.30104261e-18,
        0.00000000e+00],
       [nan,             nan,             nan,
        nan,             nan,             nan,
        nan, -4.63016428e-03, -3.68365238e-03,
        -3.33590165e-03, -3.65601230e-03, -4.55682166e-03,
        -2.58344879e-03, -4.81451716e-03, -4.53805212e-03,
        -9.19675479e-03],
       [nan,             nan,             nan,
        nan,             nan,             nan,
        nan,             nan, -1.43902409e-03,
        -1.50677442e-03, -1.24258671e-03, -1.02358732e-03,
        -1.41491937e-03, -1.17650765e-03, -8.73752399e-04,
        -7.58371151e-04],
       [nan,             nan,             nan,
        nan,             nan,             nan,
        nan,             nan,             nan,
        -5.38243361e-03, -5.20290167e-03, -5.36000015e-03,
        -5.19030294e-03, -5.41103787e-03, -4.98557354e-03,
        -3.25176943e-03],
       [nan,             nan,             nan,
        nan,             nan,             nan,
        nan,             nan,             nan,
        nan,  1.75162099e-03,  1.83081302e-03,
        1.89412807e-03,  2.03207134e-03,  1.84257612e-03,
        2.12932584e-03],
       [nan,             nan,             nan,
        nan,             nan,             nan,
        nan,             nan,             nan,
        nan,             nan, -2.05010708e-03,
        -1.77544186e-03, -2.11985006e-03, -1.77312781e-03,
        -9.86992623e-04],
       [nan,             nan,             nan,
        nan,             nan,             nan,
        nan,             nan,             nan,
        nan,             nan,             nan,
        -1.39251556e-03, -1.11090819e-03, -1.13392016e-03,
        -2.13982608e-03],
       [nan,             nan,             nan,
        nan,             nan,             nan,
        nan,             nan,             nan,
        nan,             nan,             nan,
        nan,  6.24012052e-03,  5.92489510e-03,
        6.20695243e-03],
       [nan,             nan,             nan,
        nan,             nan,             nan,
        nan,             nan,             nan,
        nan,             nan,             nan,
        nan,             nan,  2.08138046e-03,
        1.42078265e-03],
       [nan,             nan,             nan,
        nan,             nan,             nan,
        nan,             nan,             nan,
        nan,             nan,             nan,
        nan,             nan,             nan,
        4.65375622e-03],
       [nan,             nan,             nan,
        nan,             nan,             nan,
        nan,             nan,             nan,
        nan,             nan,             nan,
        nan,             nan,             nan,
        nan]]"""
#endregion
#region __Building Characteristics - Summer__
       # bc- s - to
data = [0.04794085, 0.19625199, 0.00644066, 0.00090169, 0.02252013,
        0.0310378, 0.51086342, 0.05887428, 0.02422545, 0.01266267,
        0.03563468, 0.07745485, 0.06842793, 0.10018867, 0.04532917,
        0.02745853]  
error = [0.00408713, 0.01657233, 0.00067074, 0.00012613, 0.0018464,
         0.00317362, 0.03110786, 0.00477555, 0.00230218, 0.00115588,
         0.00252008, 0.00650195, 0.00564373, 0.00876725, 0.0037288,
         0.00250117]
# bc- s - 2nd   
arr = [[nan,  4.13964754e-06,  3.40545266e-03,
        3.11167132e-03,  3.79788895e-03,  2.18308409e-03,
        3.98924382e-03,  3.05986258e-03,  2.61422805e-03,
        3.10869381e-03,  4.63218825e-03,  3.16209055e-03,
        3.44435884e-03,  3.63313320e-03,  1.50460799e-03,
        3.21151728e-03],
       [nan,             nan, -1.85257427e-04,
        -1.81157534e-03, -3.18381210e-03, -1.43918765e-03,
        6.45678136e-03, -3.70061770e-04, -1.45169320e-03,
        -1.45248721e-03, -1.25557431e-03,  1.24394909e-03,
        6.73060487e-04, -2.75286664e-03, -1.43124761e-03,
        -9.63976479e-04],
       [nan,             nan,             nan,
        1.30326067e-03,  7.81004792e-04,  1.83206709e-03,
        4.49158221e-03,  1.66909784e-03,  1.74095517e-03,
        8.78468736e-04,  1.48727101e-03,  5.09852555e-04,
        7.14903990e-04,  6.94656898e-04,  9.64419628e-04,
        1.26217099e-03],
       [nan,             nan,             nan,
        nan,  1.83331170e-03,  1.80889608e-03,
        1.93077564e-03,  2.04332565e-03,  1.88730394e-03,
        1.99449443e-03,  1.99111992e-03,  1.98873791e-03,
        2.23646704e-03,  1.85395579e-03,  2.19220133e-03,
        1.97265933e-03],
       [nan,             nan,             nan,
        nan,             nan, -7.60449219e-03,
        1.97516150e-03, -5.28719262e-03, -7.86611638e-03,
        -7.61124122e-03, -7.98104840e-03, -1.10030262e-02,
        -1.20316579e-02, -6.06233865e-03, -6.48137406e-03,
        -9.64408899e-03],
       [nan,             nan,             nan,
        nan,             nan,             nan,
        4.15621196e-03,  3.41997210e-03,  1.11577359e-03,
        -1.56021712e-04,  2.84114346e-03,  5.72278110e-04,
        -4.61514605e-04,  2.99001914e-03,  2.10986612e-03,
        -4.03552340e-04],
       [nan,             nan,             nan,
        nan,             nan,             nan,
        nan,  1.19118568e-02,  2.43046106e-03,
        7.79097801e-03,  1.09715580e-02,  6.41278622e-03,
        7.54166087e-03,  7.56786299e-03,  1.39101654e-02,
        7.08371928e-03],
       [nan,             nan,             nan,
        nan,             nan,             nan,
        nan,             nan,  1.38731718e-03,
        1.40498376e-03,  1.20052782e-03,  4.03353275e-03,
        -5.09954476e-04,  2.99954153e-03,  1.84625127e-03,
        1.29759477e-03],
       [nan,             nan,             nan,
        nan,             nan,             nan,
        nan,             nan,             nan,
        -7.04543962e-03, -7.06925973e-03, -5.21823879e-03,
        -8.67910207e-03, -6.07080018e-03, -3.68581180e-03,
        -8.25093562e-03],
       [nan,             nan,             nan,
        nan,             nan,             nan,
        nan,             nan,             nan,
        nan, -8.14345756e-03, -8.37213061e-03,
        -7.94515516e-03, -7.23491892e-03, -8.46721254e-03,
        -8.04460411e-03],
       [nan,             nan,             nan,
        nan,             nan,             nan,
        nan,             nan,             nan,
        nan,             nan, -3.95256899e-03,
        -7.24033948e-03, -4.39224849e-03, -2.73853745e-03,
        -5.03181841e-03],
       [nan,             nan,             nan,
        nan,             nan,             nan,
        nan,             nan,             nan,
        nan,             nan,             nan,
        4.51509498e-03,  4.24711875e-03,  2.22637954e-03,
        5.20826014e-03],
       [nan,             nan,             nan,
        nan,             nan,             nan,
        nan,             nan,             nan,
        nan,             nan,             nan,
        nan, -1.25275122e-03, -6.55768792e-03,
        -7.61966776e-03],
       [nan,             nan,             nan,
        nan,             nan,             nan,
        nan,             nan,             nan,
        nan,             nan,             nan,
        nan,             nan,  1.05178911e-02,
        1.06923734e-02],
       [nan,             nan,             nan,
        nan,             nan,             nan,
        nan,             nan,             nan,
        nan,             nan,             nan,
        nan,             nan,             nan,
        -4.97614518e-04],
       [nan,             nan,             nan,
        nan,             nan,             nan,
        nan,             nan,             nan,
        nan,             nan,             nan,
        nan,             nan,             nan,
        nan]]
#endregion
#endregion

#uc
""" labels = ['Building Height', 'Facade to Site Ratio', 'Building Density', 'Urban Road Volumetric Heat Capacity',
          'Urban Road Albedo', 'Sensible Anthropogenic Heat', 'Urban Road Thermal Conductivity'] """
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
ax.tick_params(labelsize=12)
plt.xticks(rotation=90)
plt.show()
