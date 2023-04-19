# Project 14 : Controling a robotic arm using VR
# Modification date : 19/01/2023 - Tanguy
# File : Homemade PID API for BraVeD project

class P:
    """Describe the controler parameter"""
    P = 0

    def __init__(self, P):
        """:param
        name : str
        P : float
        I : float
        value : float"""
        self.P = P

    def calcul(self, cmd, value, dt):
        """:param
        cmd : float
        value : float
        dt : float
        :return
        outp : float"""
        e = cmd-value
        outp = self.P*e
        return outp

    def display(self):
        """Display caracteristic from the PID"""
        print("\nPID caracteristics are ", end='')
        print(f"P : {self.P}")

    def parameters(self):
        """Return list of the parameters"""
        return [self.P]

    def update(self, P=None, I=None):
        """Update PID parameters"""
        if P != None:
            self.P = P

class PI:
    """Describe the controler parameter"""
    P = 0
    I = 0
    I_value = 0

    def __init__(self, P, I, value):
        """:param
        name : str
        P : float
        I : float
        value : float"""
        self.P = P
        self.I = I
        self.I_value = value

    def calcul(self, cmd, value, dt):
        """:param
        cmd : float
        value : float
        dt : float
        :return
        outp : float"""
        e = cmd-value
        I = self.I_value + self.I*e*dt
        outp = self.P*e + I
        self.I_value = I
        return outp

    def display(self):
        """Display caracteristic from the PID"""
        print("\nPID caracteristics are ", end='')
        print(f"P : {self.P}, I : {self.I}")

    def parameters(self):
        """Return list of the parameters"""
        return [self.P, self.I]

    def update(self, P=None, I=None):
        """Update PID parameters"""
        if P != None:
            self.P = P
        if I != None:
            self.I = I

    def reset(self):
        """Reset the saved value from integral and previous value"""
        self.I_value = 0

class PID:
    """Describe the controler parameter"""
    P = 0
    I = 0
    D = 0
    D_value = 0
    I_value = 0

    def __init__(self, P, I, D, value):
        """:param
        name : str
        P : float
        I : float
        D : float
        value : list"""
        self.P = P
        self.I = I
        self.D = D
        self.D_value = value[0]
        self.I_value = value[1]

    def calcul(self, cmd, value, dt):
        """:param
        cmd : float
        value : float
        dt : float
        :return
        outp : float"""
        e = cmd-value
        I = self.I_value + e*dt
        D = (e-self.D_value)/dt
        outp = self.P*e + I*self.I + self.D*D
        self.I_value = I
        self.D_value = e
        return outp

    def display(self):
        """Display caracteristic from the PID"""
        print("\nPID caracteristics are ", end='')
        print(f"P : {self.P}, I : {self.I}, D : {self.D}")

    def parameters(self):
        """Return list of the parameters"""
        return [self.P, self.I, self.D]

    def update(self, P=None, I=None, D=None):
        """Update PID parameters"""
        if P != None:
            self.P = P
        if I != None:
            self.I = I
        if D != None:
            self.D = D

    def reset(self):
        """Reset the saved value from integral and previous value"""
        self.I_value = 0
        self.D_value = 0