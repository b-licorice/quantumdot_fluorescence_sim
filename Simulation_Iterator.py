import csv
import os

############ CHANGE THIS FOR EACH SIMULATION ############
name = 'Scenario_1_QD1'
############ CHANGE THIS FOR EACH SIMULATION ############

iterations = 15

with open('cache.csv', 'w') as file:
    write = csv.writer(file)
    write.writerow(['total iterations', iterations])
    write.writerow(['current iteration', 1])
    write.writerow(['name', name])
for i in range(iterations):
    os.system('NPsim.py')
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

# todo: after final iteration --> make another csv with average measurements
