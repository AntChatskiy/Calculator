import operator
import copy
from tkinter import *
from tkinter import ttk


class Calculator(object):
    def __init__(self):
        self.priority = {'+': 1, '-': 1, '*': 2, '/': 2, "^": 3}
        self.operators = {"(": None, ")": None, '+': operator.add, '-': operator.sub,
                     '*': operator.mul, '/': operator.truediv, "^": operator.pow}

    def calculation(self, expression):
        """
        :param expression: 
        :return: resilt of expression 
        """
        # turn expression without spaces into list, which divide expression into operands and operators
        expression = self.parse(expression)

        # checking for errors
        if expression == "UnknownSignError":
            return expression

        # turn expression into Reverse Polish Notation
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
                # if string is floating point number, turn it into class float
                if "." in sign:
                    stack.append(float(sign))

                # if string is integer, turn it into class int
                else:
                    stack.append(int(sign))

        return stack.pop()

    def infix_to_postfix(self, expression):
        """
        :param expression: 
        :return: reverse polish notation expression
        """
        stack = []  # only pop when the coming op has priority
        output = []

        for sign in expression:
            if sign not in self.operators:
                output.append(sign)

            elif sign == '(':
                stack.append('(')

            elif sign == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                stack.pop()  # pop '('

            else:
                while stack and stack[-1] != '(' and self.priority[sign] <= self.priority[stack[-1]]:
                    output.append(stack.pop())
                stack.append(sign)

        # leftover
        while stack:
            output.append(stack.pop())

        return output

    def parse(self, expression):
        """
        :param expression: 
        :return: list with expression operators and operands 
        """
        # checking for errors
        for sign in expression:
            if sign not in self.operators and not sign.isdigit() and sign != ".":
                output = "UnknownSignError"
                return output

        output = []
        for sign in expression:
            # if sign is math operator
            if sign in self.operators:
                output.append(sign)

            # if output doesn't exist
            elif not output:
                output.append(sign)

            # if sign is digit and last sign is math operator
            elif sign not in self.operators and not output[-1].isdigit() and "." not in output[-1]:
                output.append(sign)

            # if sign is digit and last sign is digit
            elif sign not in self.operators:
                if output[-1].isdigit() or "." in output[-1]:

                    output[-1] += sign

        return output

    def reversePolishNotation(self, problem):
        stack = [""]
        mas = ""

        for sign in problem:
            if sign.isdigit():
                # if sign is digit - send it to list
                mas += sign

            elif sign in self.operatorsLevel:

                # if operator has bigger priority than the last, send it to list first
                if self.operatorsLevel[stack[-1]] < self.operatorsLevel[sign]:
                    mas += " {} ".format(sign)

                # if operator has smaller priority than the last, send it to stack, and the last to list
                elif self.operatorsLevel[stack[-1]] > self.operatorsLevel[sign]:
                    mas += " {} ".format(stack.pop())
                    stack.append(sign)

                # if operators have the same priority, send last to list, and given to stack
                elif self.operatorsLevel[stack[-1]] == self.operatorsLevel[sign]:
                    mas += " {} ".format(stack.pop())
                    stack.append(sign)

        signs = ""
        for sign in stack:
            signs += " {} ".format(sign)

        mas += signs

        return mas


class Window(object):
    def __init__(self):
        # create calculator object
        self.calculator = Calculator()

        # create main window
        self.root = Tk()
        self.root.title("Calculator")

        # let window unchangeable
        self.root.minsize(300, 220)
        self.root.maxsize(300, 220)

        # create frames for entry and keyboard
        self.calculationFrame = Frame(master=self.root)
        self.numbersFrame = Frame(master=self.root)

        # pack frames
        self.calculationFrame.pack(side=TOP)
        self.numbersFrame.pack(side=BOTTOM)

        # menu signs which could be changed without any damage to programme
        self.strMenu = [
            ["(", ")", "M", "M+"],
            ["9", "8", "7", "+"],
            ["6", "5", "4", "-"],
            ["3", "2", "1", "*"],
            ["0", "00", ".", "/"],
            ["C", "CE", "=", "^"]
        ]

        # list with buttons
        self.menu = []

        # font for ttk.buttons
        self.fontStyle = ttk.Style()
        self.fontStyle.configure("TButton", font=("times", "14"))

        # buttons settings
        self.settings = {"style": "TButton", "width": 6}  # "font": "times 14",

        # list with operations
        self.operations = self.calculator.operators

        # list with operands and signs which program use to prevent errors
        self.errorSigns = copy.copy(self.operations)
        self.errorSigns.update({".": None})

        #  create and pack entries in top frame
        self.operationEntry = Entry(self.calculationFrame, width=32, font="times 14")
        self.operationEntry.pack()

        # contains information about calculator's memory
        self.memory = ""

    def create_menu(self):
        """
        Creates main menu which contains buttons, entries.
        :return: 
        None
        """

        # fill list with buttons by the information picked from strMenu
        for i in range(len(self.strMenu)):
            self.menu.append([])
            for ii in range(len(self.strMenu[i])):
                sign = self.strMenu[i][ii]

                if sign == "=":
                    self.menu[i].append(ttk.Button(self.numbersFrame, text=sign, **self.settings, command=self.math))
                    self.menu[i][ii].grid(row=i, column=ii)

                elif sign == "CE":
                    self.menu[i].append(ttk.Button(self.numbersFrame, text=sign, **self.settings,
                                               command=lambda:
                                               self.operationEntry.delete(len(self.operationEntry.get())-1))
                                        )
                    self.menu[i][ii].grid(row=i, column=ii)

                elif sign == "C":
                    self.menu[i].append(ttk.Button(self.numbersFrame, text=sign, **self.settings,
                                               command=lambda: self.operationEntry.delete(0, END))
                                        )
                    self.menu[i][ii].grid(row=i, column=ii)

                elif sign == "M":
                    self.menu[i].append(ttk.Button(self.numbersFrame, text=sign, **self.settings,
                                                   command=self.memorizing)
                                        )
                    self.menu[i][ii].grid(row=i, column=ii)

                elif sign == "M+":
                    self.menu[i].append(ttk.Button(self.numbersFrame, text=sign, **self.settings,
                                                   command=self.push_memory)
                                        )
                    self.menu[i][ii].grid(row=i, column=ii)

                # must be usual sign
                else:
                    self.menu[i].append(ttk.Button(self.numbersFrame, text=sign, **self.settings,
                                               command=lambda lambda_sign=sign:
                                               self.operationEntry.insert(END, lambda_sign))
                                        )
                    self.menu[i][ii].grid(row=i, column=ii)

        # create action which will update itself
        self.update()
        self.root.mainloop()

    def math(self):
        # get expression from operation entry
        expression = self.operationEntry.get()
        self.operationEntry.delete(0, END)

        # calculate result of the operation
        result = self.calculator.calculation(expression)

        if isinstance(result, int) or isinstance(result, float):
            # turn integer result from real number into integer
            if result % 1 == 0:
                result = int(result)

        # insert result into operation entry
        self.operationEntry.insert(END, result)

    def memorizing(self):
        self.memory = self.operationEntry.get()

    def push_memory(self):
        self.operationEntry.insert(END, self.memory)
        self.memory = ""

    def update(self):
        """
        Update the window

        Prevent user's mistakes

        :return: 
        None
        """
        operation = self.operationEntry.get()

        for mas in self.menu:
            for button in mas:
                button["state"] = "normal"
        # if user did anything
        if operation:
            last = operation[-1]

            # disable buttons
            # if there's an operation sign in the operation entry:
            if last in self.errorSigns:

                # check every button - does it contain an operation sign
                for mas in self.menu:
                    for button in mas:
                        # if button text and  sign are the same
                            if button["text"] in self.errorSigns:
                                if last == ".":
                                    button["state"] = DISABLED

                                elif last == "(" or last == ")":
                                    if button["text"] not in self.operations:
                                        button["state"] = DISABLED

                                else:
                                    if button["text"] != "(" and button["text"] != ")":
                                        button["state"] = DISABLED

        # update itself
        self.root.after(80, self.update)

# TODO: assert tests

calc = Window()
calc.create_menu()
