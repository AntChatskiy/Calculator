try:
    import operator
    import math
    import copy
    import unittest
    import numpy as np
    import matplotlib.pyplot as plt
    from tkinter import *
    from tkinter import ttk

except ImportError:
    print("One of the folowwing libraries isn't installed: \n",
          "operator, math, copy, unittest, numpy, matplotlib, tkinter")

try:
    import calculator_unittest

except ImportError:
    print("'calculator_unittest.py' is missing")


class Parser(object):
    def __init__(self):
        """
        Parser, universal way to parse yout string or massive
        """

        self.specialActions = {"!": math.factorial}  # TODO

        self.digits = [str(digit) for digit in range(10)]
        self.operators = ["(", ")", "+", "-", "*", "/", "^", "="]
        self.special = [elem for elem in self.specialActions] + ["x", "y"]
        self.permissible = self.operators + self.special + self.digits + ["."]

    def main_parse(self):
        pass

    def separation(self, expression):
        """
        Smart split function
        :param expression: 
        :return: list with expression operators and operands 
        """
        if type(expression) == list:
            return expression

        else:
            # Checking for errors
            for sign in expression:
                if sign not in self.permissible:
                    return "UnknownSignError"

            output = []
            for sign in expression:
                # If sign is math operator
                if sign in self.operators:
                    output.append(sign)

                # If output doesn't exist and if there isn't a mistake in input
                elif not output:
                    output.append(sign)

                # if sign is special sign
                elif sign in self.special:
                    # and last output elem doesn't have a special sign at the end
                    for elem in self.special:
                        if elem in output[-1]:
                            break

                    else:
                        output.append(sign)

                # If sign is digit and last sign is digit; or sign is "."
                elif output[-1].isdigit() or "." in output[-1]:
                    output[-1] += sign

                # If sign is digit and last sign isn't digit or dot
                elif sign.isdigit() and "." not in output[-1]:
                    output.append(sign)

            return output

    def special_parse(self, expression):
        pass

    @staticmethod
    def type(expression):
        """
        Gets expression. Return expression type: error, graphic, point or expression
        :return: type
        """
        if type(expression) == str:
            if "Error" in expression:
                return "error"

            elif "y=" in expression:
                if expression[0] == "y":
                    return "graphic"

                else:
                    return "InputError"

            elif "x=" in expression:
                if expression[0] == "x":
                    return "point"

                else:
                    return "InputError"

            else:
                return "expression"

        else:
            return "InputError"


class Plot(object):
    def __init__(self):
        """
        Plot class based on matplotlib
        """
        pass

    @staticmethod
    def calculate_x(step):
        """
        :return: x - list
        """
        maximum = step * 2000
        minimum = step * -2000
        x = [i/10 for i in range(minimum, maximum)]
        return x

    @staticmethod
    def create_graphic(y, x=np.arange(150, -150, 0.1)):
        """
        Create graphic based on input x and y
        :return: None
        """
        plt.plot(x, y)
        plt.xlabel(r'$x$')  # Метка по оси x в формате TeX
        plt.ylabel(r'$f(x)$')  # Метка по оси y в формате TeX
        plt.title("Graphic")  # Заголовок в формате TeX
        plt.grid(True)  # Сетка
        plt.show()  # Показать график


class Calculator(object):
    def __init__(self):
        """
        Calculator: do operations and return the result
        """
        self.digits = [str(digit) for digit in range(10)]

        self.priority = {'+': 1, '-': 1, '*': 2, '/': 2, "^": 3}

        self.operators = {"(": None, ")": None, '+': operator.add, '-': operator.sub,
                          '*': operator.mul, '/': operator.truediv, "^": operator.pow}

        self.special = [".", "!"]
        self.special = [elem for elem in self.operators] + self.special

        self.parser = Parser()

        self.plot = Plot()
        self.step = 1

    def main(self, expression):
        """
        :param expression: 
        :return: resilt of expression 
        """
        exprType = self.parser.type(expression)

        # Checking for errors
        if exprType == "error":
            return expression

        if exprType == "InputError":
            return "InputError"

        # Checking for graphics
        elif exprType == "graphic":
            # Delete "y=" in expression
            expression = expression[2:]

            expression = self.parser.separation(expression)

            expression = self.infix_to_postfix(expression)

            self.graphic_calculation(expression)

            return " "

        elif exprType == "point":
            pass

        elif exprType == "expression":
            # Turn expression without spaces into list, which divide expression into operands and operators
            expression = self.parser.separation(expression)

            if "Error" in expression:
                return expression

            # Turn expression into Reverse Polish Notation
            expression = self.infix_to_postfix(expression)

            # Calculate
            expression = self.calculation(expression)

        return expression

    def calculation(self, expression):
        """
        :param expression: 
        :return: resilt of expression 
        """
        stack = [0]
        for sign in expression:
            if sign in self.operators:
                op2, op1 = stack.pop(), stack.pop()

                try:
                    stack.append(self.operators[sign](op1, op2))

                except ZeroDivisionError:
                    return "ZeroDivisionError"

            elif sign:
                if type(sign) == int or type(sign) == float:
                    stack.append(sign)

                # If string is floating-point number, turn it into class float
                elif "." in sign:
                    stack.append(float(sign))

                # If string is integer, turn it into class int
                elif sign.isdigit():
                    stack.append(int(sign))

        result = stack.pop()

        if type(result) == float and result % 1 == 0:
            result = int(result)

        return result

    def graphic_calculation(self, expression):
        # Calculate x
        x = self.plot.calculate_x(self.step)
        y = copy.copy(x)

        # Calculate y
        for i in range(len(y)):
            temp = copy.copy(expression)
            for ii in range(len(temp)):
                if temp[ii] == "x" or type(temp[ii]) == list:
                    temp[ii] = y[i]

            y[i] = self.calculation(temp)

        # Create graphic
        self.plot.create_graphic(y, x)

    def infix_to_postfix(self, expression):
        """
        :param expression: 
        :return: reverse polish notation expression
        """
        stack = []  # Only pop when the coming op has priority
        output = []

        for sign in expression:
            if sign not in self.operators:
                output.append(sign)

            elif sign == '(':
                stack.append('(')

            elif sign == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                stack.pop()  # Pop '('

            else:
                while stack and stack[-1] != '(' and self.priority[sign] <= self.priority[stack[-1]]:
                    output.append(stack.pop())
                stack.append(sign)

        # Leftover
        while stack:
            output.append(stack.pop())

        return output

    def do_round(self, expression):
        """
        :param expression: "12+3.623" 
        :return: "12+4"
        """
        expression = self.parser.separation(expression)  # ["12", "+", "3.6"]

        expression.reverse()  # ["3.6", "+", "12"]

        for i in range(len(expression)):
            if "." in expression[i]:  # "3.6"
                expression[i] = float(expression[i])  # "3.6" = 3.6
                expression[i] = round(expression[i])  # 4
                expression[i] = str(expression[i])  # 4 = "4"

                break  # ["4", "+", "12"]

        expression.reverse()  # ["12", "+", "4"]

        result = ""
        for elem in expression:
            result += elem

        return result


class History(Frame):
    def __init__(self, N, memory):
        """
        Special type of frame, created for showing calculator's history to user
        """
        Frame.__init__(self)

        self.storage = memory


        # Label settings
        self.settings = {"font": "times 14", "justify": "center", "state": "disabled"}

        # Font for ttk.buttons
        self.fontStyle = ttk.Style()
        self.fontStyle.configure("TButton", font=("times", "14"))

        # Buttons settings
        self.ttkSettings = {"style": "TButton", "width": 6}

        # Fills up entry list with entries
        for i in range(N):
            self.entryMas.append(Entry(self, **self.settings))
            self.entryMas[i].pack(side=TOP)

    def update_history(self):
        """
        Updates history
        :return: 
        """
        if self.storage:
            storage = copy.copy(self.storage)
            storage.reverse()

            for i in range(len(storage)):
                self.entryMas[i]["state"] = NORMAL

                self.entryMas[i].delete(0, END)
                self.entryMas[i].insert(0, storage[i])

                self.entryMas[i]["state"] = DISABLED

    def create_history_window(self):
        """
        Creates window with calculator's history
        :return: Nothing
        """
        self.history_window = Tk()
        self.history_window.title("History")

        # Exit button
        btn = ttk.Button(self.history_window, text="Exit", **self.ttkSettings, command=self.history_window.destroy)
        btn.pack(side=TOP)

        self.history_window.bind("<KeyPress>", self.destroy_window)

        storage = copy.copy(self.storage)
        storage.reverse()

        for i in range(len(storage)):
            Label(self.history_window, text=(str(i+1) + ". " + storage[i]), **self.settings).pack(side=TOP)

        self.history_window.focus_force()

    def destroy_window(self, key):
        if key.keycode == 27:
            self.history_window.destroy()


class Window(object):
    def __init__(self):
        """
        Calculator's GUI
        """
        # Create calculator object
        self.calculator = Calculator()

        # Create main window
        self.root = Tk()
        self.root.title("Calculator")

        # Let window unchangeable
        self.root.minsize(550, 220)
        self.root.maxsize(550, 220)

        # bind keyboard
        self.root.bind("<KeyPress>", self.key_press)
        self.root.bind("<KeyRelease>", self.key_release)

        # True - button is pressed, False - button is released
        self.key = False

        # Create parent-frame for keyboard and entry frames
        self.mainFrame = Frame(self.root)
        self.mainFrame.pack(side=RIGHT)

        # Create frames for entry and keyboard
        self.calculationFrame = Frame(self.mainFrame)
        self.keyboardFrame = Frame(self.mainFrame)

        # Pack frames
        self.calculationFrame.pack(side=TOP)
        self.keyboardFrame.pack(side=BOTTOM)

        # Menu signs which could be changed without any damage to programme
        self.strMenu = [
            ["M", "M+", "(", ")", "!", "+"],
            ["MC", "H", "9", "8", "7", "-"],
            ["п", "e", "6", "5", "4", "*"],
            ["T", "", "3", "2", "1", "/"],
            ["", "", "0", "00", ".", "^"],
            ["", "", "C", "CE", "=", "≈"]
        ]

        # List with buttons
        self.menu = []

        # Font for ttk.buttons
        self.fontStyle = ttk.Style()
        self.fontStyle.configure("TButton", font=("times", "14"))

        # Buttons settings
        self.settings = {"style": "TButton", "width": 6}

        # List with operations
        self.operations = self.calculator.operators

        # List with operands and signs which program use to prevent errors
        self.errorSigns = [elem for elem in self.operations] + ["."]
        self.special = ["=", "!"]
        self.variables = ["x", "y"]
        self.digits = [str(digit) for digit in range(10)]
        self.permissible = self.errorSigns + self.special + self.digits + self.variables

        # Create and pack entries in top frame
        self.operationEntry = Entry(self.calculationFrame, width=32, font="times 14")
        self.operationEntry.pack()
        self.operationEntry.focus_force()

        # Contains information about calculator's memory
        self.memory = ""

        # Keeps calculator's history
        self.storage = []

        # Class which works with calculator's operations' history
        self.history_len = 8
        self.history = History(self.history_len, self.storage)
        self.history.pack(side=LEFT)

        # Dictionary with special signs
        self.special = {"=": self.math,
                        "CE": lambda : self.operationEntry.delete(len(self.operationEntry.get())-1),
                        "C": lambda :  self.operationEntry.delete(0, END),
                        "п": lambda : self.operationEntry.insert(END, math.pi),
                        "e": lambda : self.operationEntry.insert(END, math.e),
                        "≈": self.do_round,
                        "M": self.memorizing,
                        "MC": self.forgetting,
                        "M+": lambda : self.operationEntry.insert(END, self.memory),
                        "H": self.history.create_history_window,
                        "T": self.calculator_test
                        }

        # Dictionary with key-codes
        self.keycodes = {13: self.math,  # Enter - calculate
                         27: lambda : self.root.destroy(),  # Escape - destroy window
                         67: lambda : self.operationEntry.delete(0, END),  # Clear entry
                         72: self.history.create_history_window  # H - create history window
                         }

        # Parser which is used in some functions
        self.parser = Parser()

    def create_menu(self):
        """
        Creates main menu which contains buttons, entries.
        :return: 
        None
        """

        # Fill list with buttons by the information picked from strMenu
        for i in range(len(self.strMenu)):
            self.menu.append([])
            for ii in range(len(self.strMenu[i])):
                sign = self.strMenu[i][ii]

                if sign in self.special:
                    self.menu[i].append(ttk.Button(self.keyboardFrame, text=sign,
                                                   **self.settings, command=self.special[sign])
                                        )
                    self.menu[i][ii].grid(row=i, column=ii)

                elif sign == "":
                    self.menu[i].append(None)

                # Must be usual sign
                else:
                    self.menu[i].append(ttk.Button(self.keyboardFrame, text=sign, **self.settings,
                                                   command=lambda lambda_sign=sign:
                                                   self.operationEntry.insert(END, lambda_sign))
                                        )
                    self.menu[i][ii].grid(row=i, column=ii)

        # Create action which will update itself
        self.update()
        self.root.mainloop()

    def key_press(self, key):
        """
        Do function bound on pressed key
        :param key: pressed key 
        :return: Nothing
        """
        # Focus on operation entry
        self.operationEntry.focus_force()

        if not self.key:
            if key.keycode in self.keycodes:
                # do function bound on key
                self.keycodes[key.keycode]()
                self.key = True

    def key_release(self, key):
        """
        :param key: released key 
        :return: Nothing 
        """
        if self.key:
            self.key = False

    def math(self):
        """
        do math operation
        :return: nothing
        """

        # Get expression from operation entry
        expression = self.operationEntry.get()
        self.operationEntry.delete(0, END)

        # Add operation to memory
        if len(self.storage) < self.history_len:
            self.storage.append(expression)

        # If memory reached limit, updates it
        else:
            self.storage.pop(0)
            self.storage.append(expression)

        # Update calculator's history
        self.history.update_history()

        # Calculate result of the operation
        result = self.calculator.main(expression)

        # Insert result into operation entry
        self.operationEntry.insert(END, result)

    def do_round(self):
        """
        :input: string expression, for example "12+3.6"
        :return: string expression, with rounded last digit, for example "12+4"
        """
        expression = self.operationEntry.get()  # "12+3.6"

        self.operationEntry.delete(0, END)

        result = self.calculator.do_round(expression)  # "12+4"

        self.operationEntry.insert(0, result)

    def memorizing(self):
        self.memory = self.operationEntry.get()

    def forgetting(self):
        self.memory = ""

    def update(self):
        """
        Update the window to prevent user's mistakes.
        
        This part is sometimes unreadable. But if you look on buttons calculator is disabling 
        depends on last sign, you'll see connection between code and calculator's work.  
        
        :return: 
        None
        """
        operation = self.operationEntry.get()

        for mas in self.menu:
            for button in mas:
                if button:
                    button["state"] = NORMAL

        # If user did anything
        if operation:
            last = operation[-1]

            # Disable buttons
            # If there's an operation sign in the operation entry:
            if last in self.errorSigns:
                # Check every button - does it contain an operation sign
                for mas in self.menu:
                    for button in mas:
                        if button:
                            # If button text and error sign are the same
                            if button["text"] in self.errorSigns:
                                if last == ".":
                                    button["state"] = DISABLED

                                elif last == "(" or last == ")":
                                    if button["text"] not in self.operations:
                                        button["state"] = DISABLED

                                else:
                                    if button["text"] != "(" and button["text"] != ")":
                                        button["state"] = DISABLED

            # If user did mistake when printed by PC keyboard it delete the mistake
            if last not in self.permissible and "Error" not in operation:
                operation = operation[:-1]
                self.operationEntry.delete(0, END)
                self.operationEntry.insert(0, operation)

            elif last in self.special or last in self.variables:
                if last in operation[:-1]:
                    operation = operation[:-1]
                    self.operationEntry.delete(0, END)
                    self.operationEntry.insert(0, operation)

        # Update itself
        self.root.after(50, self.update)

    @staticmethod
    def calculator_test():
        """
        Test calculator. All test are kept in file calculator_unittest.py
        :return: nothing
        """
        suite = unittest.TestLoader().loadTestsFromModule(calculator_unittest)
        unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
    calc = Window()
    calc.create_menu()