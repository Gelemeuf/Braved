import numpy as np
import sys

class Neural_Network_1(object):

    def __init__(self, name, inputs, hiddens, outputs, activation_function, activation_function_prime, evaluate):
        """Initiate the neural network

        :Param
        name : str
        inputs, hiddens1, outputs : int
        activation_function : function
        activation_function_prime : function
        """

        self.name = name

        self.inputSize = inputs
        self.outputSize = outputs
        self.hiddenSize = hiddens
        self.function = activation_function
        self.function_prime = activation_function_prime
        self.evaluate = evaluate

        self.W1 = np.random.randn(self.inputSize, self.hiddenSize)
        self.W2 = np.random.randn(self.hiddenSize, self.outputSize)


    def forward(self, X):
        """Use one input to determine the output using the network
        
        :Param
        X : numpy array"""

        self.z1 = np.dot(X, self.W1)
        self.z2 = self.function(self.z1)
        self.z3 = np.dot(self.z2, self.W2)
        output = self.function(self.z3)
        return output


    def backward(self, X, Y, O):
        """Change the strengh from link between neurons
        
        :Param
        X : numpy array
        Y : numpy array
        O : numpy array"""

        # Determine error from the output
        self.o_error = Y - O
        self.o_delta = self.o_error * self.function_prime(O)

        # Determine error from the hidden neurons
        self.z2_error = self.o_delta.dot(self.W2.T)
        self.z2_delta = self.z2_error * self.function_prime(self.z2)

        self.W1 += X.T.dot(self.z2_delta)
        self.W2 += self.z2.T.dot(self.o_delta)


    def save(self):

        file1 = open(self.name + "_W1.csv", "w")
        for element in self.W1:
            for subelement in element:
                file1.write(str(subelement) + ",")
            file1.write("\n")
        file1.close()

        file2 = open(self.name + "_W2.csv", "w")
        for element in self.W2:
            for subelement in element:
                file2.write(str(subelement) + ",")
            file2.write("\n")
        file2.close()

    def load(self):
        """Load neural network matrix"""

        try:
            W1array = list() # Create the array
            file1 = open(self.name + "_W1.csv", "r")
            for line in file1.readlines():
                array = list()
                for element in line.split(","):
                    try:
                        array.append(float(element))
                    except:
                        pass
                W1array.append(array) # Add line to the array
            file1.close()

            W2array = list() # Create the array
            file2 = open(self.name + "_W2.csv", "r")
            for line in file2.readlines():
                array = list()
                for element in line.split(","):
                    try:
                        array.append(float(element))
                    except:
                        pass
                W2array.append(array) # Add line to the array
            file2.close()

            # Transform the arrays to numpy array
            if (len(W1array)==self.inputSize) and (len(W1array[0])==self.hiddenSize) and (len(W2array)==self.hiddenSize) and (len(W2array[0])==self.outputSize):
                self.W1 = np.array((W1array), dtype=float)
                self.W2 = np.array((W2array), dtype=float)
            else:
                sys.exit() # Exit system to keep neural network integrity

        except:
            return
            

    def train(self, X, Y):
        """Train the neural network once

        :Param
        X : numpy array
        Y : numpy array
        """

        o = self.forward(X)
        self.backward(X, Y, o)

    def config(self, X, Y):
        title = f"# Artificial intelligence configuration interface : {self.name} #"
        for s in range(len(title)):
            print("#", end="")
        print("\n"+title)
        for s in range(len(title)):
            print("#", end="")
        print("\n")
        user = input("Choose order : ")
        while user != "quit":
            if user == "train":
                nb = int(input("How many time do you want to train the neural network ? "))
                print("-> Training started, please wait")
                for i in range(nb):
                    self.train(X, Y)
                print("-> Training finished !")
            elif user == 'evaluate':
                print("-> Evaluation : ", end="")
                print(self.evaluate(X, Y))
            elif user == 'load':
                self.load()
                print("-> Neural network loaded")
            elif user == 'save':
                self.save()
                print("-> Neural network saved")
            elif user == "display":
                print("\nW1 :")
                print(self.W1)
                print("\nW2 :")
                print(self.W2)
                print("\nW3 :")
                print(self.W3)
            elif user == "adjust":
                print("-> Auto adjust is processing, please wait")
                self.autoAdjust(X, Y)
                print("-> Auto adjust is over")
            elif user == "recreate":
                print("-> Creation of a random neural network")
                self.recreate()
            user = input("\nChoose order : ")

    def recreate(self):
        self.W1 = np.random.randn(self.inputSize, self.hiddenSize)
        self.W2 = np.random.randn(self.hiddenSize, self.outputSize)

    def autoAdjust(self, X, Y):
        for e in range(100):
            print(f"\t-> Neural network n°{e+1}")
            error_b = self.evaluate(X, Y)
            W1b = self.W1
            W2b = self.W2

            self.recreate()
            error_new = self.evaluate(X, Y)
            if error_new > error_b:
                self.W1 = W1b
                self.W2 = W2b
            else:
                print("\tHas been chosen !")


class Neural_Network_2(object):

    def __init__(self, name, inputs, hiddens1, hiddens2, outputs, activation_function, activation_function_prime, evaluate):
        """Initiate the neural network

        :Param
        name : str
        inputs, hiddens1, outputs : int
        activation_function : function
        activation_function_prime : function
        """

        self.name = name

        self.inputSize = inputs
        self.outputSize = outputs
        self.hiddenSize1 = hiddens1
        self.hiddenSize2 = hiddens2
        self.function = activation_function
        self.function_prime = activation_function_prime
        self.evaluate = evaluate

        self.W1 = np.random.randn(self.inputSize, self.hiddenSize1)
        self.W2 = np.random.randn(self.hiddenSize1, self.hiddenSize2)
        self.W3 = np.random.randn(self.hiddenSize2, self.outputSize)


    def forward(self, X):
        """Use one input to determine the output using the network
        
        :Param
        X : numpy array"""

        self.z1 = np.dot(X, self.W1)
        self.z2 = self.function(self.z1)
        self.z3 = np.dot(self.z2, self.W2)
        self.z4 = self.function(self.z3)
        self.z5 = np.dot(self.z4, self.W3)
        output = self.function(self.z5)
        return output


    def backward(self, X, Y, O):
        """Change the strengh from link between neurons
        
        :Param
        X : numpy array
        Y : numpy array
        O : numpy array"""

        # Determine error from the output
        self.o_error = Y - O
        self.o_delta = self.o_error * self.function_prime(O)

        # Determine error from the hidden neurons
        self.z4_error = self.o_delta.dot(self.W3.T)
        self.z4_delta = self.z4_error * self.function_prime(self.z4)

        self.z2_error = self.z4_delta.dot(self.W2.T)
        self.z2_delta = self.z2_error * self.function_prime(self.z2)

        self.W1 += X.T.dot(self.z2_delta)
        self.W2 += self.z2.T.dot(self.z4_delta)
        self.W3 += self.z4.T.dot(self.o_delta)


    def save(self):

        file1 = open(self.name + "_W1.csv", "w")
        for element in self.W1:
            for subelement in element:
                file1.write(str(subelement) + ",")
            file1.write("\n")
        file1.close()

        file2 = open(self.name + "_W2.csv", "w")
        for element in self.W2:
            for subelement in element:
                file2.write(str(subelement) + ",")
            file2.write("\n")
        file2.close()

        file3 = open(self.name + "_W3.csv", "w")
        for element in self.W3:
            for subelement in element:
                file3.write(str(subelement) + ",")
            file3.write("\n")
        file3.close()


    def load(self):
        """Load neural network matrix"""

        try:

            W1array = list() # Create the array
            file1 = open(self.name + "_W1.csv", "r")
            for line in file1.readlines():
                array = list()
                for element in line.split(","):
                    try:
                        array.append(float(element))
                    except:
                        pass
                W1array.append(array) # Add line to the array
            file1.close()

            W2array = list() # Create the array
            file2 = open(self.name + "_W2.csv", "r")
            for line in file2.readlines():
                array = list()
                for element in line.split(","):
                    try:
                        array.append(float(element))
                    except:
                        pass
                W2array.append(array) # Add line to the array
            file2.close()

            W3array = list() # Create the array
            file3 = open(self.name + "_W3.csv", "r")
            for line in file3.readlines():
                array = list()
                for element in line.split(","):
                    try:
                        array.append(float(element))
                    except:
                        pass
                W3array.append(array) # Add line to the array
            file3.close()

            # Transform the arrays to numpy array
            if (len(W1array)==self.inputSize) and (len(W1array[0])==self.hiddenSize1) and (len(W2array)==self.hiddenSize1) and (len(W2array[0])==self.hiddenSize2) and (len(W3array)==self.hiddenSize2) and (len(W3array[0])==self.outputSize):
                self.W1 = np.array((W1array), dtype=float)
                self.W2 = np.array((W2array), dtype=float)
                self.W3 = np.array((W3array), dtype=float)
            else:
                sys.exit() # Exit system to keep neural network integrity

        except:
            return
            

    def train(self, X, Y):
        """Train the neural network once

        :Param
        X : numpy array
        Y : numpy array
        """

        o = self.forward(X)
        self.backward(X, Y, o)

    def config(self, X, Y):
        title = f"# Artificial intelligence configuration interface : {self.name} #"
        for s in range(len(title)):
            print("#", end="")
        print("\n"+title)
        for s in range(len(title)):
            print("#", end="")
        print("\n")
        user = input("Choose order : ")
        while user != "quit":
            if user == "train":
                nb = int(input("How many time do you want to train the neural network ? "))
                print("-> Training started, please wait")
                for i in range(nb):
                    self.train(X, Y)
                print("-> Training finished !")
            elif user == 'evaluate':
                print("-> Evaluation : ", end="")
                print(self.evaluate(X, Y))
            elif user == 'load':
                self.load()
                print("-> Neural network loaded")
            elif user == 'save':
                self.save()
                print("-> Neural network saved")
            elif user == "display":
                print("\nW1 :")
                print(self.W1)
                print("\nW2 :")
                print(self.W2)
                print("\nW3 :")
                print(self.W3)
            elif user == "adjust":
                print("-> Auto adjust is processing, please wait")
                self.autoAdjust(X, Y)
                print("-> Auto adjust is over")
            elif user == "recreate":
                print("-> Creation of a random neural network")
                self.recreate()
            user = input("\nChoose order : ")

    def recreate(self):
        self.W1 = np.random.randn(self.inputSize, self.hiddenSize1)
        self.W2 = np.random.randn(self.hiddenSize1, self.hiddenSize2)
        self.W3 = np.random.randn(self.hiddenSize2, self.outputSize)

    def autoAdjust(self, X, Y):
        for e in range(100):
            print(f"\t-> Neural network n°{e+1}")
            error_b = self.evaluate(X, Y)
            W1b = self.W1
            W2b = self.W2
            W3b = self.W3

            self.recreate()
            error_new = self.evaluate(X, Y)
            if error_new > error_b:
                self.W1 = W1b
                self.W2 = W2b
                self.W3 = W3b
            else:
                print("\tHas been chosen !")
