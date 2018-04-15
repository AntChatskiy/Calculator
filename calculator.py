import operator
from tkinter import *


class Calculator():
    def __init__(self):
        self.priority = {'+': 1, '-': 1, '*': 2, '/': 2}
        self.operators = {"(": None, ")": None, '+': operator.add, '-': operator.sub,
                     '*': operator.mul, '/': operator.truediv, "^": operator.pow}

    def calculation(self, expression):
        """
        :param expression: 
        :return: resilt of expression 
        """
        # turn expression without spaces into list, which divide expression into operands and operators
        expression = self.turn(expression)
        # turn expression into Reverse Polish Notation
        expression = self.infix_to_postfix(expression)

        stack = [0]
        for sign in expression:
            if sign in self.operators:
                op2, op1 = stack.pop(), stack.pop()
                stack.append(self.operators[sign](op1, op2))
            elif sign:
                stack.append(float(sign))

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

    def turn(self, expression):
        """
        :param expression: 
        :return: list with expression operators and operands 
        """
        output = []
        for sign in expression:
            if sign in self.operators:
                output.append(sign)

            # if output doesn't exist
            elif not output:
                output.append(sign)

            # if sign is operand and last sign isn't an operand
            elif sign not in self.operators and not output[-1].isdigit() and "." not in output[-1]:
                output.append(sign)

            # if sign is operand and last sign is operand
            elif sign not in self.operators and output[-1].isdigit() or "." in output[-1]:
                output[-1] += sign

        return output

    def reversePolishNotation(self, problem):
        stack = ["+"]
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


class Window():
    def __init__(self):
        # create calculator object
        self.calculator = Calculator()

        # create window
        self.root = Tk()
        self.root.title("Calculator")

        # create frames for entry and keyboard
        self.calculationFrame = Frame(master=self.root)
        self.numbersFrame = Frame(master=self.root)

        # pack frames
        self.calculationFrame.pack(side=TOP)
        self.numbersFrame.pack(side=BOTTOM)

        # menu signs which could be changed without any damage to programme
        self.strMenu = [
            ["9", "8", "7", "+"],
            ["6", "5", "4", "-"],
            ["3", "2", "1", "*"],
            ["0", "00", ".", "/"],
            ["CE", "C", "=", "^"],

        ]

        # list with buttons
        self.menu = []

        # list with operands
        self.operations = ["+", "-", "*", "/", "^", "="]

        #  create and pack entries in top frame
        self.operationEntry = Entry(self.calculationFrame, width=16, font="times 14")
        self.operationEntry.pack(side=LEFT)
        self.resultEntry = Entry(self.calculationFrame, width=14, state=DISABLED, font="times 14")
        self.resultEntry.pack(side=RIGHT)

        # contains information about calculator's memory - is it empty or not
        self.memoryFlag = False

    def create_menu(self):
        """
        Creates main menu which contains buttons, entries.
        :return: 
        None
        """

        #  fill list with buttons by the information picked from strMenu
        for i in range(len(self.strMenu)):
            self.menu.append([])
            for ii in range(len(self.strMenu[i])):
                sign = self.strMenu[i][ii]

                if sign == "=":
                    self.menu[i].append(Button(self.numbersFrame, text=sign, font="times 14", width=6,
                                               command=self.math))
                    self.menu[i][ii].grid(row=i, column=ii)

                elif sign == "CE":
                    self.menu[i].append(Button(self.numbersFrame, text=sign, font="times 14", width=6,
                                               command=lambda:
                                               self.operationEntry.delete(len(self.operationEntry.get())-1)))
                    self.menu[i][ii].grid(row=i, column=ii)

                elif sign == "C":
                    self.menu[i].append(Button(self.numbersFrame, text=sign, font="times 14", width=6,
                                               command=lambda: self.operationEntry.delete(0, END)))
                    self.menu[i][ii].grid(row=i, column=ii)

                else:
                    self.menu[i].append(Button(self.numbersFrame, text=sign, font="times 14", width=6,
                                               command=lambda lambda_sign=sign:
                                               self.operationEntry.insert(END, lambda_sign)))
                    self.menu[i][ii].grid(row=i, column=ii)

        # create action which will update itself
        self.update()
        self.root.mainloop()

    def math(self):
        expression = self.operationEntry.get()
        self.operationEntry.delete(0, END)
        self.operationEntry.insert(END, self.calculator.calculation(expression))

    def update(self):
        """
        Update the window

        1)Doesn't give user a chance to write two operation signs in one line

        :return: 
        None
        """
        operation = self.operationEntry.get()
        flag = False  # True - user did operation; False - user didn't do any operations

        # if user did anything
        if operation:
            last = operation[-1]

            # disable buttons
            for Sign in self.operations:
                # if there's an operation sign in the operation entry
                if last == Sign:
                    flag = True
                    # check every button - does it contain an operation sign
                    for mas in self.menu:
                        for button in mas:
                            # if button text and operation sign are the same...
                            for sign in self.operations:
                                if button["text"] == sign:
                                    button["state"] = DISABLED
                                    # ...you shouldn't continue to compare them
                                    break
                    flag = True
                    break

                else:
                    flag = False

        # if user did operation a long time ago
        if flag == False:
            #  enable buttons which were disabled
            for mas in self.menu:
                for button in mas:
                    button["state"] = "normal"

        self.root.after(80, self.update)


calc = Window()
calc.create_menu()
