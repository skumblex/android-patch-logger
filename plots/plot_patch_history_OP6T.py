#! /usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
import datetime as dt

import matplotlib
matplotlib.rcParams['hatch.linewidth'] = 8.0

N       = 1200
device  = "OnePlus_6T"
release = "2018-11-06"

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

data = np.loadtxt("../data/" + device + "/" + device + ".patch_history", dtype=str)

date0  = dt.datetime.strptime(data[0,0], "%Y-%m-%d").date()
dateR  = dt.datetime.strptime(release, "%Y-%m-%d").date()
offset = (date0 -dateR).days

pd = np.zeros(len(data))
bd = np.array([])

l = len(data)

g, o, r, p = 0, 0, 0, 0

last_build = dt.datetime.strptime(data[0,5], "%y%m%d").date()
for i, d in enumerate(data):
    date  = dt.datetime.strptime(d[0], "%Y-%m-%d").date()
    patch = dt.datetime.strptime(d[1], "%Y-%m-%d").date()
    build = dt.datetime.strptime(d[5], "%y%m%d").date()

    days_delta  = (date - date0).days + offset
    patch_delta = (date - patch).days

    if build != last_build:
        build_delta = (build - last_build).days
        bd = np.append(bd, [build_delta])
        last_build = build

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

plt.plot(-100, 500, color='mediumseagreen', label=r'$t \leq 30\,\mathrm{days}$')
plt.plot(-100, 500, color='darkorange', label=r'$30 < t \leq 60\,\mathrm{days}$')
plt.plot(-100, 500, color='crimson', label=r'$60 < t \leq 90\,\mathrm{days}$')
plt.plot(-100, 500, color='darkorchid', label=r'$t > 90\,\mathrm{days}$')

N5 = N/4

plt.plot([-1, N], [0]*2, color='black', linestyle='-', linewidth=0.5)

plt.plot([-1, N], [30]*2, color='mediumseagreen', linestyle='--')
plt.plot([-1, N], [60]*2, color='darkorange', linestyle='--')
plt.plot([-1, N], [90]*2, color='crimson', linestyle='--')
plt.plot([-1, N], [120]*2, color='darkorchid', linestyle='--')

plt.fill_between([0, offset], -20, 150, facecolor="white", hatch="\\", edgecolor="0.9")
plt.text(0.1*N5, 135, r'$\diameter = ' + mean_delta + r"\,\mathrm{days}$", verticalalignment='center')

gi, oi, ri, pi = 100*g/l, 100*o/l, 100*r/l, 100*p/l
plt.text(0.1*N5, -14, "{:05.2f}\%".format(gi), color='mediumseagreen')
plt.text(1.1*N5, -14, "{:05.2f}\%".format(oi), color='darkorange')
plt.text(2.1*N5, -14, "{:05.2f}\%".format(ri), color='crimson')
plt.text(3.1*N5, -14, "{:05.2f}\%".format(pi), color='darkorchid')

plt.legend(fontsize=11, loc='upper right', edgecolor='none')
plt.ylabel('Age of the security patch [days]', fontsize=12)
plt.xlabel('Time since release [days]', fontsize=12)
plt.ylim(-20, 150)
plt.xlim(0, N)
plt.yticks(np.linspace(0, 150, 6))
plt.title(device.replace("_", " ") + "; Starting date: " + str(date0), fontsize=12)
plt.savefig(device + '.pdf')
plt.show()
