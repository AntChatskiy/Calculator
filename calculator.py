"""
This is GUI interface of calculator
"""
from tkinter import *


class CalculatorApp():
    """
    Calculator class
    """
    def __init__(self):
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
        operations = []
        numbers = [""]
        problem = self.operationEntry.get()

        number = 0

        # clean entry with operations
        self.operationEntry.delete(0, END)

        for i in range(len(problem)):
            if problem[i] in self.operations:
                operations.append(problem[i])

                # look for the next number
                number += 1
                numbers.append("")

            # check: is elem number or dot - 'cause user could do a mistake when did operations by keyboard
            elif problem[i].isdigit() or problem[i] == ".":
                # append digit or dot to number's string
                numbers[number] = numbers[number]+problem[i]

        # do numbers integers
        numbers = [int(elem) for elem in numbers]  # TODO: operations with float also

        for i in range(len(numbers)-1):
            if operations[0] == "+":
                operations.pop(0)  # delete operation that we are doing now from list
                numbers[0] = numbers[0] + numbers[1]  # do operation
                numbers.pop(1)

            elif operations[0] == "-":
                operations.pop(0)  # delete operation that we are doing now from list
                numbers[0] = numbers[0] - numbers[1]  # do operation
                numbers.pop(1)

            elif operations[0] == "*":
                operations.pop(0)  # delete operation that we are doing now from list
                numbers[0] = numbers[0] * numbers[1]  # do operation
                numbers.pop(1)

            elif operations[0] == "/":
                operations.pop(0)  # delete operation that we are doing now from list
                numbers[0] = numbers[0] // numbers[1]  # do operation
                numbers.pop(1)

            elif operations[0] == "^":
                operations.pop(0)  # delete operation that we are doing now from list
                numbers[0] = numbers[0] ** numbers[1]  # do operation
                numbers.pop(1)

        dozen = False

        # if number has zeros in end, but it's smaller than 10k
        if numbers[0]/100000%1 == 0:
            dozen = -1  # e-<<dozen>>. Example: 1000000 mean 1e-6. -1 because of specific of while loop

            while numbers[0]%1 == 0:
                numbers[0] = numbers[0]/10
                dozen += 1

            numbers[0] = int(numbers[0]*10)  # while loop did number float - we fix it

        self.operationEntry.insert(0, numbers[0])

        if dozen:
            self.operationEntry.insert(END, "e-{}".format(dozen))

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


cal = CalculatorApp()
cal.create_menu()
