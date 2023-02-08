from pyniryo import *
from IA_module import *

robot = NiryoRobot("169.254.200.200")

precision = 4

def sigmoid(val):
    return 1 / (1 + np.exp(-val))

def sigmoid_prime(val):
    return val * (1 - val)

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

NN = Neural_Network_1("Reverse kinematics", 6, 10, 6, sigmoid, sigmoid_prime, evaluate=evaluate)

NN.load()

"""file = open("Angle.csv", "a")
i = 0
for p1 in range(4, 29, precision):
    i+=1
    print(f"N°{i}")
    for p2 in range(-18, 5, precision):
        for p3 in range(-12, 14, precision):
            for p4 in range(-18, 18, precision):
                for p5 in range(-18, 9, precision):
                    calculatedPos = robot.forward_kinematics(p1,p2,p3,p4,p5,0.0)
                    text = f"{p1/10},{p2/10},{p3/10},{p4/10},{p5/10},{0.0},{calculatedPos.x},{calculatedPos.y},{calculatedPos.z},{calculatedPos.roll},{calculatedPos.pitch},{calculatedPos.yaw}\n"
                    file.write(text)
file.close()"""

file = open("Angle.csv", "r")
datas = list()
for line in file.readlines():
    array = list()
    for element in line.split(","):
        try:
            array.append(float(element))
        except:
            pass
    datas.append(array)
file.close()

datas_x = datas[:][6:]
datas_y = datas[0][0:6]

x_entry = np.array((datas_x), dtype=float)
y_ouput = np.array((datas_y), dtype=float)

print(x_entry)
print(y_ouput)

NN.config(x_entry, y_ouput)

robot.close_connection()