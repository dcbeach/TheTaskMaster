from tkinter import *
import tkinter as tk
import random
from tkinter import font as tkfont
import sqlite3
import datetime


def initialize_variables():
    global width, height, user_name, tasks, priority_colors, task_label, user_level

    priority_colors = {5: 'plum2', 4: 'SeaGreen3', 3: 'orange', 2: 'blue', 1: 'red'}

    user_name = "Doug"
    user_level = 0
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
        for F in (UserView, LoginView, AdminView, ViewTasksView, CreateTasksView):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.create_highscore_table()
        self.create_task_table()
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
        elif page_name == 'AdminView':
            self.frames[page_name].update_admin_view()
        elif page_name == 'ViewTasksViewOpen':
            page_name = 'ViewTasksView'
            self.frames[page_name].update_view_tasks_view(0)
        elif page_name == 'ViewTasksViewComplete':
            page_name = 'ViewTasksView'
            self.frames[page_name].update_view_tasks_view(2)
        elif page_name == 'CreateTasksView':
            self.frames[page_name].update_create_tasks_view()

        frame = self.frames[page_name]
        frame.grid()
        frame.winfo_toplevel().geometry("500x550+200+200")

    def create_highscore_table(self):
        conn = sqlite3.connect('TaskMaster.db')
        c = conn.cursor()
        c.execute(
            'CREATE TABLE IF NOT EXISTS logins(name TEXT, password TEXT, access INTEGER)')

    def create_task_table(self):
        conn = sqlite3.connect('TaskMaster.db')
        c = conn.cursor()
        c.execute(
            'CREATE TABLE IF NOT EXISTS tasks(id_num INTEGER, name TEXT, priority INTEGER, difficulty INTEGER, '
                                              'assigned TEXT, duedate TEXT, status INTEGER, completedate TEXT)')

    def add_task(self, name, priority, difficulty, assigned, duedate, status, completedate):
        id_num = random.randint(1, 100000)
        conn = sqlite3.connect('TaskMaster.db')
        c = conn.cursor()
        c.execute("INSERT INTO tasks(id_num, name, priority, difficulty, assigned, duedate, status, completedate) VALUES(?,?,?,?,?,?,?,?)",
                  (id_num, name, priority, difficulty, assigned, duedate, status, completedate))
        conn.commit()
        self.show_frame('CreateTasksView')

    def update_task(self, status, completedate, id_num):
        conn = sqlite3.connect('TaskMaster.db')
        c = conn.cursor()
        c.execute("UPDATE tasks SET status=?, completedate=? WHERE id_num=?",
                  (status, completedate, id_num))
        conn.commit()

    def load_tasks_username(self, user_name, status):
        conn = sqlite3.connect('TaskMaster.db')
        c = conn.cursor()
        c.execute("SELECT * FROM tasks WHERE assigned=? AND status=?", (user_name, status))
        rows = c.fetchall()
        print(rows)
        return rows

    def load_tasks_all(self, status):
        conn = sqlite3.connect('TaskMaster.db')
        c = conn.cursor()
        c.execute("SELECT * FROM tasks WHERE status=?", (status,))
        rows = c.fetchall()
        print(rows)
        return rows

class AdminView(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

    def update_admin_view(self):
        label = tk.Label(self, text="Welcome " + user_name, font=self.controller.title_font)
        label.place(relx=.1, rely=.05, width=.8 * width)

        view_tasks_button = tk.Button(self, text="View Open Tasks", font=self.controller.title_font, bg='light blue',
                                        command=lambda: self.controller.show_frame('ViewTasksViewOpen'))
        create_tasks_button = tk.Button(self, text="Create Tasks", font=self.controller.title_font, bg='light blue',
                                      command=lambda: self.controller.show_frame('CreateTasksView'))
        my_tasks_button = tk.Button(self, text="My Tasks", font=self.controller.title_font, bg='light blue',
                                    command=lambda: self.controller.show_frame('UserView'))
        status_update_button = tk.Button(self, text="View Completed Tasks", font=self.controller.title_font, bg='light blue',
                                         command=lambda: self.controller.show_frame('ViewTasksViewComplete'))

        view_tasks_button.place(relx=.2, rely=.2, width=.6 * width)
        create_tasks_button.place(relx=.2, rely=.35, width=.6 * width)
        my_tasks_button.place(relx=.2, rely=.5, width=.6 * width)
        status_update_button.place(relx=.2, rely=.65, width=.6 * width)


class CreateTasksView(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

    def update_create_tasks_view(self):
        label = tk.Label(self, text="Welcome " + user_name, font=self.controller.title_font)
        label.place(relx=.1, rely=.05, width=.8 * width)

        task_name_label = tk.Label(self, text="Task Name:", anchor=E, font=('Helvetica', 14))
        priority_label = tk.Label(self, text="Priority Level:", anchor=E, width=20, font=('Helvetica', 14))
        difficulty_label = tk.Label(self, text="Difficulty Level:", anchor=E, width=20, font=('Helvetica', 14))
        due_date_label = tk.Label(self, text="Due Date:", anchor=E, width=20, font=('Helvetica', 14))
        assign_user_label = tk.Label(self, text="Assigned To:", anchor=E, width=20, font=('Helvetica', 14))

        task_name_entry = tk.Entry(self, width=15, font=('Helvetica', 10))
        priority_entry = tk.Entry(self, width=15, font=('Helvetica', 10))
        difficulty_entry = tk.Entry(self, width=15, font=('Helvetica', 10))
        due_date_entry = tk.Entry(self, width=15, font=('Helvetica', 10))
        assign_user_entry = tk.Entry(self, width=15, font=('Helvetica', 10))

        task_name_label.place(relx=.1, y=(height * .15), width=width*.4)
        priority_label.place(relx=.1, y=(height * .15) + 30, width=width * .4)
        difficulty_label.place(relx=.1, y=(height * .15) + 60, width=width * .4)
        due_date_label.place(relx=.1, y=(height * .15) + 90, width=width * .4)
        assign_user_label.place(relx=.1, y=(height * .15) + 120, width=width * .4)

        task_name_entry.place(relx=.51, y=(height * .15), width=width * .4)
        priority_entry.place(relx=.51, y=(height * .15) + 30, width=width * .4)
        difficulty_entry.place(relx=.51, y=(height * .15) + 60, width=width * .4)
        due_date_entry.place(relx=.51, y=(height * .15) + 90, width=width * .4)
        assign_user_entry.place(relx=.51, y=(height * .15) + 120, width=width * .4)

        add_task_button = tk.Button(self, text="Add Current Task", font=self.controller.title_font, bg='light blue',
                                        command=lambda: self.controller.add_task(task_name_entry.get(), priority_entry.get(), difficulty_entry.get(),
                                                                                 assign_user_entry.get(), due_date_entry.get(), 0, 0))

        add_task_button.place(relx=.2, rely=.70, width=.6 * width)
        return_to_main_button = tk.Button(self, text="Return to Main", font=self.controller.title_font, bg='light blue',
                                        command=lambda: self.controller.show_frame('AdminView'))
        return_to_main_button.place(relx=.4, rely=.85, width=.55 * width)


class ViewTasksView(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

    def update_view_tasks_view(self, status):
        label = tk.Label(self, text="Welcome " + user_name, font=self.controller.title_font)
        label.place(relx=.1, rely=.05, width=.8 * width)

        tasks = self.controller.load_tasks_all(status)
        task_frame = []
        task_label = []
        completed_by_label = []
        completed_date_label = []

        if len(tasks) >= 10:
            task_length = 10
        else:
            task_length = len(tasks)

        tasks.sort(key=lambda x: x[2])

        for i in range(task_length):
            task_frame.append(Frame(self, width=.6 * width, height=30,
                                    highlightbackground=priority_colors[tasks[i][2]],
                                    highlightthickness=1))
            task_frame[i].place(relx=.20, y=(height * .15) + (35 * i))
            self.update_idletasks()

            task_label.append(Label(task_frame[i], text=tasks[i][1], anchor=W, font=("Helvetica", 10)))
            task_label[i].place(relx=.01, rely=.10, width=task_frame[i].winfo_width() / 3)

            completed_by_label.append(Label(task_frame[i], text=tasks[i][4], anchor=CENTER, font=("Helvetica", 10)))
            completed_by_label[i].place(relx=.31, rely=.10, width=task_frame[i].winfo_width() / 3)

            date = tasks[i][7]
            if status == 0:
                date = 'OPEN'

            completed_date_label.append(Label(task_frame[i], text=date, anchor=E, font=("Helvetica", 10)))
            completed_date_label[i].place(relx=.61, rely=.10, width=task_frame[i].winfo_width() / 3)

        manage_tasks_button = tk.Button(self, text="Return to Main", font=self.controller.title_font, bg='light blue',
                                        command=lambda: self.controller.show_frame('AdminView'))
        manage_tasks_button.place(relx=.4, rely=.85, width=.55 * width)


class UserView(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

    def update_user_display(self):
        label = tk.Label(self, text="Welcome " + user_name, font=self.controller.title_font)
        label.place(relx=.1, rely=.05, width=.8 * width)

        global task_frame, task_label, inprogress, tasks, difficulty_label

        tasks = self.controller.load_tasks_username(user_name, 0)

        task_frame = []
        task_label = []
        due_date_label = []
        complete_button = []
        inprogress_button = []
        inprogress = []

        if len(tasks) >= 4:
            task_length = 4
        else:
            task_length = len(tasks)

        tasks.sort(key=lambda x: x[2])

        # Displays each task in own frame
        # Task Frame Color = Priority
        # Due Date Color = Difficulty
        for i in range(task_length):
            task_frame.append(Frame(self, width=.6 * width, height=75,
                                    highlightbackground=priority_colors[tasks[i][2]],
                                    highlightthickness=3))
            task_frame[i].place(relx=.20, y=(height * .10) + 50 + (100 * i))
            self.update_idletasks()

            task_label.append(Label(task_frame[i], text=tasks[i][1], anchor=W, font=("Helvetica", 15)))
            due_date_label.append(Label(task_frame[i], text=tasks[i][5], anchor=CENTER, font=("Helvetica", 15),
                                        bg=priority_colors[tasks[i][3]]))

            task_label[i].place(relx=.01, rely=.10, width=task_frame[i].winfo_width() / 2)
            due_date_label[i].place(relx=.6, rely=.1, width=task_frame[i].winfo_width() * .35)

            inprogress_button.append(Button(task_frame[i], text="In Progress", bg='aqua',
                                            command=(lambda x=i: inprogress_clicked(x))))
            complete_button.append(Button(task_frame[i], text="Complete", bg='green',
                                          command=(lambda x=i: complete_clicked(x))))

            inprogress.append(False)
            inprogress_button[i].place(relx=.15, rely=.6, width=task_frame[i].winfo_width() / 3)
            complete_button[i].place(relx=.55, rely=.6, width=task_frame[i].winfo_width() / 3)

        if user_level == 2:
            return_to_main_button = tk.Button(self, text="Return to Main", font=self.controller.title_font, bg='light blue',
                                              command=lambda: self.controller.show_frame('AdminView'))
            return_to_main_button.place(relx=.4, rely=.85, width=.55 * width)

        def complete_clicked(x):
            now = datetime.datetime.now()
            self.controller.update_task(2, now.strftime("%Y-%m-%d"), tasks[x][0])
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

    # Login Levels
    # 0 = Incorrect, 1 = Basic, 2 = Admin
    def check_credentials(self, name, password):
        global user_name, user_level
        user_name = name
        conn = sqlite3.connect('TaskMaster.db')
        c = conn.cursor()
        c.execute("SELECT * FROM logins WHERE name=?", (name,))
        rows = c.fetchall()
        print(rows)
        if rows:
            if rows[0][1] == password:
                if rows[0][2] == 1:
                    user_level = 1
                    self.controller.show_frame('UserView')
                elif rows[0][2] == 2:
                    user_level = 2
                    self.controller.show_frame('AdminView')
            else:
                print('fail')


if __name__ == "__main__":
    initialize_variables()
    app = TaskMasterApp()
    app.mainloop()











