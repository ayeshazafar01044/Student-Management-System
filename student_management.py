import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk, ImageDraw, ImageOps
import json
import os
import shutil
from datetime import datetime

# ============================================================
# STUDENT MANAGEMENT SYSTEM
# Python + Tkinter + Pillow
# Features:
# - Add unlimited students
# - Edit / Delete students
# - Choose ANY JPG / JPEG / PNG / WEBP picture
# - Pictures are copied into student_photos automatically
# - Pictures are shown as CIRCLES
# - Automatic JSON saving
# - Manual Save Data button
# - Backup Data
# - Search
# - Statistics
# - Settings / About information
# ============================================================

APP_TITLE = "Student Management System"
VERSION = "3.0.0"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE_NAME = "students.json"
PHOTO_DIR_NAME = "student_photos"

DATA_FILE = os.path.join(BASE_DIR, DATA_FILE_NAME)
PHOTO_DIR = os.path.join(BASE_DIR, PHOTO_DIR_NAME)

# ------------------------- Theme -------------------------
BG = "#061425"
SIDEBAR = "#08182B"
CARD = "#0C1D31"
PURPLE = "#5B21D1"
PURPLE2 = "#6D28D9"
CYAN = "#17E6C1"
GREEN = "#22C55E"
BLUE = "#2563EB"
ORANGE = "#F59E0B"
RED = "#EF3340"
TEXT = "#F7FAFF"
MUTED = "#A8B4C7"
BORDER = "#1B3654"

DEFAULT_STUDENTS = [
    {
        "name": "Ayesha Zafar",
        "roll": "01017",
        "age": "20",
        "email": "ayesha.zafar@example.com",
        "department": "Software Engineering",
        "marks": 95,
        "photo": ""
    },
    {
        "name": "Muhammad Ali",
        "roll": "01018",
        "age": "21",
        "email": "muhammad.ali@example.com",
        "department": "Computer Science",
        "marks": 88,
        "photo": ""
    },
    {
        "name": "Fatima Noor",
        "roll": "01019",
        "age": "20",
        "email": "fatima.noor@example.com",
        "department": "Software Engineering",
        "marks": 76,
        "photo": ""
    },
    {
        "name": "Usman Ahmed",
        "roll": "01020",
        "age": "22",
        "email": "usman.ahmed@example.com",
        "department": "Information Technology",
        "marks": 65,
        "photo": ""
    },
    {
        "name": "Zainab Khan",
        "roll": "01021",
        "age": "19",
        "email": "zainab.khan@example.com",
        "department": "Computer Science",
        "marks": 72,
        "photo": ""
    }
]


# ============================================================
# DATA
# ============================================================

def load_students():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
            if isinstance(data, list):
                return data
        except (json.JSONDecodeError, OSError):
            pass

    students = [dict(s) for s in DEFAULT_STUDENTS]
    save_students(students, show_error=False)
    return students


def save_students(students, show_error=True):
    try:
        os.makedirs(PHOTO_DIR, exist_ok=True)
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(students, file, indent=2, ensure_ascii=False)
        return True
    except OSError as error:
        if show_error:
            messagebox.showerror("Save Error", str(error))
        return False


def get_grade(mark):
    try:
        mark = float(mark)
    except (TypeError, ValueError):
        return "F"

    if mark >= 90:
        return "A+"
    if mark >= 80:
        return "A"
    if mark >= 70:
        return "B"
    if mark >= 60:
        return "C"
    if mark >= 50:
        return "D"
    return "F"


# ============================================================
# MAIN APP
# ============================================================

class StudentManagementApp:

    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("1500x900")
        self.root.minsize(1100, 700)
        self.root.configure(bg=BG)

        os.makedirs(PHOTO_DIR, exist_ok=True)

        self.students = load_students()
        self.selected_index = None
        self.photo_path = ""

        # Keep PhotoImage objects alive.
        self.image_refs = []
        self.avatar_cache = {}

        self.setup_styles()
        self.build_window()
        self.refresh_table()

    # ========================================================
    # STYLES
    # ========================================================

    def setup_styles(self):
        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Treeview",
            background=CARD,
            fieldbackground=CARD,
            foreground=TEXT,
            rowheight=72,
            borderwidth=0,
            font=("Segoe UI", 10)
        )

        style.configure(
            "Treeview.Heading",
            background=PURPLE,
            foreground=TEXT,
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padding=10
        )

        style.map(
            "Treeview",
            background=[("selected", "#263F61")],
            foreground=[("selected", TEXT)]
        )

        style.configure(
            "TCombobox",
            fieldbackground="#081A2D",
            background="#081A2D",
            foreground=TEXT
        )

    # ========================================================
    # WINDOW
    # ========================================================

    def build_window(self):
        header = tk.Frame(self.root, bg="#061A30", height=145)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        brand = tk.Frame(header, bg="#061A30")
        brand.pack(side="left", fill="y", padx=24)

        tk.Label(
            brand,
            text="🎓",
            bg="#061A30",
            fg=TEXT,
            font=("Segoe UI Emoji", 48)
        ).pack(side="left", padx=(0, 18))

        title_box = tk.Frame(brand, bg="#061A30")
        title_box.pack(side="left", pady=22)

        tk.Label(
            title_box,
            text=APP_TITLE,
            bg="#061A30",
            fg=TEXT,
            font=("Segoe UI", 26, "bold")
        ).pack(anchor="w")

        tk.Label(
            title_box,
            text="Python Desktop Application",
            bg="#061A30",
            fg=TEXT,
            font=("Segoe UI", 13)
        ).pack(anchor="w", pady=2)

        header_art = self.create_header_art()
        self.image_refs.append(header_art)

        tk.Label(
            header,
            image=header_art,
            bg="#061A30"
        ).pack(side="right", padx=18)

        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True)

        self.sidebar = tk.Frame(body, bg=SIDEBAR, width=210)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.main_area = tk.Frame(body, bg=BG)
        self.main_area.pack(side="left", fill="both", expand=True)

        self.build_sidebar()
        self.build_scroll_area()
        self.build_dashboard()

        footer = tk.Frame(self.root, bg="#0A2037", height=42)
        footer.pack(side="bottom", fill="x")
        footer.pack_propagate(False)

        tk.Label(
            footer,
            text="▣  Data File: ",
            bg="#0A2037",
            fg=TEXT,
            font=("Segoe UI", 10)
        ).pack(side="left", padx=(30, 0))

        tk.Label(
            footer,
            text=DATA_FILE_NAME,
            bg="#0A2037",
            fg=GREEN,
            font=("Segoe UI", 10, "bold")
        ).pack(side="left")

        self.updated_label = tk.Label(
            footer,
            text="",
            bg="#0A2037",
            fg=MUTED,
            font=("Segoe UI", 10)
        )
        self.updated_label.pack(side="left", expand=True)

        tk.Label(
            footer,
            text="🛡  Auto Save: ON",
            bg="#0A2037",
            fg=GREEN,
            font=("Segoe UI", 10, "bold")
        ).pack(side="right", padx=30)

    # ========================================================
    # SIDEBAR
    # ========================================================

    def build_sidebar(self):
        items = [
            ("⌂", "Dashboard"),
            ("♟", "All Students"),
            ("＋", "Add Student"),
            ("⌕", "Search Student"),
            ("◔", "Statistics"),
            ("▣", "Backup Data"),
            ("💾", "Save Data"),
            ("⚙", "Settings"),
            ("ⓘ", "About")
        ]

        for icon, text in items:
            button = tk.Button(
                self.sidebar,
                text=f"  {icon}   {text}",
                anchor="w",
                bg=SIDEBAR,
                fg=TEXT,
                activebackground=PURPLE,
                activeforeground=TEXT,
                bd=0,
                relief="flat",
                font=("Segoe UI", 11),
                padx=16,
                pady=14,
                cursor="hand2",
                command=lambda value=text: self.navigation(value)
            )
            button.pack(fill="x", padx=14, pady=3)

        spacer = tk.Frame(self.sidebar, bg=SIDEBAR)
        spacer.pack(expand=True, fill="both")

        version_box = tk.Frame(
            self.sidebar,
            bg="#32157A",
            height=125
        )
        version_box.pack(fill="x", padx=12, pady=10)
        version_box.pack_propagate(False)

        tk.Label(
            version_box,
            text="🎓",
            bg="#32157A",
            fg=TEXT,
            font=("Segoe UI Emoji", 34)
        ).pack(pady=(8, 0))

        tk.Label(
            version_box,
            text="Student Management",
            bg="#32157A",
            fg=TEXT,
            font=("Segoe UI", 10, "bold")
        ).pack()

        tk.Label(
            version_box,
            text="System",
            bg="#32157A",
            fg=TEXT,
            font=("Segoe UI", 10, "bold")
        ).pack()

        tk.Label(
            version_box,
            text=f"v{VERSION}",
            bg="#32157A",
            fg="#22FF76",
            font=("Segoe UI", 10, "bold")
        ).pack()

    # ========================================================
    # SCROLL AREA
    # ========================================================

    def build_scroll_area(self):
        self.canvas = tk.Canvas(
            self.main_area,
            bg=BG,
            highlightthickness=0
        )

        self.scrollbar = ttk.Scrollbar(
            self.main_area,
            orient="vertical",
            command=self.canvas.yview
        )

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.content = tk.Frame(self.canvas, bg=BG)

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.content,
            anchor="nw"
        )

        self.content.bind(
            "<Configure>",
            lambda event: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.bind(
            "<Configure>",
            lambda event: self.canvas.itemconfig(
                self.canvas_window,
                width=event.width
            )
        )

        self.canvas.bind_all("<MouseWheel>", self.mouse_wheel)

    def mouse_wheel(self, event):
        try:
            self.canvas.yview_scroll(
                int(-1 * (event.delta / 120)),
                "units"
            )
        except Exception:
            pass

    # ========================================================
    # HEADER ART
    # ========================================================

    def create_header_art(self, width=540, height=110):
        img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        for x, color in [(15, PURPLE), (48, CYAN), (81, ORANGE)]:
            draw.rounded_rectangle(
                (x, 72, x + 58, 87),
                radius=4,
                fill=color
            )

        # Student 1
        draw.ellipse((145, 18, 205, 78), fill="#F1B39F")
        draw.ellipse((139, 12, 211, 54), fill="#29202B")
        draw.rounded_rectangle(
            (132, 70, 218, 105),
            radius=12,
            fill="#D94680"
        )

        # Student 2
        draw.ellipse((255, 16, 315, 76), fill="#D6B090")
        draw.ellipse((249, 10, 321, 52), fill="#17212D")
        draw.rounded_rectangle(
            (242, 70, 328, 105),
            radius=12,
            fill="#2563EB"
        )

        # Student 3
        draw.ellipse((365, 18, 425, 78), fill="#F0C19F")
        draw.ellipse((359, 12, 431, 52), fill="#3B241D")
        draw.rounded_rectangle(
            (352, 70, 438, 105),
            radius=12,
            fill="#F59E0B"
        )

        return ImageTk.PhotoImage(img)

    # ========================================================
    # DASHBOARD
    # ========================================================

    def build_dashboard(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        cards = tk.Frame(self.content, bg=BG)
        cards.pack(fill="x", padx=16, pady=(16, 12))

        for column in range(4):
            cards.columnconfigure(column, weight=1)

        self.card_total = self.make_summary_card(
            cards, "TOTAL STUDENTS", "0",
            "Students Registered", PURPLE, "♟"
        )

        self.card_average = self.make_summary_card(
            cards, "AVERAGE MARKS", "0",
            "Overall Average", "#1557A6", "↗"
        )

        self.card_highest = self.make_summary_card(
            cards, "HIGHEST MARKS", "0",
            "Top Score", "#17603F", "🏆"
        )

        self.card_departments = self.make_summary_card(
            cards, "DEPARTMENTS", "0",
            "Departments", "#A86606", "▣"
        )

        self.card_total.grid(row=0, column=0, sticky="ew", padx=(0, 7))
        self.card_average.grid(row=0, column=1, sticky="ew", padx=7)
        self.card_highest.grid(row=0, column=2, sticky="ew", padx=7)
        self.card_departments.grid(row=0, column=3, sticky="ew", padx=(7, 0))

        lower = tk.Frame(self.content, bg=BG)
        lower.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        lower.grid_columnconfigure(1, weight=1)
        lower.grid_rowconfigure(0, weight=1)

        self.form_panel = tk.Frame(
            lower,
            bg=CARD,
            highlightbackground=BORDER,
            highlightthickness=1,
            width=350
        )
        self.form_panel.grid(
            row=0, column=0, sticky="nsew", padx=(0, 10)
        )
        self.form_panel.grid_propagate(False)

        self.table_panel = tk.Frame(
            lower,
            bg=CARD,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        self.table_panel.grid(row=0, column=1, sticky="nsew")

        self.build_student_form()
        self.build_student_table()

    def make_summary_card(self, parent, title, value, subtitle, color, icon):
        card = tk.Frame(parent, bg=color, height=112)
        card.grid_propagate(False)
        card.columnconfigure(1, weight=1)

        tk.Label(
            card,
            text=icon,
            bg=color,
            fg=TEXT,
            font=("Segoe UI Emoji", 30)
        ).grid(
            row=0, column=0, rowspan=3,
            padx=(20, 12), pady=12
        )

        text = tk.Frame(card, bg=color)
        text.grid(
            row=0, column=1,
            sticky="nsew",
            padx=(0, 15), pady=12
        )

        tk.Label(
            text, text=title, bg=color, fg=TEXT,
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w")

        value_label = tk.Label(
            text, text=value, bg=color, fg=TEXT,
            font=("Segoe UI", 23, "bold")
        )
        value_label.pack(anchor="w")

        tk.Label(
            text, text=subtitle, bg=color, fg=TEXT,
            font=("Segoe UI", 9)
        ).pack(anchor="w")

        card.value_label = value_label
        return card

    # ========================================================
    # FORM
    # ========================================================

    def form_label(self, text):
        label = tk.Label(
            self.form_panel,
            text=text,
            bg=CARD,
            fg=TEXT,
            font=("Segoe UI", 9)
        )
        label.pack(anchor="w", padx=14)
        return label

    def form_entry(self, variable):
        entry = tk.Entry(
            self.form_panel,
            textvariable=variable,
            bg="#081A2D",
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
            highlightthickness=1,
            highlightbackground=BORDER,
            highlightcolor=CYAN,
            font=("Segoe UI", 10)
        )
        entry.pack(fill="x", padx=14, pady=(3, 7), ipady=7)
        return entry

    def build_student_form(self):
        tk.Label(
            self.form_panel,
            text="♟  Add / Update Student",
            bg=CARD,
            fg=CYAN,
            font=("Segoe UI", 17, "bold")
        ).pack(anchor="w", padx=18, pady=(18, 8))

        # Circular preview
        self.preview = tk.Label(
            self.form_panel,
            bg=CARD,
            width=110,
            height=110
        )
        self.preview.pack(pady=(2, 8))

        tk.Button(
            self.form_panel,
            text="📷  Choose Any Picture",
            command=self.choose_picture,
            bg="#C62B6A",
            fg=TEXT,
            bd=0,
            font=("Segoe UI", 10, "bold"),
            padx=14,
            pady=8,
            cursor="hand2"
        ).pack(pady=(0, 10))

        self.name_var = tk.StringVar()
        self.roll_var = tk.StringVar()
        self.age_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.department_var = tk.StringVar()
        self.marks_var = tk.StringVar()
        self.search_var = tk.StringVar()

        self.form_label("Full Name")
        self.name_entry = self.form_entry(self.name_var)

        self.form_label("Roll Number")
        self.form_entry(self.roll_var)

        self.form_label("Age")
        self.form_entry(self.age_var)

        self.form_label("Email")
        self.form_entry(self.email_var)

        self.form_label("Department")

        self.department_box = ttk.Combobox(
            self.form_panel,
            textvariable=self.department_var,
            state="readonly",
            values=[
                "Software Engineering",
                "Computer Science",
                "Information Technology",
                "Data Science",
                "Artificial Intelligence",
                "Cyber Security",
                "Business Administration",
                "Other"
            ]
        )
        self.department_box.pack(
            fill="x", padx=14, pady=(3, 7), ipady=5
        )

        self.form_label("Marks")
        self.form_entry(self.marks_var)

        buttons = tk.Frame(self.form_panel, bg=CARD)
        buttons.pack(fill="x", padx=14, pady=4)

        buttons.columnconfigure(0, weight=1)
        buttons.columnconfigure(1, weight=1)

        self.make_button(
            buttons, "＋  Add Student",
            self.add_student, GREEN
        ).grid(row=0, column=0, sticky="ew", padx=(0, 4))

        self.make_button(
            buttons, "✎  Update",
            self.update_student, ORANGE
        ).grid(row=0, column=1, sticky="ew", padx=(4, 0))

        self.make_button(
            buttons, "▣  Delete",
            self.delete_student, RED
        ).grid(row=1, column=0, sticky="ew", padx=(0, 4), pady=(7, 0))

        self.make_button(
            buttons, "⌫  Clear",
            self.clear_form, BLUE
        ).grid(row=1, column=1, sticky="ew", padx=(4, 0), pady=(7, 0))

        tk.Label(
            self.form_panel,
            text="You can add as many students as you want.\n"
                 "Choose any JPG, JPEG, PNG or WEBP picture.",
            bg=CARD,
            fg=MUTED,
            justify="left",
            font=("Segoe UI", 8)
        ).pack(anchor="w", padx=14, pady=(8, 10))

    def make_button(self, parent, text, command, bg):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg,
            fg="white",
            bd=0,
            font=("Segoe UI", 10, "bold"),
            pady=9,
            cursor="hand2"
        )

    # ========================================================
    # TABLE
    # ========================================================

    def build_student_table(self):
        top = tk.Frame(self.table_panel, bg=CARD)
        top.pack(fill="x", padx=12, pady=(18, 10))

        tk.Label(
            top, text="⌕", bg=CARD, fg=TEXT,
            font=("Segoe UI", 23)
        ).pack(side="left", padx=(4, 8))

        search_entry = tk.Entry(
            top,
            textvariable=self.search_var,
            bg="#081A2D",
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
            highlightthickness=1,
            highlightbackground=BORDER,
            font=("Segoe UI", 10)
        )
        search_entry.pack(side="left", fill="x", expand=True, ipady=9)

        search_entry.bind(
            "<Return>", lambda event: self.refresh_table()
        )

        tk.Button(
            top,
            text="⌕  Search",
            command=self.refresh_table,
            bg=PURPLE2,
            fg=TEXT,
            bd=0,
            font=("Segoe UI", 10, "bold"),
            padx=16,
            pady=9,
            cursor="hand2"
        ).pack(side="left", padx=8)

        tk.Button(
            top,
            text="Show All",
            command=self.show_all,
            bg="#25354A",
            fg=TEXT,
            bd=0,
            font=("Segoe UI", 10, "bold"),
            padx=16,
            pady=9,
            cursor="hand2"
        ).pack(side="left")

        columns = (
            "Name", "Roll No", "Age",
            "Department", "Marks", "Grade", "Action"
        )

        self.tree = ttk.Treeview(
            self.table_panel,
            columns=columns,
            show="tree headings",
            selectmode="browse"
        )

        # Photo is #0 because Tkinter Treeview supports images only there.
        self.tree.heading("#0", text="Photo")
        self.tree.column(
            "#0", width=82, minwidth=70,
            anchor="center", stretch=False
        )

        widths = {
            "Name": 155,
            "Roll No": 85,
            "Age": 60,
            "Department": 190,
            "Marks": 75,
            "Grade": 75,
            "Action": 145
        }

        for column in columns:
            self.tree.heading(column, text=column)
            self.tree.column(
                column,
                width=widths[column],
                minwidth=55,
                anchor="center"
            )

        self.tree.column("Name", anchor="w")
        self.tree.column("Department", anchor="w")
        self.tree.column("Action", anchor="center")

        self.tree.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0, 10)
        )

        self.tree.bind(
            "<<TreeviewSelect>>",
            self.select_student
        )

        self.tree.bind(
            "<Button-1>",
            self.table_action_click
        )

    def table_action_click(self, event):
        row_id = self.tree.identify_row(event.y)
        column_id = self.tree.identify_column(event.x)

        if not row_id or column_id != "#7":
            return

        try:
            index = int(row_id)
        except ValueError:
            return

        if not (0 <= index < len(self.students)):
            return

        bbox = self.tree.bbox(row_id, "#7")
        if not bbox:
            return

        x_start, _, width, _ = bbox
        relative_x = event.x - x_start

        if relative_x < width / 2:
            self.edit_by_index(index)
        else:
            self.delete_by_index(index)

    def edit_by_index(self, index):
        if not (0 <= index < len(self.students)):
            return

        self.selected_index = index
        student = self.students[index]

        self.name_var.set(student.get("name", ""))
        self.roll_var.set(student.get("roll", ""))
        self.age_var.set(student.get("age", ""))
        self.email_var.set(student.get("email", ""))
        self.department_var.set(student.get("department", ""))
        self.marks_var.set(str(student.get("marks", "")))
        self.photo_path = student.get("photo", "")

        self.update_preview()
        self.name_entry.focus_set()

    def delete_by_index(self, index):
        if not (0 <= index < len(self.students)):
            return

        student = self.students[index]

        answer = messagebox.askyesno(
            "Delete Student",
            f"Are you sure you want to delete "
            f"{student.get('name', 'this student')}?"
        )

        if not answer:
            return

        photo = self.resolve_photo_path(student.get("photo", ""))

        self.students.pop(index)

        # Remove the student's copied picture too.
        if photo and os.path.exists(photo):
            try:
                os.remove(photo)
            except OSError:
                pass

        self.selected_index = None
        self.clear_form()
        save_students(self.students)
        self.refresh_table()

        messagebox.showinfo(
            "Deleted",
            "Student deleted successfully! ✓"
        )

    # ========================================================
    # TABLE REFRESH
    # ========================================================

    def refresh_table(self):
        if not hasattr(self, "tree"):
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        query = self.search_var.get().strip().lower()
        self.image_refs = []

        for index, student in enumerate(self.students):
            searchable = " ".join(
                str(student.get(key, ""))
                for key in (
                    "name", "roll", "age",
                    "department", "email"
                )
            ).lower()

            if query and query not in searchable:
                continue

            photo = self.create_avatar(
                student.get("name", "Student"),
                58,
                index,
                student.get("photo", "")
            )

            self.image_refs.append(photo)

            self.tree.insert(
                "",
                "end",
                iid=str(index),
                image=photo,
                values=(
                    student.get("name", ""),
                    student.get("roll", ""),
                    student.get("age", ""),
                    student.get("department", ""),
                    self.format_marks(student.get("marks", "")),
                    get_grade(student.get("marks", 0)),
                    "✎ Edit    🗑 Delete"
                )
            )

        self.update_summary()
        self.update_preview()

    def format_marks(self, marks):
        try:
            value = float(marks)
            return f"{value:g}"
        except (TypeError, ValueError):
            return str(marks)

    # ========================================================
    # SUMMARY
    # ========================================================

    def update_summary(self):
        total = len(self.students)

        marks_list = []

        for student in self.students:
            try:
                marks_list.append(float(student.get("marks", 0)))
            except (TypeError, ValueError):
                pass

        average = sum(marks_list) / len(marks_list) if marks_list else 0
        highest = max(marks_list, default=0)

        departments = len({
            student.get("department", "")
            for student in self.students
            if student.get("department", "")
        })

        self.card_total.value_label.config(text=str(total))
        self.card_average.value_label.config(text=f"{average:.2f}")
        self.card_highest.value_label.config(text=f"{highest:g}")
        self.card_departments.value_label.config(text=str(departments))

        self.updated_label.config(
            text="  Last Updated: "
            + datetime.now().strftime("%d-%b-%Y %I:%M:%S %p")
        )

    # ========================================================
    # CIRCULAR PHOTO SYSTEM
    # ========================================================

    def resolve_photo_path(self, photo_path):
        if not photo_path:
            return ""

        if os.path.isabs(photo_path):
            return photo_path

        return os.path.join(BASE_DIR, photo_path)

    def circular_photo(self, source, size=100):
        """
        Takes a PIL image and returns a circular ImageTk.PhotoImage.
        This is used for both real student photos and generated avatars.
        """
        source = source.convert("RGB")

        # Make the image square by cropping the sides/top as necessary.
        source = ImageOps.fit(
            source,
            (size, size),
            method=Image.LANCZOS,
            centering=(0.5, 0.5)
        )

        result = Image.new(
            "RGBA",
            (size, size),
            (0, 0, 0, 0)
        )

        result.paste(source, (0, 0))

        mask = Image.new("L", (size, size), 0)
        mask_draw = ImageDraw.Draw(mask)

        mask_draw.ellipse(
            (2, 2, size - 3, size - 3),
            fill=255
        )

        result.putalpha(mask)

        # Circular border.
        draw = ImageDraw.Draw(result)
        draw.ellipse(
            (2, 2, size - 3, size - 3),
            outline=CYAN,
            width=max(2, size // 22)
        )

        return ImageTk.PhotoImage(result)

    def create_avatar(
        self,
        name,
        size=100,
        seed=0,
        photo_path=""
    ):
        # First priority: user's selected real picture.
        resolved_photo = self.resolve_photo_path(photo_path)

        if resolved_photo and os.path.exists(resolved_photo):
            try:
                img = Image.open(resolved_photo)
                return self.circular_photo(img, size)
            except Exception:
                pass

        # Otherwise create a circular placeholder avatar.
        key = (name, size, seed)

        if key in self.avatar_cache:
            return self.avatar_cache[key]

        palettes = [
            ("#F2B8A8", "#241723", "#D94680"),
            ("#D7B08D", "#17202B", "#2563EB"),
            ("#E4BFA6", "#202B20", "#168A65"),
            ("#C99576", "#171717", "#B7B7B7"),
            ("#F0C2A2", "#3B261B", "#F59E0B")
        ]

        skin, hair, shirt = palettes[seed % len(palettes)]

        img = Image.new(
            "RGB",
            (size, size),
            "#173550"
        )

        draw = ImageDraw.Draw(img)
        cx = size // 2

        # Face
        draw.ellipse(
            (
                cx - size * 0.20,
                size * 0.18,
                cx + size * 0.20,
                size * 0.55
            ),
            fill=skin
        )

        # Hair
        draw.ellipse(
            (
                cx - size * 0.25,
                size * 0.08,
                cx + size * 0.25,
                size * 0.43
            ),
            fill=hair
        )

        # Repaint face lower section to make hair look natural.
        draw.ellipse(
            (
                cx - size * 0.19,
                size * 0.20,
                cx + size * 0.19,
                size * 0.56
            ),
            fill=skin
        )

        # Eyes
        eye = max(2, size // 25)

        draw.ellipse(
            (
                cx - size * 0.11,
                size * 0.34,
                cx - size * 0.11 + eye,
                size * 0.34 + eye
            ),
            fill="#17202A"
        )

        draw.ellipse(
            (
                cx + size * 0.08,
                size * 0.34,
                cx + size * 0.08 + eye,
                size * 0.34 + eye
            ),
            fill="#17202A"
        )

        # Smile
        draw.arc(
            (
                cx - size * 0.09,
                size * 0.39,
                cx + size * 0.09,
                size * 0.50
            ),
            10,
            165,
            fill="#8C4C4C",
            width=max(1, size // 35)
        )

        # Clothes
        draw.rounded_rectangle(
            (
                cx - size * 0.31,
                size * 0.50,
                cx + size * 0.31,
                size * 1.02
            ),
            radius=int(size * 0.18),
            fill=shirt
        )

        # Convert to circle.
        result = self.circular_photo(img, size)

        self.avatar_cache[key] = result
        return result

    def update_preview(self):
        if (
            self.selected_index is not None
            and 0 <= self.selected_index < len(self.students)
        ):
            student = self.students[self.selected_index]

            picture = self.create_avatar(
                student.get("name", "Student"),
                115,
                self.selected_index,
                student.get("photo", "")
            )
        else:
            picture = self.create_avatar(
                "Student",
                115,
                0
            )

        self.preview.config(image=picture)
        self.preview.image = picture

    # ========================================================
    # SELECT STUDENT
    # ========================================================

    def select_student(self, event=None):
        selected = self.tree.selection()

        if not selected:
            return

        try:
            index = int(selected[0])
        except ValueError:
            return

        self.edit_by_index(index)

    # ========================================================
    # CHOOSE PICTURE
    # ========================================================

    def choose_picture(self):
        """
        User can choose ANY supported picture from any folder.
        The picture is copied into student_photos and linked to
        the student record when Add/Update is pressed.
        """
        path = filedialog.askopenfilename(
            title="Choose Student Picture",
            filetypes=[
                (
                    "Image Files",
                    "*.png *.jpg *.jpeg *.webp *.bmp"
                ),
                ("All Files", "*.*")
            ]
        )

        if not path:
            return

        try:
            extension = os.path.splitext(path)[1].lower()

            allowed = (
                ".png", ".jpg", ".jpeg",
                ".webp", ".bmp"
            )

            if extension not in allowed:
                raise ValueError(
                    "Please choose PNG, JPG, JPEG, WEBP or BMP."
                )

            filename = (
                "student_"
                + datetime.now().strftime("%Y%m%d%H%M%S%f")
                + extension
            )

            destination = os.path.join(PHOTO_DIR, filename)
            relative_path = os.path.join(
                PHOTO_DIR_NAME, filename
            )

            os.makedirs(PHOTO_DIR, exist_ok=True)
            shutil.copy2(path, destination)

            self.photo_path = relative_path

            image = Image.open(destination)
            photo = self.circular_photo(image, 115)

            self.preview.config(image=photo)
            self.preview.image = photo

            messagebox.showinfo(
                "Picture Selected",
                "Picture selected successfully!\n\n"
                "Now click 'Add Student' or 'Update' to save it."
            )

        except Exception as error:
            messagebox.showerror(
                "Picture Error",
                str(error)
            )

    # ========================================================
    # VALIDATION
    # ========================================================

    def validate_form(self):
        name = self.name_var.get().strip()
        roll = self.roll_var.get().strip()
        age = self.age_var.get().strip()
        email = self.email_var.get().strip()
        department = self.department_var.get().strip()
        marks_text = self.marks_var.get().strip()

        if not name:
            messagebox.showwarning(
                "Missing Data",
                "Please enter student name."
            )
            return False

        if not roll:
            messagebox.showwarning(
                "Missing Data",
                "Please enter roll number."
            )
            return False

        if not age:
            messagebox.showwarning(
                "Missing Data",
                "Please enter age."
            )
            return False

        try:
            age_value = int(age)
            if age_value < 1 or age_value > 100:
                raise ValueError
        except ValueError:
            messagebox.showwarning(
                "Invalid Age",
                "Age must be a number between 1 and 100."
            )
            return False

        if not email:
            messagebox.showwarning(
                "Missing Data",
                "Please enter email."
            )
            return False

        if "@" not in email or "." not in email:
            messagebox.showwarning(
                "Invalid Email",
                "Please enter a valid email address."
            )
            return False

        if not department:
            messagebox.showwarning(
                "Missing Data",
                "Please select a department."
            )
            return False

        try:
            marks = float(marks_text)

            if marks < 0 or marks > 100:
                raise ValueError

        except ValueError:
            messagebox.showwarning(
                "Invalid Marks",
                "Marks must be between 0 and 100."
            )
            return False

        return True

    def make_student_record(self):
        return {
            "name": self.name_var.get().strip(),
            "roll": self.roll_var.get().strip(),
            "age": self.age_var.get().strip(),
            "email": self.email_var.get().strip(),
            "department": self.department_var.get().strip(),
            "marks": float(self.marks_var.get()),
            "photo": self.photo_path
        }

    # ========================================================
    # ADD STUDENT
    # ========================================================

    def add_student(self):
        if not self.validate_form():
            return

        roll = self.roll_var.get().strip()

        if any(
            str(student.get("roll", "")) == roll
            for student in self.students
        ):
            messagebox.showerror(
                "Duplicate Roll Number",
                "This roll number already exists."
            )
            return

        self.students.append(self.make_student_record())
        self.selected_index = len(self.students) - 1

        if save_students(self.students):
            self.refresh_table()

            messagebox.showinfo(
                "Success",
                "Student added successfully! ✓\n\n"
                "Student information and picture have been saved."
            )

    # ========================================================
    # UPDATE
    # ========================================================

    def update_student(self):
        if self.selected_index is None:
            messagebox.showwarning(
                "Select Student",
                "Select a student from the table first."
            )
            return

        if not self.validate_form():
            return

        current_roll = self.roll_var.get().strip()

        for index, student in enumerate(self.students):
            if (
                index != self.selected_index
                and str(student.get("roll", "")) == current_roll
            ):
                messagebox.showerror(
                    "Duplicate Roll Number",
                    "This roll number belongs to another student."
                )
                return

        self.students[self.selected_index] = self.make_student_record()

        if save_students(self.students):
            self.refresh_table()

            messagebox.showinfo(
                "Updated",
                "Student updated successfully! ✓"
            )

    # ========================================================
    # DELETE
    # ========================================================

    def delete_student(self):
        if self.selected_index is None:
            messagebox.showwarning(
                "Select Student",
                "Select a student from the table first."
            )
            return

        self.delete_by_index(self.selected_index)

    # ========================================================
    # CLEAR
    # ========================================================

    def clear_form(self):
        self.selected_index = None
        self.photo_path = ""

        self.name_var.set("")
        self.roll_var.set("")
        self.age_var.set("")
        self.email_var.set("")
        self.department_var.set("")
        self.marks_var.set("")

        if hasattr(self, "tree"):
            self.tree.selection_remove(self.tree.selection())

        self.update_preview()

    def show_all(self):
        self.search_var.set("")
        self.refresh_table()

    # ========================================================
    # NAVIGATION
    # ========================================================

    def navigation(self, page):
        if page == "Dashboard":
            self.canvas.yview_moveto(0)
            messagebox.showinfo(
                "Dashboard",
                "Dashboard shows:\n\n"
                "• Total students\n"
                "• Average marks\n"
                "• Highest marks\n"
                "• Number of departments\n\n"
                "All numbers update automatically."
            )

        elif page == "All Students":
            self.canvas.yview_moveto(0.20)
            messagebox.showinfo(
                "All Students",
                f"There are currently {len(self.students)} students "
                "registered in the system.\n\n"
                "Click any student to edit their information."
            )

        elif page == "Add Student":
            self.canvas.yview_moveto(0.15)
            self.clear_form()
            self.name_entry.focus_set()

        elif page == "Search Student":
            self.canvas.yview_moveto(0.20)
            self.search_var.set("")
            self.refresh_table()
            messagebox.showinfo(
                "Search Student",
                "Type a name, roll number, age, email or department "
                "in the search box, then press Search."
            )

        elif page == "Statistics":
            self.show_statistics()

        elif page == "Backup Data":
            self.backup_data()

        elif page == "Save Data":
            self.save_data()

        elif page == "Settings":
            messagebox.showinfo(
                "Settings",
                "STUDENT MANAGEMENT SYSTEM SETTINGS\n\n"
                "✓ Automatic saving: ON\n"
                "✓ Circular student pictures: ON\n"
                "✓ Picture formats: PNG, JPG, JPEG, WEBP, BMP\n\n"
                f"Data file:\n{DATA_FILE}\n\n"
                f"Picture folder:\n{PHOTO_DIR}\n\n"
                "Every Add, Update and Delete operation is saved "
                "automatically."
            )

        elif page == "About":
            messagebox.showinfo(
                "About",
                f"{APP_TITLE}\n\n"
                f"Version {VERSION}\n\n"
                "A desktop student management application.\n\n"
                "Built with:\n"
                "• Python\n"
                "• Tkinter\n"
                "• Pillow\n"
                "• JSON data storage\n\n"
                "You can add unlimited students and choose "
                "your own pictures."
            )

    # ========================================================
    # STATISTICS
    # ========================================================

    def show_statistics(self):
        total = len(self.students)
        marks = []

        for student in self.students:
            try:
                marks.append(float(student.get("marks", 0)))
            except (TypeError, ValueError):
                pass

        average = sum(marks) / len(marks) if marks else 0
        highest = max(marks, default=0)
        lowest = min(marks, default=0)

        departments = sorted({
            student.get("department", "")
            for student in self.students
            if student.get("department", "")
        })

        messagebox.showinfo(
            "Statistics",
            f"Total Students: {total}\n"
            f"Average Marks: {average:.2f}\n"
            f"Highest Marks: {highest:g}\n"
            f"Lowest Marks: {lowest:g}\n\n"
            f"Departments ({len(departments)}):\n"
            + "\n".join(f"• {d}" for d in departments)
        )

    # ========================================================
    # SAVE
    # ========================================================

    def save_data(self):
        if save_students(self.students):
            self.updated_label.config(
                text="  Saved: "
                + datetime.now().strftime(
                    "%d-%b-%Y %I:%M:%S %p"
                )
            )

            messagebox.showinfo(
                "Save Data",
                "All student data and picture paths "
                "have been saved successfully! ✓"
            )

    # ========================================================
    # BACKUP
    # ========================================================

    def backup_data(self):
        path = filedialog.asksaveasfilename(
            title="Save Student Backup",
            defaultextension=".json",
            filetypes=[("JSON File", "*.json")],
            initialfile="students_backup.json"
        )

        if not path:
            return

        try:
            with open(path, "w", encoding="utf-8") as file:
                json.dump(
                    self.students,
                    file,
                    indent=2,
                    ensure_ascii=False
                )

            messagebox.showinfo(
                "Backup Complete",
                "Student data backup saved successfully! ✓\n\n"
                "Note: student_photos is kept inside the application "
                "folder for the original pictures."
            )

        except Exception as error:
            messagebox.showerror(
                "Backup Error",
                str(error)
            )


# ============================================================
# START
# ============================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagementApp(root)
    root.mainloop()