# // 20220207 新規作成　→　0212 l/r 仕様変更　→　end button 廃止
# // 20220215 編集中　→　0306調整/確認

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar, DateEntry
import pandas as pd
import datetime

font = 16
font_small = int(font * 0.75)
pad_x = 10
pad_y = 10
file = "/home/pi/Documents/monitor/indata_all.pkl"


def gui_refine():
    global root
    global combobox
    global entry_calender1
    global entry_calender2

    root = tk.Tk()
    root.title(u'検索画面')

    frame_hedder = tk.Frame(root)
    frame_hedder.pack()
    title = tk.Label(frame_hedder, text="検索画面", font=('', font))
    title.pack(side=tk.LEFT, padx=pad_x, pady=pad_y)

    frame_locate = tk.Frame(root)
    frame_locate.pack()
    entry_calender1 = DateEntry(frame_locate, locale='ja_JP', font=('', font_small), showweeknumbers=False)
    entry_calender1.pack(side=tk.LEFT, padx=pad_x, pady=pad_y)
    label_locate = tk.Label(frame_locate, text="～", font=('', font_small))
    label_locate.pack(side=tk.LEFT, padx=pad_x, pady=pad_y)
    entry_calender2 = DateEntry(frame_locate, locale='ja_JP', font=('', font_small), showweeknumbers=False)
    entry_calender2.pack(side=tk.LEFT, padx=pad_x, pady=pad_y)
 
    frame_button = tk.Frame(root)
    frame_button.pack()
    button = tk.Button(frame_button, text="検索", command=serch, font=('', font_small))
    button.pack(side=tk.LEFT, padx=pad_x, pady=pad_y)

    root.mainloop()

def serch():
    global serch_list

    df = pd.read_pickle(file)
    print(df)
    get_start = entry_calender1.get()
    get_end = entry_calender2.get()

    serch_start = datetime.datetime.strptime(get_start, '%Y/%m/%d').date()
    serch_end = datetime.datetime.strptime(get_end, '%Y/%m/%d').date() + datetime.timedelta(days=1)
    
    serch_list = []
    for i in daterange(serch_start, serch_end):
        df_refine = df[df.iloc[:, 1].dt.date == i]
        df_refine_l = df_refine[df_refine.iloc[:, 0] == "lh"]
        df_refine_r = df_refine[df_refine.iloc[:, 0] == "rh"]
        quantity_l = df_refine_l.shape[0]
        quantity_r = df_refine_r.shape[0]
        restTime = df_refine.iloc[:, 2].astype(int).sum()
        print(restTime)
        
        try:
            timeStart = df_refine.iat[0, 1].strftime('%H:%M')
            timeEnd = df_refine.iat[-1, 1].strftime('%H:%M')
            if quantity_l == "":
                quantity_l = 0
            elif quantity_r == "":
                quantity_r = 0
            average = round((((df_refine.iat[-1, 1] - df_refine.iat[0, 1]).total_seconds()) - restTime) / (quantity_l + quantity_r), 1)
        except IndexError:
            timeStart = ""
            timeEnd = ""
            average = ""

        serch_list.append([i, quantity_l, quantity_r, timeStart, timeEnd, average])
    
    gui_show()

def daterange(start, end):
    for n in range((end - start).days):
        yield start + datetime.timedelta(n)

def gui_show():
    global app

    app = tk.Toplevel()
    app.title(u'集計画面')
    
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("", font))
    style.configure("Treeview", font=("", font))

    frame_hedder = tk.Frame(app)
    frame_hedder.pack()
    label = tk.Label(frame_hedder, text="一覧", font=('', font))
    label.pack(side=tk.LEFT, padx=pad_x, pady=pad_y)

    frame_table = tk.Frame(app)
    frame_table.pack()
    column = ("day", "quantity_l", "quantity_r", "timeStart", "timeEnd", "average")
    tree = ttk.Treeview(frame_table, columns=column)
    tree.heading('#0', text='')
    tree.heading('day', text='日', anchor='w')
    tree.heading('quantity_l', text='LH（個）', anchor='w')
    tree.heading('quantity_r', text='RH（個）', anchor='w')
    tree.heading('timeStart', text='開始', anchor='w')
    tree.heading('timeEnd', text='終了', anchor='w')
    tree.heading('average', text='平均（秒）', anchor='w')
    tree.column('#0', width=0, stretch='no')
    tree.column('day', anchor='w', width=200)
    tree.column('quantity_l', anchor='w', width=100)
    tree.column('quantity_r', anchor='w', width=100)
    tree.column('timeStart', anchor='w', width=100)
    tree.column('timeEnd', anchor='w', width=100)
    tree.column('average', anchor='w', width=100)

    for i in serch_list:
        tree.insert(parent='', index='end', values=i)
    
    scrollbar = ttk.Scrollbar(frame_table, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)

    tree.pack(side=tk.LEFT, padx=pad_x, pady=pad_y)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=pad_x, pady=pad_y)

    app.mainloop()

def destroy_root():
    root.destroy()

def destroy_app():
    app.destroy()

if __name__ == "__main__":
    gui_refine()
