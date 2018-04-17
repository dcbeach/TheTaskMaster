from tkinter import *
import random
import tkinter as tk
from tkinter import font as tkfont
import sqlite3


def initialize_variables():
    global width, height, user_name, tasks, priority_colors, task_label

    priority_colors = {1: 'beige', 2: 'pink', 3: 'orange', 4: 'blue', 5: 'red'}

    #tasks = [Task Name, Priority, Difficulty, Due Date]
    tasks = [['Do Dishes', 3, 1, '1/27/18'], ['Clean Office', 2, 2, '2/12/18'], ['Do Homework', 4, 4, '4/12/18'],
             ['Write Blog', 5, 3, '1/12/18'], ['Plan Party', 3, 1, '7/5/18']]

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
        for F in (UserView, LoginView):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.create_highscore_table()
        self.show_frame("LoginView")

    def show_frame(self, page_name):
        for frame in self.frames.values():
            frame.grid_remove()
            for widget in frame.winfo_children():
                widget.destroy()

        if page_name == 'UserView':
            self.frames[page_name].update_user_display()
        elif page_name == 'LoginView':
            self.frames[page_name].load_login_screen()
        elif page_name == 'StartPage':
            self.frames[page_name].display_startpage()

        frame = self.frames[page_name]
        frame.grid()
        frame.winfo_toplevel().geometry("500x550+200+200")

    def create_highscore_table(self):
        conn = sqlite3.connect('TaskMaster.db')
        c = conn.cursor()
        c.execute(
            'CREATE TABLE IF NOT EXISTS logins(name TEXT, password TEXT, access INTEGER)')


class UserView(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

    def update_user_display(self):
        label = tk.Label(self, text="Welcome " + user_name, font=self.controller.title_font)
        label.place(relx=.1, rely=.05, width=.8 * width)


        global task_frame, task_label, inprogress, tasks
        task_frame = []
        task_label = []
        complete_button = []
        inprogress_button = []
        inprogress = []
        task_length = 0

        if len(tasks) >= 4:
            task_length = 4
        else:
            task_length = len(tasks)

        tasks.sort(key=lambda x: x[1])

        for i in range(task_length):
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
            complete_button.append(Button(task_frame[i], text="Complete", bg='green',
                                          command=(lambda x=i: complete_clicked(x))))

            inprogress.append(False)
            inprogress_button[i].place(relx=.15, rely=.6, width=task_frame[i].winfo_width() / 3)
            complete_button[i].place(relx=.55, rely=.6, width=task_frame[i].winfo_width() / 3)

        def complete_clicked(x):
            tasks.pop(x)
            self.controller.show_frame('UserView')

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


class LoginView(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

    def load_login_screen(self):
        login_title = tk.Label(self, text="Please Log In", font=self.controller.title_font)
        login_title.place(relx=.2, rely=.1, width=width*.6)

        user_name_label = tk.Label(self, text="User Name:", font=self.controller.title_font)
        password_label = tk.Label(self, text="Password:", font=self.controller.title_font)
        user_name_text = tk.Entry(self, width=20, font=self.controller.title_font)
        password_text = tk.Entry(self, show='*', width=20, font=self.controller.title_font)
        login_button = tk.Button(self, text="Log In", bg='DeepSkyBlue2', font=self.controller.title_font,
                                 command=lambda: self.check_credentials(user_name_text.get(), password_text.get()))

        user_name_label.place(relx=.2, rely=.2, width=width*.6)
        user_name_text.place(relx=.2, rely=.3, width=width * .6)
        password_label.place(relx=.2, rely=.4, width=width * .6)
        password_text.place(relx=.2, rely=.5, width=width * .6)
        login_button.place(relx=.3, rely=.6, width=width * .4)

    def check_credentials(self, name, password):
        print('checking credentials')
        conn = sqlite3.connect('TaskMaster.db')
        c = conn.cursor()
        c.execute("SELECT * FROM logins WHERE name=?", (name,))
        rows = c.fetchall()
        print(rows)
        if rows:
            if rows[0][1] == password:
                print('LOGGING IN')
            else:
                print('fail')


if __name__ == "__main__":
    initialize_variables()
    app = TaskMasterApp()
    app.mainloop()











