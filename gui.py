from tkinter import *
from logic import SemesterManager, Semester

class GradeCalc:
    """Holds GradeCalc content"""

    def __init__(self, root: Tk) -> None:
        """Sets up main window and starts the app"""
        self.semesters = []
        self.window = root
        self.window.title("GradeCalc")
        self.window.geometry("600x500")
        self.window.resizable(False, False)
        self.semester_manager = SemesterManager()
        self.current_frame = None
        self.message_label = Label(self.window, text="", font=("Arial", 12), fg="black", anchor="w")
        self.message_label.pack(side="bottom", fill="x", pady=5)
        self.start_page()

    def clear_frame(self) -> None:
        """Clears current frame from window"""
        if self.current_frame is not None:
            self.current_frame.pack_forget()
            self.current_frame = None

    def start_page(self) -> None:
        """Displays start page with button options and text"""
        self.clear_frame()
        start_frame = Frame(self.window)
        start_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.current_frame = start_frame
        Label(start_frame, text="Welcome to the GradeCalc", font=("Arial", 16)).pack(pady=20)
        Button(start_frame, text="Add Semester", command=self.add_semester).pack(pady=5)
        Button(start_frame, text="View Past Semester", command=self.view_semester).pack(pady=5)
        Button(start_frame, text="Exit", command=self.window.quit).pack(pady=20)

    def add_semester(self) -> None:
        """Shows page for adding a new semester"""
        self.clear_frame()
        add_frame = Frame(self.window)
        add_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.current_frame = add_frame
        Label(add_frame, text="Enter Semester Name:", font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=5)
        semester_name_entry = Entry(add_frame, width=25)
        semester_name_entry.grid(row=0, column=1, pady=5)

        class_entries = []
        for i in range(7):
            Label(add_frame, text=f"Class {i + 1} Name:").grid(row=i + 1, column=0, sticky="w", pady=5)
            class_name_entry = Entry(add_frame, width=20)
            class_name_entry.grid(row=i + 1, column=1, pady=5)
            Label(add_frame, text="Earned/Total:").grid(row=i + 1, column=2, sticky="e", padx=5)
            earned_entry = Entry(add_frame, width=5)
            earned_entry.grid(row=i + 1, column=3, pady=5)
            total_entry = Entry(add_frame, width=5)
            total_entry.grid(row=i + 1, column=4, pady=5)
            class_entries.append((class_name_entry, earned_entry, total_entry))

        def save_semester() -> None:
            """Saves semester details entered by user"""
            semester_name = semester_name_entry.get().strip()
            if not semester_name:
                self.show_message("Semester name can't empty")
                return

            new_semester = Semester(semester_name, self.semester_manager)
            for class_name_entry, earned_entry, total_entry in class_entries:
                class_name = class_name_entry.get().strip()
                if class_name:
                    try:
                        earned = int(earned_entry.get().strip())
                        total = int(total_entry.get().strip())
                        new_semester.add_class(class_name, earned, total)
                    except ValueError:
                        self.show_message("Earned/Total must be an int")
                        return

            self.semester_manager.add_semester(new_semester)
            self.show_message(f"Semester '{semester_name}' added!")
            self.start_page()

        Button(add_frame, text="Save Semester", command=save_semester).grid(row=8, column=1, pady=20)
        Button(add_frame, text="Back", command=self.start_page).grid(row=8, column=2, pady=20)

    def view_semester(self) -> None:
        """Displays the page for viewing past semesters"""

        self.clear_frame()
        view_frame = Frame(self.window)
        view_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.current_frame = view_frame
        Label(view_frame, text="Select Semester to View:", font=("Arial", 12)).pack(anchor="w", pady=5)
        semester_listbox = Listbox(view_frame, height=10, width=50)
        semester_listbox.pack(fill="x", pady=5)

        for semester in self.semester_manager.semesters:
            semester_listbox.insert(END, semester.name)

        def delete_semester() -> None:
            """Deletes selected semester from the list"""
            selected_index = semester_listbox.curselection()

            if not selected_index:
                self.show_message("No semester selected")
                return

            selected_name = semester_listbox.get(selected_index[0])
            self.semester_manager.delete_semester(selected_name)
            semester_listbox.delete(selected_index)
            self.show_message(f"{selected_name} deleted!")

        def view_selected_semester() -> None:
            """Views details of the selected semester"""
            selected_index = semester_listbox.curselection()
            if not selected_index:
                self.show_message("No semester selected")
                return
            selected_name = semester_listbox.get(selected_index[0])
            self.view_semester_info(selected_name)

        Button(view_frame, text="Delete Semester", command=delete_semester).pack(side="left", padx=5)
        Button(view_frame, text="View Semester", command=view_selected_semester).pack(side="right", padx=5)
        Button(view_frame, text="Back", command=self.start_page).pack(side="bottom", pady=10)

    def view_semester_info(self, semester_name: str) -> None:
        """Shows semester overview"""
        self.clear_frame()
        details_frame = Frame(self.window)
        details_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.current_frame = details_frame

        semester = next((s for s in self.semester_manager.semesters if s.name == semester_name), None)
        if not semester:
            self.show_message("Semester not found")
            self.start_page()
            return

        Label(details_frame, text=f"{semester.name}:", font=("Arial", 14)).pack(pady=10)
        grades = semester.calculate_class_grades()
        row = 0
        for class_name, (earned, total) in semester.get_classes():
            grade = grades.get(class_name, 'N/A')
            Label(details_frame, text=f"{class_name}: {earned}/{total} - Grade: {grade}", font=("Arial", 12)).pack(
                anchor="w")
            row += 1
        Button(details_frame, text="Revise", command=lambda: self.edit_semester(semester_name)).pack(
            side="left", padx=5, pady=20)
        Button(details_frame, text="Back", command=self.view_semester).pack(side="right", padx=5, pady=20)

    def edit_semester(self, semester_name: str) -> None:
        """Displays semester for revisions"""
        self.clear_frame()
        edit_frame = Frame(self.window)
        edit_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.current_frame = edit_frame

        semester = next((s for s in self.semester_manager.semesters if s.name == semester_name), None)
        if not semester:
            self.show_message("Semester not found")
            self.start_page()
            return
        Label(edit_frame, text=f"Editing {semester.name}", font=("Arial", 12)).grid(row=0, column=0, columnspan=5,
                                                                                    pady=5)
        class_entries = []
        for i, (class_name, (earned, total)) in enumerate(semester.get_classes()):
            row = i + 1
            Label(edit_frame, text=f"Class {i + 1} Name:").grid(row=row, column=0, sticky="w", pady=5, padx=5)
            class_name_entry = Entry(edit_frame, width=20)
            class_name_entry.insert(0, class_name)
            class_name_entry.grid(row=row, column=1, pady=5, padx=5)
            Label(edit_frame, text="Earned/Total:").grid(row=row, column=2, sticky="e", padx=5)
            earned_entry = Entry(edit_frame, width=5)
            earned_entry.insert(0, earned)
            earned_entry.grid(row=row, column=3, pady=5, padx=5)
            total_entry = Entry(edit_frame, width=5)
            total_entry.insert(0, total)
            total_entry.grid(row=row, column=4, pady=5, padx=5)
            class_entries.append((class_name_entry, earned_entry, total_entry))

        def save_changes() -> None:
            """Saves any revisions to classes"""
            updated_classes = []
            for class_name_entry, earned_entry, total_entry in class_entries:
                updated_class_name = class_name_entry.get().strip()
                if updated_class_name:
                    try:
                        updated_earned = int(earned_entry.get().strip())
                        updated_total = int(total_entry.get().strip())
                        updated_classes.append((updated_class_name, updated_earned, updated_total))
                    except ValueError:
                        self.show_message("Earned/Total must be an int")
                        return

            semester.update_classes(updated_classes)
            self.show_message("Semester updated!")
            self.view_semester_info(semester.name)

        Button(edit_frame, text="Save Changes", command=save_changes).grid(row=row + 1, column=1, pady=20)
        Button(edit_frame, text="Back", command=self.view_semester).grid(row=row + 1, column=2, pady=20)

    def show_message(self, message: str) -> None:
        """Shows message at the bottom of the window"""
        self.message_label.config(text=message)
        self.message_label.place(relx=0.5, rely=1.0, anchor="s")
        self.message_label.pack(side=BOTTOM, pady=10)
        self.message_label.after(3000, lambda: self.message_label.config(text=""))
