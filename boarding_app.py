import tkinter as tk
from tkinter import ttk, simpledialog, messagebox, filedialog
import calendar
import csv
import datetime

class BoardingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Animal Boarding Calendar")
        self.geometry("1000x600")

        # initial cages
        self.cages = ["Cage1", "Cage2", "Cage3", "Cage4"]
        self.data = []  # list of dicts representing rows

        self.create_widgets()

    def create_widgets(self):
        top = tk.Frame(self)
        top.pack(side=tk.TOP, fill=tk.X)

        tk.Button(top, text="Add Month", command=self.add_month).pack(side=tk.LEFT)
        tk.Button(top, text="Add Cage", command=self.add_cage).pack(side=tk.LEFT)
        tk.Button(top, text="Join Cages", command=self.join_cages).pack(side=tk.LEFT)
        tk.Button(top, text="Split Cage", command=self.split_cage).pack(side=tk.LEFT)
        tk.Button(top, text="Book Stay", command=self.book_stay).pack(side=tk.LEFT)
        tk.Button(top, text="Save CSV", command=self.save_csv).pack(side=tk.LEFT)

        style = ttk.Style(self)
        style.configure("Treeview", borderwidth=1, relief="solid")
        style.configure("Treeview.Heading", borderwidth=1, relief="solid")
        self.tree = ttk.Treeview(self, columns=["Date", "Notes"] + self.cages, show="headings")
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<Double-1>", self.on_double_click)
        self.refresh_tree()

    def refresh_tree(self):
        self.tree.delete(*self.tree.get_children())
        cols = ["Date", "Notes"] + self.cages
        self.tree.configure(columns=cols)
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, stretch=True)

        for row in self.data:
            values = [row.get("Date", ""), row.get("Notes", "")] + [row.get(c, "") for c in self.cages]
            self.tree.insert("", tk.END, values=values)

    def add_month(self):
        month = simpledialog.askinteger("Month", "Enter month (1-12)")
        year = simpledialog.askinteger("Year", "Enter year")
        if not month or not year:
            return
        days = calendar.monthrange(year, month)[1]
        for d in range(1, days + 1):
            date_str = f"{year}-{month:02d}-{d:02d}"
            row = {"Date": date_str, "Notes": ""}
            for c in self.cages:
                row[c] = ""
            self.data.append(row)
        self.refresh_tree()

    def add_cage(self):
        name = simpledialog.askstring("Add Cage", "Cage name")
        if not name:
            return
        self.cages.append(name)
        for row in self.data:
            row[name] = ""
        self.refresh_tree()

    def book_stay(self):
        cage = simpledialog.askstring("Book Stay", "Cage name")
        if not cage or cage not in self.cages:
            messagebox.showerror("Error", "Cage name not found")
            return
        animal = simpledialog.askstring("Book Stay", "Animal name")
        start = simpledialog.askstring("Book Stay", "Start date YYYY-MM-DD")
        end = simpledialog.askstring("Book Stay", "End date YYYY-MM-DD")
        if not animal or not start or not end:
            return
        try:
            start_date = datetime.datetime.strptime(start, "%Y-%m-%d").date()
            end_date = datetime.datetime.strptime(end, "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("Error", "Dates must be YYYY-MM-DD")
            return
        if start_date > end_date:
            messagebox.showerror("Error", "Start date after end date")
            return
        for row in self.data:
            try:
                row_date = datetime.datetime.strptime(row["Date"], "%Y-%m-%d").date()
            except Exception:
                continue
            if start_date <= row_date <= end_date:
                row[cage] = animal
        self.refresh_tree()

    def on_double_click(self, event):
        item = self.tree.identify_row(event.y)
        col = self.tree.identify_column(event.x)
        if not item or not col:
            return
        col_index = int(col[1:]) - 1
        column_name = self.tree.cget("columns")[col_index]
        old_value = self.tree.set(item, column_name)
        new_value = simpledialog.askstring("Edit", f"Enter value for {column_name}", initialvalue=old_value)
        if new_value is None:
            return
        row_index = self.tree.index(item)
        self.data[row_index][column_name] = new_value
        self.refresh_tree()

    def join_cages(self):
        c1 = simpledialog.askstring("Join Cages", "First cage name")
        c2 = simpledialog.askstring("Join Cages", "Second cage name")
        if not c1 or not c2:
            return
        if c1 not in self.cages or c2 not in self.cages:
            messagebox.showerror("Error", "Cage names not found")
            return
        new_name = f"{c1}+{c2}"
        self.cages = [c for c in self.cages if c not in (c1, c2)]
        self.cages.append(new_name)
        for row in self.data:
            row[new_name] = (row.get(c1, "") + " " + row.get(c2, "")).strip()
            row.pop(c1, None)
            row.pop(c2, None)
        self.refresh_tree()

    def split_cage(self):
        cage = simpledialog.askstring("Split Cage", "Cage name to split")
        if not cage or cage not in self.cages or "+" not in cage:
            messagebox.showerror("Error", "Cage name invalid or not a joined cage")
            return
        parts = cage.split("+")
        self.cages.remove(cage)
        for p in parts:
            self.cages.append(p)
        for row in self.data:
            content = row.get(cage, "")
            words = content.split()
            for i, p in enumerate(parts):
                row[p] = words[i] if i < len(words) else ""
            row.pop(cage, None)
        self.refresh_tree()

    def save_csv(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if not path:
            return
        cols = ["Date", "Notes"] + self.cages
        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(cols)
            for row in self.data:
                writer.writerow([row.get(c, "") for c in cols])
        messagebox.showinfo("Saved", f"Data saved to {path}")

if __name__ == "__main__":
    app = BoardingApp()
    app.mainloop()
