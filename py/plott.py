# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import csv

__author__ = 'eirikaa'


def loadcsv():

    filename = 'accelerometer0.csv'
    rows = []
    x = []
    y = []
    z = []
    time = []
    absoloute = []
    csvfile = open(filename, 'r')
    csv_reader = csv.reader(csvfile, delimiter=' ')
    for row in csv_reader:
        rows.append(row)
    csvfile.close()

    for data in rows:
        x.append(data[1])
        y.append(data[2])
        z.append(data[3])
        time.append(data[5])
        absoloute.append(data[4])

    x_list = list(map(float, x))
    y_list = list(map(float, y))
    z_list = list(map(float, z))
    xyz_list = list(map(float, absoloute))
    time_list = list(map(float, time))
    return x_list, y_list, z_list, time_list, xyz_list


def plot(x_list, y_list, z_list, time_list, klasse_x, klasse_y, klasse_z):

    plt.plot(time_list, x_list, 'r', label='x-axis')
    plt.plot(time_list, y_list, 'b', label='y-axis')
    plt.plot(time_list, z_list, 'g', label='z-axis')
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

    for value in range(0, len(time_list)-5, 5):
        diff_x.append(abs(max(x_list[value:value+5]) - min(x_list[value:value+5])))
        diff_y.append(abs(max(y_list[value:value+5]) - min(y_list[value:value+5])))
        diff_z.append(abs(max(z_list[value:value+5]) - min(z_list[value:value+5])))

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

    x_list, y_list, z_list, time_list, xyz_list = loadcsv()

    diff_x, diff_y, diff_z = diff(x_list, y_list, z_list, time_list)
    class_list_x, klasse_x, class_list_y, klasse_y, class_list_z, klasse_z = classify(diff_x, diff_y, diff_z)

    klasse_x.append(1)
    klasse_x.append(1)
    klasse_y.append(1)
    klasse_y.append(1)
    klasse_z.append(1)
    klasse_z.append(1)

    print(len(time_list))
    print(len(x_list))
    print(len(y_list))
    print(len(z_list))
    print(len(klasse_x))
    plot(x_list, y_list, z_list, time_list, klasse_x, klasse_y, klasse_z)
