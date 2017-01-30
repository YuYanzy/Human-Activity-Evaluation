__author__ = 'eirikaa'

import matplotlib.pyplot as plt
import csv

def loadtxt():
    # with open ('results_dasstur.txt', 'r') as r:
    #     # print r.read()
    #     lines = r.read().splitlines()
    #     one=lines[:][:15]
    #     four = lines[47:]
    #     print one
    #     print four
    filename='results_dasstur.csv'
    rows = []
    one = []
    two = []
    three = []
    four = []
    csvfile = open(filename, 'r')
    csv_reader = csv.reader(csvfile, delimiter = ' ')
    for row in csv_reader:
        rows.append(row)
    csvfile.close()

    for i in rows:
        one.append(i[0])
        two.append(i[1])
        three.append(i[2])
        four.append(i[3])

    x_list = map(float, one)
    y_list = map(float, two)
    z_list = map(float, three)

    x_list[:] = [x*10 for x in x_list]
    y_list[:] = [y*10 for y in y_list]
    z_list[:] = [z*10 for z in z_list]
    time_list = map(float, four)
    return x_list, y_list, z_list, time_list

def plot(x_list, y_list, z_list, time_list, klasse_x, klasse_y, klasse_z):
    plt.plot(time_list, x_list, 'r', label = 'x-axis')
    plt.plot(time_list, y_list, 'b', label = 'y-axis')
    plt.plot(time_list, z_list, 'g', label = 'z-axis')
    plt.plot(time_list, klasse_x, 'ro')
    plt.plot(time_list, klasse_y, 'bo')
    plt.plot(time_list, klasse_z, 'go')
    # plt.plot(time_list, map(sum, zip(x_list, y_list, z_list)), label = 'x + y + z')
    # plt.plot(time_list, [x*y*z for x,y,z in zip(x_list,y_list,z_list)], label = 'x * y * z')
    plt.legend()
    plt.axis([min(time_list), max(time_list), -50, 50])

    plt.show()


def diff(x_list, y_list, z_list, time_list):
    diff_x = []
    diff_y = []
    diff_z = []
    for i in range(0,len(time_list)-5, 5):
        diff_x.append(abs(max(x_list[i:i+5]) - min(x_list[i:i+5])))
        diff_y.append(abs(max(y_list[i:i+5]) - min(y_list[i:i+5])))
        diff_z.append(abs(max(z_list[i:i+5]) - min(z_list[i:i+5])))
    return diff_x, diff_y, diff_z

def classify(diff_x, diff_y, diff_z):
    class_list_x = []
    class_list_y = []
    class_list_z = []
    for diff in diff_x:
        if diff >= 1:
            class_list_x.append(30)
        else:
            class_list_x.append(-30)

    klasse_x = []
    klasse_y = []
    klasse_z = []
    for j in class_list_x:
        klasse_x.append(j)
        klasse_x.append(j)
        klasse_x.append(j)
        klasse_x.append(j)
        klasse_x.append(j)

    for diff in diff_y:
        if diff >= 1:
            class_list_y.append(35)
        else:
            class_list_y.append(-35)


    for j in class_list_y:
        klasse_y.append(j)
        klasse_y.append(j)
        klasse_y.append(j)
        klasse_y.append(j)
        klasse_y.append(j)

    for diff in diff_z:
        if diff >= 1:
            class_list_z.append(40)
        else:
            class_list_z.append(-40)

    for j in class_list_z:
        klasse_z.append(j)
        klasse_z.append(j)
        klasse_z.append(j)
        klasse_z.append(j)
        klasse_z.append(j)

    return class_list_x, klasse_x, class_list_y, klasse_y, class_list_z, klasse_z

if __name__ == '__main__':

    x_list, y_list, z_list, time_list = loadtxt()
    diff_x, diff_y, diff_z  = diff(x_list, y_list, z_list, time_list)
    class_list_x, klasse_x, class_list_y, klasse_y, class_list_z, klasse_z = classify(diff_x, diff_y, diff_z)
    klasse_x.append(1)
    klasse_x.append(1)
    klasse_x.append(1)
    klasse_x.append(1)

    klasse_y.append(1)
    klasse_y.append(1)
    klasse_y.append(1)
    klasse_y.append(1)

    klasse_z.append(1)
    klasse_z.append(1)
    klasse_z.append(1)
    klasse_z.append(1)

    plot(x_list, y_list, z_list, time_list, klasse_x, klasse_y, klasse_z)