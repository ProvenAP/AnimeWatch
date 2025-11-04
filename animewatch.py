import json
import os
import tkinter as tk
import tkinter.font as tkfont
from tkinter import messagebox

DATA_FILE = "animewatch_data.json"

# simple in-memory store: list of shows
# each show: {"title": str, "total": int, "watched": int}
shows = []

# last removed item (for undo)
last_removed = None

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
        except:
            pass
    return []

def save_data():
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(shows, f, ensure_ascii=False, indent=2)
    except:
        pass

def refresh_listbox():
    listbox.delete(0, tk.END)
    for s in shows:
        listbox.insert(tk.END, f'{s["title"]} — Progress: {s["watched"]}/{s["total"]}')

def add_show(event=None):
    # event is for enter-key path (ih#7)
    title = title_entry.get().strip()
    total_text = total_entry.get().strip()

    if not title:
        messagebox.showinfo("note", "enter a show title first.")
        return
    if not total_text.isdigit() or int(total_text) <= 0:
        messagebox.showinfo("note", "total episodes must be a positive number.")
        return

    total = int(total_text)

    # if title exists, don’t duplicate
    for s in shows:
        if s["title"].lower() == title.lower():
            messagebox.showinfo("note", "that show is already in your watchlist.")
            return

    shows.append({"title": title, "total": total, "watched": 0})
    save_data()
    refresh_listbox()
    title_entry.delete(0, tk.END)
    total_entry.delete(0, tk.END)

def remove_show():
    global last_removed
    idx = listbox.curselection()
    if not idx:
        messagebox.showinfo("note", "select a show first.")
        return

    i = idx[0]
    s = shows[i]

    # ih#8: confirm before destructive action
    ok = messagebox.askyesno("confirm remove", f'remove "{s["title"]}" from watchlist?')
    if not ok:
        return

    last_removed = shows.pop(i)
    save_data()
    refresh_listbox()

def undo_remove():
    # ih#5: quick undo
    global last_removed
    if last_removed is None:
        messagebox.showinfo("note", "nothing to undo.")
        return
    shows.append(last_removed)
    last_removed = None
    save_data()
    refresh_listbox()

def mark_watched():
    idx = listbox.curselection()
    if not idx:
        messagebox.showinfo("note", "select a show first.")
        return
    i = idx[0]
    s = shows[i]

    if s["watched"] >= s["total"]:
        messagebox.showinfo("note", "you already finished this show.")
        return

    s["watched"] += 1
    save_data()
    refresh_listbox()

def toggle_details():
    # ih#3: let users choose how much info to see
    if details_frame.winfo_ismapped():
        details_frame.pack_forget()
    else:
        details_frame.pack(fill="x", padx=10, pady=(6, 10))

def on_select(event):
    # when you select a show, update the details area
    idxs = listbox.curselection()
    if not idxs:
        details_var.set("details: (select a show)")
        return
    i = idxs[0]
    s = shows[i]
    details_var.set(
        f'title: {s["title"]}\n'
        f'episodes watched: {s["watched"]}/{s["total"]}\n'
        f'progress: {int((s["watched"]/s["total"])*100)}%'
    )

def toggle_theme():
    # ih#7 alt approach + accessibility: theme change
    is_dark = theme_var.get() == 1
    bg = "#111" if is_dark else "#f5f5f5"
    fg = "#f5f5f5" if is_dark else "#111"
    for w in all_widgets:
        try:
            w.configure(bg=bg, fg=fg)
        except:
            # some widgets (e.g., listbox) have different config keys
            pass
    try:
        listbox.configure(bg=bg, fg=fg)
    except:
        pass
    root.configure(bg=bg)
    banner.configure(bg=bg, fg=fg)
    step_label.configure(bg=bg, fg=fg)
    cost_label.configure(bg=bg, fg=fg)
    details_frame.configure(bg=bg)
    details_label.configure(bg=bg, fg=fg)

def bigger_font():
    # accessibility: quick font bump
    size = app_font["size"]
    app_font.configure(size=size + 2)

def smaller_font():
    size = app_font["size"]
    if size > 8:
        app_font.configure(size=size - 2)

# ---------- UI ----------
root = tk.Tk()
root.title("AnimeWatch — Milestone #1")

# a shared font so we can bump size for accessibility
app_font = tkfont.nametofont("TkDefaultFont")
app_font.configure(size=11)

# banner (ih#1: benefits)
banner = tk.Label(root, text="track, organize, and get updates on your favorite anime.", font=app_font)
banner.pack(fill="x", padx=10, pady=(10, 2))

# step-by-step (ih#6)
step_label = tk.Label(root, text="steps: 1) add a show  2) mark episodes  3) manage your list", font=app_font)
step_label.pack(fill="x", padx=10, pady=(0, 6))

# costs (ih#2)
cost_label = tk.Label(root, text="no account • saved locally • changes apply instantly", font=app_font)
cost_label.pack(fill="x", padx=10, pady=(0, 10))

# input row: title + total episodes + add
input_frame = tk.Frame(root)
input_frame.pack(fill="x", padx=10)

tk.Label(input_frame, text="title:", font=app_font).grid(row=0, column=0, padx=(0,6), pady=4, sticky="e")
title_entry = tk.Entry(input_frame, width=28, font=app_font)
title_entry.grid(row=0, column=1, padx=(0,12), pady=4, sticky="w")

tk.Label(input_frame, text="total episodes:", font=app_font).grid(row=0, column=2, padx=(0,6), pady=4, sticky="e")
total_entry = tk.Entry(input_frame, width=8, font=app_font)
total_entry.grid(row=0, column=3, padx=(0,12), pady=4, sticky="w")

add_btn = tk.Button(input_frame, text="add to watchlist", command=add_show, font=app_font)
add_btn.grid(row=0, column=4, padx=(0,0), pady=4)

# ih#7: multiple ways — press Enter to add as well
title_entry.bind("<Return>", add_show)
total_entry.bind("<Return>", add_show)

# list + actions
mid = tk.Frame(root)
mid.pack(fill="both", expand=True, padx=10, pady=(10, 6))

listbox = tk.Listbox(mid, height=10, activestyle="none", font=app_font)
listbox.pack(side="left", fill="both", expand=True)
listbox.bind("<<ListboxSelect>>", on_select)

btns = tk.Frame(mid)
btns.pack(side="right", fill="y", padx=(10,0))
tk.Button(btns, text="mark episode watched", command=mark_watched, font=app_font).pack(fill="x", pady=4)
tk.Button(btns, text="remove", command=remove_show, font=app_font).pack(fill="x", pady=4)
tk.Button(btns, text="undo remove", command=undo_remove, font=app_font).pack(fill="x", pady=4)

# ih#3: optional details area (collapsible)
toggle = tk.Button(root, text="toggle details", command=toggle_details, font=app_font)
toggle.pack(padx=10, pady=(0,4), anchor="w")

details_frame = tk.Frame(root)
details_var = tk.StringVar(value="details: (select a show)")
details_label = tk.Label(details_frame, textvariable=details_var, justify="left", font=app_font)
details_label.pack(fill="x")

# accessibility controls (ih#4 familiar controls + alt approaches)
acc = tk.Frame(root)
acc.pack(fill="x", padx=10, pady=(8,10))
theme_var = tk.IntVar(value=0)
tk.Checkbutton(acc, text="dark mode", variable=theme_var, command=toggle_theme, font=app_font).pack(side="left", padx=(0,10))
tk.Button(acc, text="A−", command=smaller_font, font=app_font).pack(side="left")
tk.Button(acc, text="A+", command=bigger_font, font=app_font).pack(side="left")

# collect widgets for theme toggling
all_widgets = [w for w in root.winfo_children()] + [input_frame, mid, btns, acc]

# initial data
shows.extend(load_data())
refresh_listbox()

root.mainloop()
