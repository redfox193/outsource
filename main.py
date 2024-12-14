# main.py
import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from sqlalchemy.orm import Session

import schemas
from database import engine, get_db
import models
import crud

# Ensure tables are created at startup
models.Base.metadata.create_all(bind=engine)


def get_database_session():
    db = Session(bind=engine)
    return db


class ProjectManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Справочник проекты-сотрудники")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        self.db = get_database_session()

        header_frame = tk.Frame(self.root)
        header_frame.pack(fill=tk.X, pady=5)

        fio_label = tk.Label(header_frame, text="Гончаров Сергей Витальевич", font=("Arial", 10))
        fio_label.pack(side=tk.LEFT, padx=10)

        course_label = tk.Label(header_frame, text="3 курс 11 группа", font=("Arial", 10))
        course_label.pack(side=tk.LEFT, padx=10)

        info_frame = tk.Frame(self.root)
        info_frame.pack(fill=tk.X, pady=5)
        course_label = tk.Label(info_frame, text="Для сортировки по колонке кликните её по названию", font=("Arial", 10))
        course_label.pack(side=tk.LEFT, padx=10)

        # Dropdown for table selection
        table_frame = tk.Frame(root)
        table_frame.pack(pady=10)

        tk.Label(table_frame, text="Выберите таблицу:").pack(side=tk.LEFT)
        self.selected_table = tk.StringVar()
        self.table_combobox = ttk.Combobox(table_frame, textvariable=self.selected_table, state="readonly")
        self.table_combobox['values'] = ("Projects", "Employees")
        self.table_combobox.pack(side=tk.LEFT)
        self.table_combobox.bind("<<ComboboxSelected>>", self.display_selected_table)
        self.selected_table.set("Projects")

        # Treeview setup
        self.tree = ttk.Treeview(root, columns=("id"), show="headings")
        self.tree.pack(fill="both", expand=True)

        # Buttons for actions
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Добавить", command=self.create_entry).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Изменить", command=self.edit_entry).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Удалить", command=self.delete_entry).pack(side=tk.LEFT, padx=5)

        self.sorted_column = None
        self.sort_order = True  # True for ascending, False for descending

        self.display_selected_table()

    def display_selected_table(self, event=None):
        table_name = self.selected_table.get()
        self.clear_tree()

        def format_date(date):
            return date.strftime("%d.%m.%Y")

        if table_name == "Projects":
            self.setup_tree_columns(["id", "название", "описание", "бюджет", "дедлайн"])
            projects = crud.get_projects(self.db)
            for project in projects:
                self.tree.insert("", "end", iid=project.id,
                                 values=(project.id, project.name, project.description, project.budget, format_date(project.deadline)))
        elif table_name == "Employees":
            self.setup_tree_columns(["id", "имя", "должность", "завершённые проекты", "активный проект"])
            employees = crud.get_employees(self.db)
            for employee in employees:
                if employee.project:
                    project_name = employee.project.name
                else:
                    project_name = None
                self.tree.insert("", "end", iid=employee.id, values=(
                employee.id, employee.fullName, employee.position, employee.completedProjects, project_name))

    def setup_tree_columns(self, columns):
        self.tree['columns'] = columns
        for col in columns:
            if col == "id":
                self.tree.column(col, width=0, stretch=tk.NO)
                self.tree.heading(col, text="")
            else:
                self.tree.column(col, width=100, anchor=tk.W, stretch=tk.YES)
                self.tree.heading(col, text=col.capitalize(), command=lambda col=col: self.sort_treeview(col))

    def sort_treeview(self, column):
        rows = list(self.tree.get_children())

        if self.sorted_column == column:
            self.sort_order = not self.sort_order  # Toggle sort order
        else:
            self.sorted_column = column
            self.sort_order = True  # Default to ascending

        # Function to extract sort key based on column
        def sort_key(row):
            value = self.tree.item(row)['values'][self.tree["columns"].index(column)]
            if column == "дедлайн":
                day, month, year = map(int, value.split("."))
                return year, month, day  # Sort by year, then month, then day
            return value  # For other columns, use raw value

        # Sort rows based on the extracted sort key
        rows.sort(key=sort_key, reverse=not self.sort_order)

        # Rearrange rows in Treeview
        for i, row in enumerate(rows):
            self.tree.move(row, '', i)

    def clear_tree(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

    def create_entry(self):
        table_name = self.selected_table.get()
        if table_name == "Projects":
            self.project_form()
        elif table_name == "Employees":
            self.employee_form()

    def project_form(self, project=None):
        form = tk.Toplevel(self.root)
        form.title("Создать Проект" if not project else "Редактировать Проект")

        tk.Label(form, text="Название:").grid(row=0, column=0)
        name_entry = tk.Entry(form)
        name_entry.grid(row=0, column=1)

        # Pre-fill the name if editing an existing project
        if project:
            name_entry.insert(0, project.name)

        tk.Label(form, text="Описание:").grid(row=1, column=0)
        desc_text = tk.Text(form, height=5, width=30)  # Multiline description
        desc_text.grid(row=1, column=1)

        # Pre-fill the description if editing an existing project
        if project:
            desc_text.insert("1.0", project.description)

        tk.Label(form, text="Бюджет:").grid(row=2, column=0)
        budget_entry = tk.Entry(form)
        budget_entry.grid(row=2, column=1)

        # Pre-fill the budget if editing an existing project
        if project:
            budget_entry.insert(0, project.budget)

        tk.Label(form, text="Дедлайн (выберите дату):").grid(row=3, column=0)

        # Create a label to display the selected date
        selected_date_label = tk.Label(form, text="Выберите дату")
        selected_date_label.grid(row=3, column=1)

        # Add a calendar widget
        cal = Calendar(form, selectmode="day", date_pattern="dd.mm.yyyy")
        cal.grid(row=4, column=1)

        # Pre-fill the calendar with the existing deadline if editing a project
        def update_label(event=None):
            selected_date = cal.get_date()
            selected_date_label.config(text=f"Выбраная дата: {selected_date}")

        cal.bind("<<CalendarSelected>>", update_label)

        if project:
            # Correct way to set the calendar date
            cal.selection_set(project.deadline)  # Set the date for the calendar
            update_label()

        def submit():
            try:
                data = {
                    "name": name_entry.get(),
                    "description": desc_text.get("1.0", "end-1c"),  # Get the text from Text widget
                    "budget": float(budget_entry.get()),
                    "deadline": datetime.strptime(cal.get_date(), "%d.%m.%Y").date(),  # Convert the selected date
                }
                print(data)
                if project:
                    crud.update_project(self.db, project.id, schemas.ProjectUpdate(**data))
                else:
                    crud.create_project(self.db, schemas.ProjectCreate(**data))
                self.display_selected_table()
                form.destroy()
            except ValueError as e:
                messagebox.showerror("Неверный формат данных", str(e))

        tk.Button(form, text="Submit", command=submit).grid(row=5, column=1)

    def employee_form(self, employee=None):
        form = tk.Toplevel(self.root)
        form.title("Создать Сотрудника" if not employee else "Изменить Сотрудника")

        tk.Label(form, text="Имя:").grid(row=0, column=0)
        name_entry = tk.Entry(form, width=25)
        name_entry.grid(row=0, column=1)
        if employee:
            name_entry.insert(0, employee.fullName)

        tk.Label(form, text="Должность:").grid(row=1, column=0)
        position_entry = tk.Entry(form, width=25)
        position_entry.grid(row=1, column=1)
        if employee:
            position_entry.insert(0, employee.position)

        tk.Label(form, text="Завершённые проекты:").grid(row=2, column=0)
        completed_entry = tk.Entry(form, width=25)
        completed_entry.grid(row=2, column=1)
        if employee:
            completed_entry.insert(0, employee.completedProjects)

        tk.Label(form, text="Активный проект:").grid(row=3, column=0)
        project_combobox = ttk.Combobox(form, state="readonly", width=20)
        project_combobox.grid(row=3, column=1)

        projects = crud.get_projects(self.db)
        project_names = [(project.name, project.id) for project in projects]

        project_combobox['values'] = [name for name, _ in project_names] + [None]

        if employee and employee.projectId:
            project_name = next((name for name, pid in project_names if pid == employee.projectId), None)
            project_combobox.set(project_name)
        project_combobox.set('None')

        def submit():
            try:
                selected_project = project_combobox.current()
                if selected_project != len(project_combobox['values']) - 1:
                    selected_project_id = project_names[selected_project][1]
                else:
                    selected_project_id = None

                data = {
                    "fullName": name_entry.get(),
                    "position": position_entry.get(),
                    "completedProjects": int(completed_entry.get()),
                    "projectId": selected_project_id
                }

                if employee:
                    crud.update_employee(self.db, employee.id, schemas.EmployeeUpdate(**data))
                else:
                    crud.create_employee(self.db, schemas.EmployeeCreate(**data))
                self.display_selected_table()
                form.destroy()
            except ValueError as e:
                messagebox.showerror("Неверный формат данных", str(e))

        tk.Button(form, text="Подтвердить", command=submit).grid(row=4, column=1)

    def edit_entry(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Ошибка", "Запись не выбрана")
            return
        row_id = int(selected[0])
        table_name = self.selected_table.get()

        if table_name == "Projects":
            project = self.db.query(models.Project).filter(models.Project.id == row_id).first()
            self.project_form(project)
        elif table_name == "Employees":
            employee = self.db.query(models.Employee).filter(models.Employee.id == row_id).first()
            self.employee_form(employee)

    def delete_entry(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Ошибка", "Запись не выбрана")
            return
        row_id = int(selected[0])
        table_name = self.selected_table.get()

        if table_name == "Projects":
            crud.delete_project(self.db, row_id)
        elif table_name == "Employees":
            crud.delete_employee(self.db, row_id)
        self.display_selected_table()


if __name__ == "__main__":
    root = tk.Tk()
    app = ProjectManagerApp(root)
    root.mainloop()
