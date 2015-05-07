from __future__ import print_function
import matplotlib
matplotlib.use('wxagg')
# matplotlib.rcParams['backend.multifigure'] = True
# matplotlib.rcParams['toolbar'] = 'toolmanager'
 
import matplotlib.pyplot as plt
import numpy as np

figure = plt.figure()
ax = figure.add_subplot(211)
ax2 = figure.add_subplot(212)

shape = (1024, 1280)
img1 = np.random.rand(*shape) *  65 + 81
img2 = np.random.rand(*shape) *  8 + 7
id_ = 2

bmin = []
bmax = []
dmin = []
dmax = []
length = []

profile = np.mean(img1, axis=0).tolist()
profile_min = np.min(img1, axis=0).tolist()
profile_max = np.max(img1, axis=0).tolist()
x = np.arange(np.shape(profile)[0]).tolist()
l = np.shape(img1)[0]
profile_mid = img1[l // 2, :].tolist()

length.append(np.shape(profile)[0])

avg_ = np.mean(img1)
del img1
bmax.append(1.1 * avg_)
bmin.append(0.9 * avg_)

ax.plot(x, profile_mid,
        label='50% mid',
        gid='%d:marker' % id_)
ax.plot(x, profile_min,
        label='50% min',
        gid='%d:marker' % id_)
ax.plot(x, profile_max,
        label='50% max',
        gid='%d:marker' % id_)
ax.plot(x, profile,
        label='50% mean',
        gid='%d:marker' % id_)

#     img = r.spatial['avg_dark'][0]
profile_dark = np.mean(img2, axis=0).tolist()
profile_dark_min = np.min(img2, axis=0).tolist()
profile_dark_max = np.max(img2, axis=0).tolist()
x_dark = np.arange(np.shape(profile_dark)[0]).tolist()

l = np.shape(img2)[0]
profile_dark_mid = img2[l // 2, :].tolist()
del img2
avg_ = np.mean(profile_dark_max)
dmax.append(1.1 * avg_)

avg_ = np.mean(profile_dark_min)
dmin.append(0.9 * avg_)

ax2.plot(x_dark, profile_dark_mid,
         label='Dark mid',
         gid='%d:marker' % id_)
ax2.plot(x_dark, profile_dark_min,
         label='Dark min',
         gid='%d:marker' % id_)
ax2.plot(x_dark, profile_dark_max,
         label='Dark max',
         gid='%d:marker' % id_)
ax2.plot(x_dark, profile_dark,
         label='Dark mean',
         gid='%d:marker' % id_)


 
# for i in range(5):
#     fig = plt.figure(i)
#     ax = fig.add_subplot(111)
#     for j in range(5):
#         ax.plot(np.random.rand(1400))
 
plt.show()