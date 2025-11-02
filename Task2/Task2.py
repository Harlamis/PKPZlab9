import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from collections import deque
import os

platoon1_deque = deque()
platoon2_deque = deque()
updated_platoon1_deque = deque()

def load_files():
    global platoon1_deque, platoon2_deque
    
    file_path1 = filedialog.askopenfilename(
        title="Оберіть файл для 1-го взводу",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        initialdir=os.getcwd()
    )
    
    if not file_path1:
        return

    file_path2 = filedialog.askopenfilename(
        title="Оберіть файл для 2-го взводу",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        initialdir=os.getcwd()
    )
    
    if not file_path2:
        return

    try:
        with open(file_path1, 'r', encoding='utf-8') as f:
            content = f.read()
            platoon1_deque = deque(name for name in content.split() if name.strip())
            
        with open(file_path2, 'r', encoding='utf-8') as f:
            content = f.read()
            platoon2_deque = deque(name for name in content.split() if name.strip())

        update_listbox_ui(listbox_p1_initial, platoon1_deque)
        update_listbox_ui(listbox_p2_initial, platoon2_deque)
        listbox_p1_updated.delete(0, tk.END)

        status_var.set(f"Завантажено: Взвод 1 ({len(platoon1_deque)}), Взвод 2 ({len(platoon2_deque)})")
        process_button.config(state=tk.NORMAL)
        
    except FileNotFoundError:
        messagebox.showerror("Помилка", "Файл не знайдено.")
    except Exception as e:
        messagebox.showerror("Помилка читання", f"Не вдалося прочитати файл: {e}")

def process_lists():
    global updated_platoon1_deque
    
    try:
        m = int(spin_m_var.get())
        if m < 0:
            raise ValueError("Число 'm' не може бути від'ємним")
    except ValueError as e:
        messagebox.showerror("Помилка вводу", f"Будь ласка, введіть коректне число 'm'.\n({e})")
        return

    if not platoon1_deque or not platoon2_deque:
        messagebox.showwarning("Брак даних", "Списки взводів порожні. Будь ласка, завантажте файли.")
        return

    updated_platoon1_deque = deque(platoon1_deque)

    removed_count = 0
    for _ in range(m):
        if updated_platoon1_deque:
            updated_platoon1_deque.popleft()
            removed_count += 1
        else:
            break

    platoon2_list_view = list(platoon2_deque)
    len_p2 = len(platoon2_list_view)

    if len_p2 == 0:
        status_var.set(f"Взвод 2 порожній. Видалено {removed_count}, нікого додати.")
    else:
        for i in range(m):
            soldier_to_add = platoon2_list_view[i % len_p2]
            updated_platoon1_deque.append(soldier_to_add)
        
        status_var.set(f"Видалено {removed_count} (зі взводу 1). Додано {m} (зі взводу 2).")

    update_listbox_ui(listbox_p1_updated, updated_platoon1_deque)
    save_button.config(state=tk.NORMAL)

def save_file():
    if not updated_platoon1_deque:
        messagebox.showwarning("Нема чого зберігати", "Список оновленого взводу порожній.")
        return

    file_path = filedialog.asksaveasfilename(
        title="Зберегти оновлений 1-й взвод",
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        initialfile="platoon1_updated.txt"
    )

    if not file_path:
        return

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            for soldier in updated_platoon1_deque:
                f.write(f"{soldier}\n")
        status_var.set(f"Оновлений список збережено у {file_path}")
    except Exception as e:
        messagebox.showerror("Помилка збереження", f"Не вдалося зберегти файл: {e}")

def update_listbox_ui(listbox: tk.Listbox, data: deque):
    listbox.delete(0, tk.END)
    for item in data:
        listbox.insert(tk.END, item)

root = tk.Tk()
root.title("Менеджер ротації взводів")
root.geometry("750x450")
controls_frame = ttk.Frame(root, padding="10")
controls_frame.pack(fill='x')
load_button = ttk.Button(controls_frame, text="Завантажити списки (2 файли)", command=load_files)
load_button.pack(side=tk.LEFT, padx=5, pady=5)
ttk.Label(controls_frame, text="Солдатів завершило контракт (m):").pack(side=tk.LEFT, padx=(20, 5))
spin_m_var = tk.StringVar(value="1")
spin_m = ttk.Spinbox(controls_frame, from_=0, to=100, textvariable=spin_m_var, width=5)
spin_m.pack(side=tk.LEFT, padx=5)
process_button = ttk.Button(controls_frame, text="Провести ротацію", command=process_lists, state=tk.DISABLED)
process_button.pack(side=tk.LEFT, padx=5)
save_button = ttk.Button(controls_frame, text="Зберегти результат", command=save_file, state=tk.DISABLED)
save_button.pack(side=tk.RIGHT, padx=5)
lists_frame = ttk.Frame(root, padding="10")
lists_frame.pack(fill='both', expand=True)
lists_frame.columnconfigure(0, weight=1)
lists_frame.columnconfigure(1, weight=1)
lists_frame.columnconfigure(2, weight=1)
lists_frame.rowconfigure(1, weight=1)
ttk.Label(lists_frame, text="Взвод 1 (Початковий)", font=("Arial", 12, "bold")).grid(row=0, column=0, pady=5)
listbox_p1_initial_frame = ttk.Frame(lists_frame)
listbox_p1_initial_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
scrollbar_p1 = ttk.Scrollbar(listbox_p1_initial_frame, orient=tk.VERTICAL)
listbox_p1_initial = tk.Listbox(listbox_p1_initial_frame, yscrollcommand=scrollbar_p1.set, exportselection=False)
scrollbar_p1.config(command=listbox_p1_initial.yview)
scrollbar_p1.pack(side=tk.RIGHT, fill=tk.Y)
listbox_p1_initial.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
ttk.Label(lists_frame, text="Взвод 2 (Донор)", font=("Arial", 12, "bold")).grid(row=0, column=1, pady=5)
listbox_p2_initial_frame = ttk.Frame(lists_frame)
listbox_p2_initial_frame.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
scrollbar_p2 = ttk.Scrollbar(listbox_p2_initial_frame, orient=tk.VERTICAL)
listbox_p2_initial = tk.Listbox(listbox_p2_initial_frame, yscrollcommand=scrollbar_p2.set, exportselection=False)
scrollbar_p2.config(command=listbox_p2_initial.yview)
scrollbar_p2.pack(side=tk.RIGHT, fill=tk.Y)
listbox_p2_initial.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
ttk.Label(lists_frame, text="Взвод 1 (Оновлений)", font=("Arial", 12, "bold")).grid(row=0, column=2, pady=5)
listbox_p1_updated_frame = ttk.Frame(lists_frame)
listbox_p1_updated_frame.grid(row=1, column=2, padx=5, pady=5, sticky="nsew")
scrollbar_p3 = ttk.Scrollbar(listbox_p1_updated_frame, orient=tk.VERTICAL)
listbox_p1_updated = tk.Listbox(listbox_p1_updated_frame, yscrollcommand=scrollbar_p3.set, exportselection=False, bg="#f0f8ff")
scrollbar_p3.config(command=listbox_p1_updated.yview)
scrollbar_p3.pack(side=tk.RIGHT, fill=tk.Y)
listbox_p1_updated.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
status_var = tk.StringVar()
status_bar = ttk.Label(root, textvariable=status_var, relief=tk.SUNKEN, anchor=tk.W, padding="5")
status_bar.pack(side=tk.BOTTOM, fill='x')
status_var.set("Готово. Будь ласка, завантажте файли взводів.")
root.mainloop()

