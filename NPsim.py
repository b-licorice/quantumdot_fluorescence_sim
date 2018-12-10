import numpy as np
import random
import math
from collections import Counter
import matplotlib.pyplot as plt
import sys
import time
import csv
import os

# Written and created by Bruce Lickey

# -------------------------------
# todo: read transition rates from an file rather than replacing variables each run
# (apologies to has to run this before I've implemented that)
# -------------------------------

start = time.time()
curdir = os.getcwd()
print(curdir)
iterate = True


################
# transition rates (per 10 nanoseconds)
# QD1 - Scenario 1
g12 = (4.2*10**6)*(10**(-8))
g21 = (10**8)*(10**(-8))
g23 = (10**6)*(10**(-8))
g32 = (10**5)*(10**(-8))
################

f = g12/(g12+g21)
R = g23/g32
fR = f*R
a_on = 0.5
a_off = 0.5
state = 1  # initial state of system (|1>, |2>, or |3>), initially set to 1 (ground)
tfinal = 100000*(10**5)  # total length of trajectory, in 10-nanosecond bins
threshold_percent = 0.1  # Currently, threshold is generated from this value times the maximum photon count recorded

print("f: {},  R: {},  fR: {}".format(round(f, 2), R, round(fR, 2)))


def expRNG(a):  # exponential random number generator **(equivalent to -(1/a)*log(1-y))
    x = np.random.exponential(scale=1/a)
    return x


def transition(g):
    if g >= 1:
        statechange = True
    else:
        roll = random.random()
        if roll >= (1-g):
            statechange = True
        else:
            statechange = False
    return statechange


# Generating initial g_on and g_off conditions:
x1 = expRNG(a_on)
x2 = expRNG(a_off)
g_on = g23*math.exp(-x1)
g_off = g32*math.exp(-x2)

print('\ninitial x = ~'+str(round(x1, 5)), ', ', 'initial g_on = ~'+str(round(g_on/10, 10)), 'ns\u207b\u00b9')
print('initial x\' = ~'+str(round(x2, 5)), ', ', 'initial g_off = ~'+str(round(g_off/10, 10)), 'ns\u207b\u00b9 \n\n')

sub_clock = 0  # each time this hits 10^5 sub-bins (= one 1-ms bin) it resets, and data for that bin is appended
time_ms = 0  # counts time bins in milliseconds
counts = 0  # photon count of each bin
timevalues = []  # Every 1-ms bin, the time is recorded and appended to this list
photoncounts = []  # Every 1-ms bin, the net photon count over the bin time is appended to this list

# the following info is used for providing a dynamic time estimate readout
t_0 = time.time()
calculation_clock = 0
t_i = 0
t_remaining = '--'
current_iter = 'n/a'
total_iter = 'n/a'
if iterate:
    with open('cache.csv') as cache:
        read = csv.reader(cache)
        rowindex = 0
        for row in read:
            rowindex += 1
            if rowindex == 1:
                total_iter = row[1]
            if rowindex == 3:
                current_iter = row[1]

# the main algorithm of the program, which performs a series of calculations to output fluorescence for each 1-ms bin.
for i in range(0, tfinal):
    sub_clock += 1
    if sub_clock == (10 ** 5):
        calculation_clock += 1
        if calculation_clock == 10:  # prints dynamic ETA readout every 10^6 sub-bins
            t_i = time.time() - t_0
            t_remaining = (t_i/i)*(tfinal-i)
            if t_remaining < 120:
                if t_remaining == 1:
                    t_remaining = "1 second"
                else:
                    t_remaining = str(round(t_remaining))+" seconds"
            elif 3600 > t_remaining >= 120:
                t_remaining = "~"+str(round(t_remaining/60))+" minutes"
            elif t_remaining >= 3600:
                if t_remaining//3600 == 1:
                    t_remaining = "1 hour, "+str(round((t_remaining % 3600)/60))+" minutes"
                else:
                    t_remaining = str(round(t_remaining//3600))+" hours, "+str(round((t_remaining % 3600)/60))+" minutes"
            if iterate:
                ETA = ("\r  Computing... {}%        Estimated time remaining: {}       Simulation: {} of {}".format(percent_complete, t_remaining, current_iter, total_iter))
            else:
                ETA = ("\r  Computing... {}%        Estimated time remaining: {}".format(percent_complete, t_remaining))
            calculation_clock = 0
            sys.stdout.write(ETA)
        photoncounts.append(counts)
        time_ms += 1
        timevalues.append(time_ms)
        sub_clock = 0
        counts = 0
        percent_complete = round(100*i/tfinal)
    if state == 1:
        if transition(g12):
            state = 2
    elif state == 2:
        if transition(g_on):
            x1 = expRNG(a_on)  # generates new x if a transition occurs
            g_on = g23*math.exp(-x1)  # generates new g_on
            state = 3
        elif transition(g21):
            counts += 1
            state = 1
    elif state == 3:
        if transition(g_off):
            x2 = expRNG(a_off)
            g_off = g32*math.exp(-x2)
            state = 2



# print(photoncounts)
# print(timevalues)
threshold = max(photoncounts)*threshold_percent
print("\n\nMax counts: ", max(photoncounts))
print("Threshold: ", threshold)


def record_trajectories(photon_count_list):
    nextvalue = 0
    on_list = []
    off_list = []
    on_trajectory = 0
    off_trajectory = 0
    for value in photon_count_list:
        nextvalue += 1
        try:
            if value >= threshold:
                on_trajectory += 1
                if photon_count_list[nextvalue] < threshold:
                    on_list.append(on_trajectory)
                    on_trajectory = 0
            elif value < threshold:
                off_trajectory += 1
                if photon_count_list[nextvalue] >= threshold:
                    off_list.append(off_trajectory)
                    off_trajectory = 0
        except IndexError:
            if photon_count_list[-1] >= threshold and photon_count_list[-2] >= threshold:
                on_list.append(on_trajectory)
            elif photon_count_list[-1] >= threshold > photon_count_list[-2]:
                on_list.append(1)
            elif photon_count_list[-1] < threshold and photon_count_list[-2] < threshold:
                off_list.append(off_trajectory)
            elif photon_count_list[-1] < threshold <= photon_count_list[-2]:
                off_list.append(1)
            break
    return on_list, off_list


ontimes_list = record_trajectories(photoncounts)[0]
# print(ontimes_list)
offtimes_list = record_trajectories(photoncounts)[1]
# print(offtimes_list)

t_on, N_on = list(zip(*Counter(ontimes_list).items()))     # Builds two lists: t_on/off values, and their corresponding
t_off, N_off = list(zip(*Counter(offtimes_list).items()))  # N values. The 'Counter' module calculates N.

# The following is a trivial function for the sole purpose of printing two lists of tuples in the format (t, N). Not
# actually necessary, but useful while coding/proofing.
def sorter(list1, list2):
    sortedlist = sorted(list(zip(list1, list2)), key=lambda tup: tup[0])
    return sortedlist


# print('\nON: (t(ms), N): ', sorter(t_on, N_on))
# print('OFF: (t(ms), N): ', sorter(t_off, N_off), '\n')

# The two lists (t and N) are then paired into a list of tuples, which can then be sorted by the t values (low to high).
sorted_on_values = sorted(list(zip(t_on, N_on)), key=lambda tup: tup[0])
sorted_off_values = sorted(list(zip(t_off, N_off)), key=lambda tup: tup[0])

# The following four lines separate each tuple into its two constituent values in order to change each list of tuples
# into two separate lists with t and N values that correspond to each other ordinally.
t_on = [i[0] for i in sorted_on_values]
N_on = [i[1] for i in sorted_on_values]
t_off = [i[0] for i in sorted_off_values]
N_off = [i[1] for i in sorted_off_values]


def ntotal(N, p):
    Ntot = 0
    try:
        if not p:  # if calculating normally for the sake of counting (i.e. to print to the terminal, just to see it)
            for count in N:
                Ntot += count
            return Ntot
        else:  # if using N to compute probability density, then the first and last values in N must be excluded
            del (N[0], N[-1])
            for count in N:
                Ntot += count
            return Ntot
    except IndexError:
        badtrajectory = True  # The shorter t_total is, the likelier it is to get "bad" simulations with 0-2 events
        pass

N_tot_on = ntotal(N_on, False)
N_tot_off = ntotal(N_off, False)
N_tot_on_p = ntotal(N_on, True)
N_tot_off_p = ntotal(N_off, True)


def pdf(t, N, Ntot):  # Probability density function
    dt_fwd = [t[n+1]-t[n] for n in range(len(t)-1)]  # [t_(i+1) - t_i] for each t
    dt_prev = [t[n]-t[n-1] for n in range(len(t))]  # [t_i - t_(i-1)] for each t in t
    del (dt_fwd[0], dt_prev[0], dt_prev[-1])  # removes first value of both, and final value of dt_prev
    avg_dt = [i/2 for i in [x + y for x, y in zip(dt_fwd, dt_prev)]]  # <dt> = (1/2)*{[t_(i+1) - t_i]+[t_i - t_(i-1)]}
    P = [i/Ntot for i in N]  # P = N/Ntot
    pd = [P / dt for P, dt in zip(P, avg_dt)]
    return pd


pd_on = pdf(t_on, N_on, N_tot_on_p)
pd_off = pdf(t_off, N_off, N_tot_off_p)

del (t_on[0], t_on[-1], t_off[0], t_off[-1])
print('On times (ms): ', t_on)
print('On time N values: ', N_on, '\n')
# print('Total on counts: ',N_tot_on,'\n')
print('Off times (ms): ', t_off)
print('Off time N values: ', N_off, '\n')
# print('Total off counts: ', N_tot_off, '\n')
print('P(t_on): ', pd_on)
print('P(t_off): ', pd_off, '\n')


def log_elements(values):  # a function that applies the base-10 log operation on every item in an input list
    log = [math.log10(n) for n in values]
    return log


log_pd_on = log_elements(pd_on)
log_pd_off = log_elements(pd_off)
log_t_on = log_elements(t_on)
log_t_off = log_elements(t_off)


# Plotting the data: #todo: maybe clean all this up a bit?

def linfit(t, pd):  # function for generating the trendline
    fit_input = np.polyfit(t, pd, 1)
    fit = np.poly1d(fit_input)
    return fit_input, fit(t)

fit_on = linfit(log_t_on, log_pd_on)
fit_off = linfit(log_t_off, log_pd_off)
fig = plt.figure(figsize=(11, 7), num='Simulated Fluorescence Intermittency')

blinkplot = fig.add_subplot(212)
blinkplot.axhline(y=threshold, linewidth=0.6, linestyle='--', color='#abadb2')

blinkplot.plot(timevalues, photoncounts, 'k-')
blinkplot.axis([0, (tfinal*(10**-5)), 0, (max(photoncounts)*1.2)])
blinkplot.set_xlabel('time (ms)')
blinkplot.set_ylabel('Counts/ms')

logploton = fig.add_subplot(221)
logploton.plot(log_t_on, fit_on[1], color='#8b8d91', linestyle='--', linewidth=0.6)
logploton.plot(log_t_on, log_pd_on, 'k.')
fiteq_on = 'y = %.4fx-%0.4f' % (fit_on[0][0], -(fit_on[0][1]))  # todo: fix double negative intercepts
print('Linear fit (ON): ', fiteq_on)
logploton.set_title('On')
logploton.set_xlabel('log(\u03c4)')
logploton.set_ylabel('log(P(\u03c4))')

logplotoff = fig.add_subplot(222)
logplotoff.plot(log_t_off, fit_off[1], color='#8b8d91', linestyle='--', linewidth=0.6)
logplotoff.plot(log_t_off, log_pd_off, 'k.')
fiteq_off = 'y = %.4fx-%0.4f' % (fit_off[0][0], -(fit_off[0][1])) # todo: fix double negative intercepts
print('Linear fit (OFF): ', fiteq_off, '\n')
logplotoff.set_title('Off')
logplotoff.set_xlabel('log(\u03c4)')
logplotoff.set_ylabel('log(P(\u03c4))')

fig.text(0.33, 0.82, fiteq_on)  # todo: Maybe find a better way to format these eventually
fig.text(0.76, 0.82, fiteq_off)

print("Calculation time: %s seconds\n" % (time.time() - start))

if iterate:  # todo: 1) prevent overwrite of existing iterated simulations of the same kind, 2) save linear fit data & averaged data
    with open('cache.csv') as file:
        read = csv.reader(file)
        rowindex = 0
        for row in read:
            rowindex += 1
            if rowindex == 3:
                iteration = row[1]
            if rowindex == 5:
                name = row[1]
    save_dir = curdir+'\Simulations\\'+name
    if not os.path.exists(save_dir):
        print('Path does not exist; writing new directories')
        os.makedirs(save_dir+'\\data')
    print('Plot saved to:', save_dir+'\\'+name+'_'+iteration)
    plt.savefig(save_dir+'\\'+name+'_'+iteration)

    csv_dir = save_dir+'\\data\\'+name+'_'+iteration+'.csv'
    with open(csv_dir, 'w', newline='') as file:
        outputcsv = csv.writer(file)
        outputcsv.writerow(['f', 'R', 'fR'])
        outputcsv.writerow([f, R, fR])
        outputcsv.writerow(['g12', 'g21', 'g23', 'g32'])
        outputcsv.writerow([g12*(10**8), g21*(10**8), g23*(10**8), g32*(10**8)])
        outputcsv.writerow([])
        outputcsv.writerow(['m_on', 'b_on', 'm_off', 'b_off'])
        outputcsv.writerow([fit_on[0][0], fit_on[0][1], fit_off[0][0], fit_off[0][1]])
        outputcsv.writerow([])
        outputcsv.writerow(['time', 'photons'])
        for i in range(len(timevalues)):
            outputcsv.writerow([timevalues[i], photoncounts[i]])
    dir_path = os.getcwd()+csv_dir
    print('Data saved to '+dir_path+'\n')
else:
    plt.show()

while not iterate:
    prompt_csv = input('Would you like to export the raw simulated fluorescence data as a .csv file? [Y/N] ')
    if prompt_csv in ['Y', 'y']:
        csvfilename = input('Please name your file: ')
        if csvfilename[-4:] != '.csv':
            csvfilename = csvfilename+'.csv'
        with open(csvfilename, 'w', newline='') as file:
            outputcsv = csv.writer(file)
            for i in range(len(timevalues)):
                outputcsv.writerow([timevalues[i], photoncounts[i]])
        dir_path = os.getcwd()+"\Simulations\data"
        print('File saved to '+dir_path+'\\'+csvfilename)
        break
    elif prompt_csv in ['N', 'n']:
        break
    elif prompt_csv not in ['Y', 'y', 'N', 'n']:
        print('Invalid response.')
