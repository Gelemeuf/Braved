from IA_module import *

def max_list(x):
    max = x[0]
    for e in x:
        if e > max:
            max = e
    return max

def sigmoid(val):
    return 1 / (1 + np.exp(-val))

def sigmoid_prime(val):
    return val * (1 - val)

def arctan(x):
    return np.arctan(x)

def arctan_prime(x):
    return 1/(1+(abs(x)**2))

def evaluate(X, Y):
    result = NN.forward(X).tolist()
    expected = Y.tolist()
    error = 0
    if (len(result) == len(expected)) and (len(result[0]) == len(expected[0])):
        count = 0
        for i in range(len(result)):
            for j in range(len(result[0])):
                error += abs(expected[i][j] - result[i][j])
                count += 1
        error = error / count
    return error

NN = Neural_Network_1("Reverse_kinematics1", 6, 45, 6, arctan, arctan_prime, evaluate=evaluate)

file = open("Angle.csv", "r")
datas_x = list()
datas_y = list()

for line in file.readlines():
    array1 = list()
    array2 = list()
    i = 0
    for element in line.split(","):
        try:
            if i<6:
                array1.append(float(element))
            else:
                array2.append(float(element))
            i += 1
        except:
            pass
    datas_y.append(array1)
    datas_x.append(array2)
file.close()

x_entry = np.array((datas_x), dtype=float)
y_ouput = np.array((datas_y), dtype=float)

x_max_value = max_list([x_entry.max(), abs(x_entry.min())])
y_max_value = max_list([y_ouput.max(), abs(y_ouput.min())])

x_entry = (x_entry)/(x_max_value)
y_ouput = (y_ouput)/(y_max_value)

NN.config(x_entry, y_ouput)