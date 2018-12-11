import csv
import os

iterations = 15*9
iter_count = 0

np = 1
SA = 24.1
g12 = (4.2*10**6)*(10**(-8))
g21 = (10**8)*(10**(-8))
g23 = (10**6)*(10**(-8))*(SA/24.1)
g32 = (10**5)*(10**(-8))
name = 'SCENARIO_2_NP_1'

with open('cache.csv', 'w') as file:
    write = csv.writer(file)
    write.writerow(['total iterations', iterations])
    write.writerow(['current iteration', 1])
    write.writerow(['name', name])
for i in range(iterations):
    os.system('NPsim.py')
    if iter_count == 15:
        np += 1
        iter_count = 0
    iter_count += 1
    new_iter = ['current iteration']
    with open('cache.csv') as file:
        read = csv.reader(file)
        rowindex = 0
        for row in read:
            rowindex += 1
            if rowindex == 3:
                cur_iter = int(row[1]) + 1
                new_iter.append(cur_iter)
    with open('cache.csv', 'w') as file:
        write = csv.writer(file)
        write.writerow(['total iterations', iterations])
        write.writerow(new_iter)
        write.writerow(['name', name])
    if np == 2:
        SA = 40.7
        g12 = (9.1*10**6)*(10**(-8))
        g21 = (10**8)*(10**(-8))
        g23 = (10**6)*(10**(-8))*(SA/24.1)
        g32 = (10**5)*(10**(-8))
        name = 'SCENARIO_2_NP_2'
    if np == 3:
        SA = 67.9
        g12 = (2.0*10**7)*(10**(-8))
        g21 = (10**8)*(10**(-8))
        g23 = (10**6)*(10**(-8))*(SA/24.1)
        g32 = (10**5)*(10**(-8))
        name = 'SCENARIO_2_NP_3'
    if np == 4:
        SA = 75
        g12 = (1.9*10**7)*(10**(-8))
        g21 = (10**8)*(10**(-8))
        g23 = (10**6)*(10**(-8))*(SA/24.1)
        g32 = (10**5)*(10**(-8))
        name = 'SCENARIO_2_NP_4'
    if np == 5:
        SA = 132
        g12 = (3.8*10**7)*(10**(-8))
        g21 = (10**8)*(10**(-8))
        g23 = (10**6)*(10**(-8))*(SA/24.1)
        g32 = (10**5)*(10**(-8))
        name = 'SCENARIO_2_NP_5'
    if np == 6:
        SA = 238
        g12 = (8.8*10**7)*(10**(-8))
        g21 = (10**8)*(10**(-8))
        g23 = (10**6)*(10**(-8))*(SA/24.1)
        g32 = (10**5)*(10**(-8))
        name = 'SCENARIO_2_NP_6'
    if np == 7:
        SA = 201
        g12 = (9.9*10**7)*(10**(-8))
        g21 = (10**8)*(10**(-8))
        g23 = (10**6)*(10**(-8))*(SA/24.1)
        g32 = (10**5)*(10**(-8))
        name = 'SCENARIO_2_NP_7'
    if np == 8:
        SA = 1.08*10**3
        g12 = (6.1*10**8)*(10**(-8))
        g21 = (10**8)*(10**(-8))
        g23 = (10**6)*(10**(-8))*(SA/24.1)
        g32 = (10**5)*(10**(-8))
        name = 'SCENARIO_2_NP_8'
    if np == 9:
        SA = 3.00*10**3
        g12 = (9.5*10**8)*(10**(-8))
        g21 = (10**8)*(10**(-8))
        g23 = (10**6)*(10**(-8))*(SA/24.1)
        g32 = (10**5)*(10**(-8))
        name = 'SCENARIO_2_NP_9'
    with open('currentsim.csv', 'w') as file:
        write = csv.writer(file)
        write.writerow(['g12', g12])
        write.writerow(['g21', g21])
        write.writerow(['g23', g23])
        write.writerow(['g32', g32])
        write.writerow(['name', name])


# after final iteration --> make another csv with average measurements
