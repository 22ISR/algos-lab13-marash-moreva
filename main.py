import tkinter as tk
from tkinter import ttk
import requests
import threading

def get_data():
    try:
        response = requests.get("https://kitek.ktkv.dev/songs.json")
        if response.status_code == 200:
            return response.json()
        else:
            print("Ошибка при получении данных")
            return []
    except Exception as e:
        print("Ошибка:", e)
        return []

def filter_data(query):
    query = query.lower()
    result = []
    for song in all_songs:
        if (query in song["track"].lower() or 
            query in song["artists"].lower() or 
            query in song["album"].lower()):
            result.append(song)
    return result

def update_table(data):
    for row in table.get_children():
        table.delete(row)
    for song in data:
        table.insert('', tk.END, values=(song["track"], song["artists"], song["album"], song["duration"], song["popularity"], song["date_added"]))

def on_search(*args):
    query = search_var.get()
    filtered = filter_data(query)
    update_table(filtered)

def sort_by(col_index, reverse=False):
    data = []
    for item in table.get_children():
        data.append((table.item(item)['values'], item))
    
    data.sort(key=lambda x: x[0][col_index], reverse=reverse)

    for index, (values, item) in enumerate(data):
        table.move(item, '', index)

    headings[col_index]['command'] = lambda: sort_by(col_index, not reverse)

def load_data():
    global all_songs
    all_songs = get_data()
    update_table(all_songs)

root = tk.Tk()
root.title("Картотека Spotify")
root.geometry("900x500")

search_var = tk.StringVar()
search_var.trace("w", on_search)
search_entry = ttk.Entry(root, textvariable=search_var, width=50)
search_entry.pack(pady=10)

columns = ("Название", "Исполнитель", "Альбом", "Длительность", "Популярность", "Дата добавления")
table = ttk.Treeview(root, columns=columns, show='headings')

headings = []
for i, col in enumerate(columns):
    table.heading(col, text=col, command=lambda c=i: sort_by(c, False))
    headings.append(table.heading(col))

table.column("Название", width=200)
table.column("Исполнитель", width=150)
table.column("Альбом", width=150)
table.column("Длительность", width=100, anchor=tk.CENTER)
table.column("Популярность", width=100, anchor=tk.CENTER)
table.column("Дата добавления", width=120, anchor=tk.CENTER)

table.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

all_songs = []
threading.Thread(target=load_data).start()

root.mainloop()