import operator
import math
import copy
import unittest
import calculator_unittest
from tkinter import *
from tkinter import ttk


class Parser(object):
    def __init__(self):
        """
        Parser, universal way to parse yout string or massive
        """

        self.specialActions = {"!": math.factorial}  # TODO

        self.digits = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
        self.operators = ["(", ")", "+", "-", "*", "/", "^"]
        self.special = [elem for elem in self.specialActions] + ["."]
        self.permissible = self.operators + self.special + self.digits

    def main_parse(self):
        None

    def separation(self, expression):
        """
        Smart split function
        :param expression: 
        :return: list with expression operators and operands 
        """

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
                if sign not in self.special:
                    # FIXME be careful if you add something to special
                    output.append(sign)

            # if sign is special sign
            elif sign in self.special:
                # and last output elem doesn't have a special sign at the end
                for elem in self.special:
                    if elem in output[-1][-1]:
                        break

                else:
                    output[-1] += sign

            # If sign is digit and last sign is digit
            elif output[-1][-1].isdigit() or "." in output[-1][-1]:
                output[-1] += sign

            # If sign is digit and last sign isn't digit or dot
            elif sign.isdigit() and "." not in output[-1][-1]:
                output.append(sign)

        return output

    def special_parse(self, expression):
        None


class Calculator(object):
    def __init__(self):
        """
        Calculator: do operations and return the result
        """
        self.priority = {'+': 1, '-': 1, '*': 2, '/': 2, "^": 3}

        self.operators = {"(": None, ")": None, '+': operator.add, '-': operator.sub,
                          '*': operator.mul, '/': operator.truediv, "^": operator.pow}

        self.special = [".", "!"]
        self.special = [elem for elem in self.operators] + self.special

        self.parser = Parser()

    def calculation(self, expression):
        """
        :param expression: 
        :return: resilt of expression 
        """
        # Turn expression without spaces into list, which divide expression into operands and operators
        expression = self.parser.separation(expression)

        # Checking for errors
        if expression == "UnknownSignError":
            return expression

        # Turn expression into Reverse Polish Notation
        expression = self.infix_to_postfix(expression)

        stack = [0]
        for sign in expression:
            if sign in self.operators:
                op2, op1 = stack.pop(), stack.pop()

                try:
                    stack.append(self.operators[sign](op1, op2))

                except ZeroDivisionError:
                    return "ZeroDivisionError"

            elif sign:
                # If string is floating point number, turn it into class float
                if "." in sign:
                    stack.append(float(sign))

                # If string is integer, turn it into class int
                else:
                    stack.append(int(sign))

        return stack.pop()

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

    def reverse_polish_notation(self, expression):
        """
        :param expression: expression, which is written in infix way 
        :return: expression, which is written in postfix way
        """

        stack = [""]
        mas = ""

        for sign in expression:
            if sign.isdigit():
                # If sign is digit - send it to list
                mas += sign

            elif sign in self.operatorsLevel:

                # If operator has bigger priority than the last, send it to list first
                if self.operatorsLevel[stack[-1]] < self.operatorsLevel[sign]:
                    mas += " {} ".format(sign)

                # If operator has smaller priority than the last, send it to stack, and the last to list
                elif self.operatorsLevel[stack[-1]] > self.operatorsLevel[sign]:
                    mas += " {} ".format(stack.pop())
                    stack.append(sign)

                # If operators have the same priority, send last to list, and given to stack
                elif self.operatorsLevel[stack[-1]] == self.operatorsLevel[sign]:
                    mas += " {} ".format(stack.pop())
                    stack.append(sign)

        signs = ""
        for sign in stack:
            signs += " {} ".format(sign)

        mas += signs

        return mas

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
        self.entryMas = []

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
        if self.storage:
            storage = copy.copy(self.storage)
            storage.reverse()

            for i in range(len(storage)):
                self.entryMas[i]["state"] = NORMAL

                self.entryMas[i].delete(0, END)
                self.entryMas[i].insert(0, storage[i])

                self.entryMas[i]["state"] = DISABLED

    def history_window(self):

        root = Tk()
        root.title("History")

        ttk.Button(root, text="Exit", **self.ttkSettings, command=root.destroy).pack(side=TOP)

        storage = copy.copy(self.storage)
        storage.reverse()

        for i in range(len(storage)):
            Label(root, text=(str(i+1) + ". " + storage[i]), **self.settings).pack(side=TOP)


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
        self.errorSigns = copy.copy(self.operations)
        self.errorSigns.update({".": None})

        # Create and pack entries in top frame
        self.operationEntry = Entry(self.calculationFrame, width=32, font="times 14")
        self.operationEntry.pack()

        # Contains information about calculator's memory
        self.memory = ""

        # Keeps calculator's history
        self.storage = []

        # Class which works with calculator's operations' history
        self.history = History(8, self.storage)
        self.history.pack(side=LEFT)

        # Dictionary with special signs
        self.special = {"CE": lambda: self.operationEntry.delete(len(self.operationEntry.get())-1),
                        "C": lambda:  self.operationEntry.delete(0, END),
                        "п": lambda: self.operationEntry.insert(END, math.pi),
                        "e": lambda: self.operationEntry.insert(END, math.e),
                        "=": self.math,
                        "≈": self.do_round,
                        "M": self.memorizing,
                        "MC": self.forgetting,
                        "M+": lambda: self.operationEntry.insert(END, self.memory),
                        "H": self.history.history_window,
                        "T": self.calculator_test
                        }

        # parser which is used in some functions
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

    def math(self):
        """
        do math operation
        :return: nothing
        """
        # Get expression from operation entry
        expression = self.operationEntry.get()
        self.operationEntry.delete(0, END)

        # Add operation to memory
        if len(self.storage) < 8:
            self.storage.append(expression)

        # If memory reached limit, updates it
        else:
            self.storage.pop(0)
            self.storage.append(expression)

        # Update calculator's history
        self.history.update_history()

        # Calculate result of the operation
        result = self.calculator.calculation(expression)

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

                            elif last == "(" or last == "." and button["text"] == "=":
                                if button["text"] == "=":
                                    button["state"] = DISABLED

        # Update itself
        self.root.after(80, self.update)

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