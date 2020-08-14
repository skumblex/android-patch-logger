#! /usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
import datetime as dt

plt.rc('text', usetex=True)
plt.rc('font', family='serif', size=14)
plt.rcParams['text.latex.preamble']=r"\usepackage{amsmath}\usepackage{mathpazo}\usepackage{mathabx}"

fig = plt.figure(figsize=(0.4*12.0, 0.4*11.0), dpi=150, edgecolor="white")
ax = fig.add_subplot(1,1,1)
ax.tick_params(axis='both', which='both', labelsize=11, direction="in", width=0.5)
ax.xaxis.set_ticks_position('both')
ax.yaxis.set_ticks_position('both')
for axis in ['top','bottom','left','right']:
    ax.spines[axis].set_linewidth(0.5)

data = np.loadtxt("patch_history", dtype=str)

date0 = dt.datetime.strptime(data[0,0], "%Y-%m-%d").date()

last_date = date0
last_build = dt.datetime.strptime(data[0,5], "%y%m%d").date()
pd = np.zeros(len(data))
bd = np.array([])

l = len(data)

g = 0
o = 0
r = 0
p = 0
for i, d in enumerate(data):
    date  = dt.datetime.strptime(d[0], "%Y-%m-%d").date()
    patch = dt.datetime.strptime(d[1], "%Y-%m-%d").date()
    build = dt.datetime.strptime(d[5], "%y%m%d").date()

    days_delta  = (date - date0).days
    patch_delta = (date - patch).days

    if build != last_build:
        build_delta = -(last_build - build).days
        bd = np.append(bd, [build_delta])
        last_build = build
        last_date = date

    pd[i] = patch_delta

    if patch_delta <= 30:
        col = 'mediumseagreen'
        g += 1
    elif patch_delta <= 60:
        col = 'darkorange'
        o += 1
    elif patch_delta <= 90:
        col = 'crimson'
        r += 1
    else:
        col = 'darkorchid'
        p += 1

    plt.plot(days_delta, patch_delta, "*", color=col)

print(g/l*100, o/l*100, r/l*100, p/l*100)
print(np.mean(pd), np.mean(bd), np.sqrt(np.var(bd)))
mean_delta = str(int(np.mean(pd*10))/10)

plt.plot(0, 500, color='mediumseagreen', label=r'$t \leq 30\,\mathrm{days}$')
plt.plot(0, 500, color='darkorange', label=r'$30 < t \leq 60\,\mathrm{days}$')
plt.plot(0, 500, color='crimson', label=r'$60 < t \leq 90\,\mathrm{days}$')
plt.plot(0, 500, color='darkorchid', label=r'$t > 90\,\mathrm{days}$')

plt.plot([-1, 1000], [30]*2, color='mediumseagreen', linestyle='--')
plt.plot([-1, 1000], [60]*2, color='darkorange', linestyle='--')
plt.plot([-1, 1000], [90]*2, color='crimson', linestyle='--')

plt.text(5, 130, r'$\diameter = ' + mean_delta + r"\,\mathrm{days}$")

plt.legend(fontsize=11)
plt.ylabel('Age of the security patch [days]', fontsize=12)
plt.xlabel('Time since start of data collection [days]', fontsize=12)
plt.ylim(0, 150)
plt.xlim(-5, 505)
plt.yticks(np.linspace(0, 150, 6))
plt.title("OnePlus 6T; Starting date: 2019-04-09", fontsize=12)
plt.savefig('oneplus_patch.png')
plt.show()
