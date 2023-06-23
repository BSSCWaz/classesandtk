# This code has been adapted from https://coderslegacy.com/python/switching-between-tkinter-frames-with-tkraise/
# The code demonstrates how to have multiple frames within a single window.
# It has some complexity as it utilises classes and instances of these classes to create the window and frame.
# Warren Sutton adjusted this code on 23 Jun 2023
#
import tkinter as tk

class FirstWindow(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        # The following line was added to demonstrate how a property of the instance of this frame
        # could have it's background ("bg") changed.
        self["bg"] = "blue"
        # The following two lines create two StringVars in each instance of this frame
        self.test_entry_sv = tk.StringVar()
        self.test_label_sv = tk.StringVar()
        tk.Label(self, text="This is Window 1").pack(padx=10, pady=10)
        # The test_label_sv StringVar is attached to the Label, so that the displayed content of
        # the label can be dynamically updated. Note: the 'self' keyword was used in the creation
        # of the StringVar above and used in the subsequent usage here.
        tk.Label(self, textvariable=self.test_label_sv).pack(padx=10, pady=10)
        # The following line was experimental and has been commented out. The line of code
        # demonstrates that the value of the StringVar
        # can be updated in code. However, doing so within the __init__ method is unlikely to be
        # required, as updating the value is most likely to be needed to be done via the result
        # of a process/code elsewhere. Updating the StringVar value elsewhere in the code can
        # be done via either calling a function in this class and/or accessing the property of
        # the class/instance from elsewhere within your code.
        #
        # self.test_label_sv.set("Test")
        tk.Entry(self, textvariable=self.test_entry_sv).pack(padx=10, pady=10)
        # A lambda function has been included in this command, primarily because I wanted to pass
        # a value to the function which gets called when this button is called. You may recall
        # that when we are not using tkinter by defining classes we would normally not need to
        # pass a value in parameters '()' when we add a command function to a button. This is
        # because we can normally easily access the StringVar value which has the value a calling
        # function requires. And this is because we normally make the StringVars as global values.
        # Once we start using classes and instances accessing the StringVars is not so straightforward
        # and so it's likely better to pass the value to the function as a parameter. Using a lambda
        # function is one way to achieve this.
        #
        tk.Button(self, text="Click Me", command=lambda: addToMyList(self.test_entry_sv.get())).pack(padx=10, pady=10)
        self.pack(padx=10, pady=10)

    # The following method (function) is one way that the StringVar value could be updated.
    # This method can be called from elsewhere in the code and passed the new_value to go
    # into the StringVar.
    def update_the_label(self, new_value):
        self.test_label_sv.set(new_value)


class SecondWindow(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        tk.Label(self, text="This is Window 2").pack(padx=10, pady=10)
        self.pack(padx=10, pady=10)


class MainWindow():
    def __init__(self, master):
        mainframe = tk.Frame(master)
        mainframe.config(background='yellow')
        mainframe.pack(padx=10, pady=10, fill='both', expand=1)
        self.windowNum = 0
        self.framelist = []
        self.framelist.append(FirstWindow(mainframe))
        self.framelist.append(SecondWindow(mainframe))
        self.framelist[1].forget()
        bottomframe = tk.Frame(master)
        bottomframe.config(background="red")
        bottomframe.pack(padx=10, pady=10)

        switch = tk.Button(bottomframe, text="Switch", command=self.switchWindows)
        switch.pack(padx=10, pady=10)

        bottomframe2 = tk.Frame(master)
        bottomframe2.config(background="blue")
        bottomframe2.pack(padx=10, pady=10)


    def switchWindows(self):
        self.framelist[self.windowNum].forget()
        self.windowNum = (self.windowNum + 1) % len(self.framelist)
        self.framelist[self.windowNum].tkraise()
        self.framelist[self.windowNum].pack(padx=10, pady=10)

    def test_get_to_label(self, new_label):
        # Either of the following two lines of code could be used to update the StringVar, within the
        # frame (framelist[0]), within the window. The first line of code updates the property of the
        # StringVar directly, whereas the second line of code calls a method(function) of the
        # frame (frameList) to update the StringVar method.
        #
        # self.framelist[0].test_label_sv.set(new_label)
        self.framelist[0].update_the_label(new_label)

# The following adds a module (global) level data structure which can be accessed by functions
# throughout your code.
myList = []

# The following function can be called as the result of a click event on a button within the instance
# of a tk frame. Together with the lambda function within the frame instance (object) above this code
# is not only called as the result of a click event, but is also passed a value from an Entry widget.
# The function also has some test code which prints the adjusted list and some other code that is used
# to demonstrate how a Label value can be updated in the frame. There are different ways this might be
# achieved. One of the ways to update the Label value has been commented out.
def addToMyList(value_to_add):
    myList.append(value_to_add)
    print(myList)
    # Either of the following two ways could be used to update a label value in a frame.
    #
    # window.framelist[0].test_label_sv.set("test2")
    window.test_get_to_label("Hello World!!")


root = tk.Tk()
window = MainWindow(root)
root.mainloop()