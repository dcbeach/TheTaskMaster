from tkinter import *
import random
import tkinter as tk
from tkinter import font as tkfont
import sqlite3


def initialize_variables():
    global width, height, user_name, tasks, priority_colors, task_label

    priority_colors = {1: 'beige', 2 : 'pink', 3 : 'orange', 4 : 'blue', 5 : 'red'}
    tasks = (('Do Dishes', 3, 1), ('Clean Office', 2, 2), ('Do Homework', 4, 5), ('Write Blog', 5, 4))

    user_name = "Doug"
    width, height = 500, 550


class TaskMasterApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        #For F in (UserView):
        page_name = UserView.__name__
        frame = UserView(parent=container, controller=self)
        self.frames[page_name] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("UserView")

    def show_frame(self, page_name):
        for frame in self.frames.values():
            frame.grid_remove()
            for widget in frame.winfo_children():
                widget.destroy()

        if page_name == 'UserView':
            self.frames[page_name].update_user_display()
        elif page_name == 'HighScore':
            self.frames[page_name].display_highscores()
        elif page_name == 'StartPage':
            self.frames[page_name].display_startpage()

        frame = self.frames[page_name]
        frame.grid()
        frame.winfo_toplevel().geometry("500x550+200+200")


class UserView(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

    def update_user_display(self):
        label = tk.Label(self, text="Welcome " + user_name, font=self.controller.title_font)
        label.place(relx=.1, rely=.05, width=.8 * width)


        global task_frame, task_label, inprogress
        task_frame = []
        task_label = []
        complete_button = []
        inprogress_button = []
        inprogress = []

        for i in range(len(tasks)):
            print(tasks[i][1])
            task_frame.append(Frame(self, width=.6 * width, height=75,
                                    highlightbackground=priority_colors[tasks[i][1]],
                                    highlightthickness=3))
            task_frame[i].place(relx=.20, y=(height * .10) + 50 + (100 * i))
            self.update_idletasks()

            task_label.append(Label(task_frame[i], text=tasks[i][0], anchor=W, font=("Helvetica", 15)))
            task_label[i].place(relx=.01, rely=.10, width=task_frame[i].winfo_width() / 2)

            inprogress_button.append(Button(task_frame[i], text="In Progress", bg='aqua',
                                            command=(lambda x=i: inprogress_clicked(x))))
            complete_button.append(Button(task_frame[i], text="Complete", bg='green'))

            inprogress.append(False)
            inprogress_button[i].place(relx=.15, rely=.6, width=task_frame[i].winfo_width() / 3)
            complete_button[i].place(relx=.55, rely=.6, width=task_frame[i].winfo_width() / 3)

        def inprogress_clicked(x):
            global task_label
            if not inprogress[x]:
                inprogress[x] = True
                task_frame[x].config(background='aqua')
                task_label[x].config(background='aqua')
            else:
                inprogress[x] = False
                task_frame[x].config(background='SystemButtonFace')
                task_label[x].config(background='SystemButtonFace')

if __name__ == "__main__":
    initialize_variables()
    app = TaskMasterApp()
    app.mainloop()











