import json
import os
import tkinter as tk
import tkinter.font as tkfont
from tkinter import messagebox

import ttkbootstrap as ttk
import requests


DATA_FILE = "animewatch_data.json"


class AnimeWatchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AnimeWatch — Milestone 3")
        self.root.geometry("860x520")

        self.style = ttk.Style()
        self.shows = []
        self.last_removed = None

        self.app_font = tkfont.nametofont("TkDefaultFont")
        self.app_font.configure(size=11)

        self.load_data()
        self.build_ui()
        self.refresh_listbox()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, dict):
                    self.shows = data.get("watchlist", [])
                elif isinstance(data, list):
                    self.shows = data
                else:
                    self.shows = []
            except Exception:
                self.shows = []
        else:
            self.shows = []

    def save_data(self):
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump({"watchlist": self.shows}, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def build_ui(self):
        self.banner = ttk.Label(
            self.root,
            text="track, organize, and get gentle suggestions for what to watch next.",
            font=("Segoe UI", 14, "bold"),
            anchor="w",
        )
        self.banner.pack(fill="x", padx=16, pady=(12, 2))

        self.step_label = ttk.Label(
            self.root,
            text="steps: 1) add a show  2) mark episodes  3) manage your list",
            font=self.app_font,
            anchor="w",
        )
        self.step_label.pack(fill="x", padx=16, pady=(0, 2))

        self.cost_label = ttk.Label(
            self.root,
            text="no account • saved locally • changes apply instantly",
            font=self.app_font,
            anchor="w",
        )
        self.cost_label.pack(fill="x", padx=16, pady=(0, 8))

        self.input_frame = ttk.Frame(self.root)
        self.input_frame.pack(fill="x", padx=16)

        ttk.Label(self.input_frame, text="title:", font=self.app_font).grid(
            row=0, column=0, padx=(0, 6), pady=4, sticky="e"
        )
        self.title_entry = ttk.Entry(self.input_frame, width=28)
        self.title_entry.grid(row=0, column=1, padx=(0, 12), pady=4, sticky="w")

        ttk.Label(self.input_frame, text="total episodes:", font=self.app_font).grid(
            row=0, column=2, padx=(0, 6), pady=4, sticky="e"
        )
        self.total_entry = ttk.Entry(self.input_frame, width=10)
        self.total_entry.grid(row=0, column=3, padx=(0, 12), pady=4, sticky="w")

        self.add_btn = ttk.Button(
            self.input_frame, text="add to watchlist", command=self.add_show, bootstyle="success"
        )
        self.add_btn.grid(row=0, column=4, pady=4)

        self.title_entry.bind("<Return>", self.add_show_event)
        self.total_entry.bind("<Return>", self.add_show_event)

        self.mid = ttk.Frame(self.root)
        self.mid.pack(fill="both", expand=True, padx=16, pady=(10, 6))

        self.listbox = tk.Listbox(
            self.mid,
            height=11,
            activestyle="none",
            font=self.app_font,
        )
        self.listbox.pack(side="left", fill="both", expand=True)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)
        self.listbox.bind("<Double-Button-1>", self.mark_watched_event)

        self.scrollbar = ttk.Scrollbar(self.mid, orient="vertical", command=self.listbox.yview)
        self.scrollbar.pack(side="left", fill="y", padx=(0, 6))
        self.listbox.configure(yscrollcommand=self.scrollbar.set)

        self.btns = ttk.Frame(self.mid)
        self.btns.pack(side="right", fill="y")

        self.mark_btn = ttk.Button(
            self.btns, text="mark episode watched", command=self.mark_watched, bootstyle="primary"
        )
        self.mark_btn.pack(fill="x", pady=4)

        self.remove_btn = ttk.Button(
            self.btns, text="remove", command=self.remove_show, bootstyle="danger"
        )
        self.remove_btn.pack(fill="x", pady=4)

        self.undo_btn = ttk.Button(
            self.btns, text="undo remove", command=self.undo_remove, bootstyle="secondary"
        )
        self.undo_btn.pack(fill="x", pady=4)

        self.toggle_btn = ttk.Button(
            self.root, text="toggle details", command=self.toggle_details, bootstyle="secondary"
        )
        self.toggle_btn.pack(padx=16, pady=(0, 6), anchor="w")

        self.details_frame = ttk.Frame(self.root)

        self.details_var = tk.StringVar(value="details: (select a show)")
        self.details_label = ttk.Label(
            self.details_frame, textvariable=self.details_var, justify="left", font=self.app_font
        )
        self.details_label.pack(fill="x")

        self.details_box = tk.Text(self.details_frame, height=7, font=self.app_font, wrap="word")
        self.details_box.pack(fill="both", pady=(4, 4))

        self.ms_frame = ttk.Frame(self.details_frame)
        self.ms_frame.pack(fill="x", pady=(2, 4))

        self.time_btn = ttk.Button(
            self.ms_frame, text="get time", command=self.ms_time, bootstyle="info-outline"
        )
        self.time_btn.pack(side="left", padx=4)

        self.fact_btn = ttk.Button(
            self.ms_frame, text="anime fact", command=self.ms_fact, bootstyle="info-outline"
        )
        self.fact_btn.pack(side="left", padx=4)

        self.motivate_btn = ttk.Button(
            self.ms_frame, text="motivate me", command=self.ms_motivate, bootstyle="info-outline"
        )
        self.motivate_btn.pack(side="left", padx=4)

        self.suggest_btn = ttk.Button(
            self.ms_frame, text="suggest", command=self.ms_suggest, bootstyle="info-outline"
        )
        self.suggest_btn.pack(side="left", padx=4)

        self.acc = ttk.Frame(self.root)
        self.acc.pack(fill="x", padx=16, pady=(8, 10))

        self.theme_var = tk.IntVar(value=0)
        self.theme_check = ttk.Checkbutton(
            self.acc,
            text="dark mode",
            variable=self.theme_var,
            command=self.toggle_theme,
            bootstyle="round-toggle",
        )
        self.theme_check.pack(side="left", padx=(0, 10))

        self.smaller_btn = ttk.Button(self.acc, text="A−", command=self.smaller_font, width=3)
        self.smaller_btn.pack(side="left")

        self.bigger_btn = ttk.Button(self.acc, text="A+", command=self.bigger_font, width=3)
        self.bigger_btn.pack(side="left", padx=(4, 0))

    def refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for s in self.shows:
            self.listbox.insert(
                tk.END,
                f'{s["title"]} — progress: {s["watched"]}/{s["total"]}',
            )

    def add_show_event(self, event):
        self.add_show()

    def add_show(self):
        title = self.title_entry.get().strip()
        total_text = self.total_entry.get().strip()

        if not title:
            messagebox.showinfo("note", "enter a show title first.")
            return
        if not total_text.isdigit() or int(total_text) <= 0:
            messagebox.showinfo("note", "total episodes must be a positive number.")
            return

        total = int(total_text)

        for s in self.shows:
            if s["title"].lower() == title.lower():
                messagebox.showinfo("note", "that show is already in your watchlist.")
                return

        self.shows.append({"title": title, "total": total, "watched": 0})
        self.save_data()
        self.refresh_listbox()
        self.title_entry.delete(0, tk.END)
        self.total_entry.delete(0, tk.END)

    def remove_show(self):
        idxs = self.listbox.curselection()
        if not idxs:
            messagebox.showinfo("note", "select a show first.")
            return

        i = idxs[0]
        s = self.shows[i]

        ok = messagebox.askyesno("confirm remove", f'remove "{s["title"]}" from watchlist?')
        if not ok:
            return

        self.last_removed = self.shows.pop(i)
        self.save_data()
        self.refresh_listbox()

    def undo_remove(self):
        if self.last_removed is None:
            messagebox.showinfo("note", "nothing to undo.")
            return
        self.shows.append(self.last_removed)
        self.last_removed = None
        self.save_data()
        self.refresh_listbox()

    def mark_watched_event(self, event):
        self.mark_watched()

    def mark_watched(self):
        idxs = self.listbox.curselection()
        if not idxs:
            messagebox.showinfo("note", "select a show first.")
            return
        i = idxs[0]
        s = self.shows[i]

        if s["watched"] >= s["total"]:
            messagebox.showinfo("note", "you already finished this show.")
            return

        s["watched"] += 1
        self.save_data()
        self.refresh_listbox()

    def toggle_details(self):
        if self.details_frame.winfo_ismapped():
            self.details_frame.pack_forget()
        else:
            self.details_frame.pack(fill="both", padx=16, pady=(0, 10))

    def on_select(self, event):
        idxs = self.listbox.curselection()
        if not idxs:
            self.details_var.set("details: (select a show)")
            return
        i = idxs[0]
        s = self.shows[i]
        percent = int((s["watched"] / s["total"]) * 100) if s["total"] > 0 else 0
        self.details_var.set(
            f'title: {s["title"]}\n'
            f'episodes watched: {s["watched"]}/{s["total"]}\n'
            f'progress: {percent}%'
        )

    def toggle_theme(self):
        if self.theme_var.get() == 1:
            self.style.theme_use("darkly")
        else:
            self.style.theme_use("flatly")

    def bigger_font(self):
        size = self.app_font["size"]
        self.app_font.configure(size=size + 2)

    def smaller_font(self):
        size = self.app_font["size"]
        if size > 8:
            self.app_font.configure(size=size - 2)

    def ms_time(self):
        try:
            r = requests.get("http://127.0.0.1:5001/time", timeout=1.0)
            self.details_box.insert(tk.END, f"\n\ntime: {r.text}")
        except Exception:
            self.details_box.insert(tk.END, "\n\ntime: (time microservice offline)")

    def ms_fact(self):
        try:
            r = requests.get("http://127.0.0.1:5002/fact", timeout=1.0)
            self.details_box.insert(tk.END, f"\nanime fact: {r.text}")
        except Exception:
            self.details_box.insert(tk.END, "\nanime fact: (fact microservice offline)")

    def ms_motivate(self):
        try:
            r = requests.get("http://127.0.0.1:5003/motivate", timeout=1.0)
            self.details_box.insert(tk.END, f"\nmotivation: {r.text}")
        except Exception:
            self.details_box.insert(tk.END, "\nmotivation: (motivation microservice offline)")

    def ms_suggest(self):
        try:
            r = requests.get("http://127.0.0.1:5004/suggest", timeout=1.0)
            self.details_box.insert(tk.END, f"\nsuggestion: {r.text}")
        except Exception:
            self.details_box.insert(tk.END, "\nsuggestion: (suggestion microservice offline)")


if __name__ == "__main__":
    app = ttk.Window(themename="flatly")
    AnimeWatchApp(app)
    app.mainloop()
