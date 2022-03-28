import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import csv

font = 12
font_small = int(font*0.75)
pad_x = 10
pad_y = 10

file_day = "/home/pi/Documents/monitor/rest_day.csv"
file_night = "/home/pi/Documents/monitor/rest_night.csv"

list_rest_after = []

class RestSet():
    def gui_first(self):
        self.app = tk.Tk()
        self.app.title("休憩時間設定")

        frame_title = tk.Frame(self.app)
        frame_title.pack()
        title = tk.Label(frame_title, text="休憩時間設定", font=('', font))
        title.pack(padx=pad_x, pady=pad_y)

        self.radioValue = tk.IntVar()

        frame_radio = tk.Frame(self.app)
        frame_radio.pack()
        radio_day = tk.Radiobutton(frame_radio, text="日勤", variable=self.radioValue, value=0, font=('', font))
        radio_night = tk.Radiobutton(frame_radio, text="夜勤", variable=self.radioValue, value=1, font=('', font))
        button_read = tk.Button(frame_radio, text="読込", command=self.read, font=('', font_small))
        radio_day.pack(side=tk.LEFT, padx=pad_x, pady=pad_y)
        radio_night.pack(side=tk.LEFT, padx=pad_x, pady=pad_y)
        button_read.pack(side=tk.LEFT, padx=pad_x, pady=pad_y)

        self.app.mainloop()

    def read(self):
        self.list_rest_before = []
        self.value = self.radioValue.get()
        if self.value == 0:
            with open(file_day, encoding='utf-8', newline='') as f:
                csvreader = csv.reader(f)
                list = [row for row in csvreader]
        elif self.value ==1:
            with open(file_night, encoding='utf-8', newline='') as f:
                csvreader = csv.reader(f)
                list = [row for row in csvreader]

        for n in range(1, len(list)):
            for m in range(1, 3):
                self.list_rest_before.append(list[n][m])
        
        self.gui_main()

    def gui_main(self):
        self.root = tk.Toplevel()
        self.root.title("休憩時間登録")

        frame_title = tk.Frame(self.root)
        frame_title.pack()
        title = tk.Label(frame_title, text="休憩時間設定", font=('', font))
        button_set = tk.Button(frame_title, text="登録", command=self.set, font=('', font_small))
        title.pack(side=tk.LEFT, padx=pad_x, pady=pad_y)
        button_set.pack(side=tk.RIGHT, padx=pad_x, pady=pad_y)

        frame_table = tk.Frame(self.root)
        frame_table.pack()
        label_1 = tk.Label(frame_table, text="No.", font=('', font))
        label_2 = tk.Label(frame_table, text="開始.", font=('', font))
        label_3 = tk.Label(frame_table, text="", font=('', font))
        label_4 = tk.Label(frame_table, text="終了", font=('', font))
        label_no_1 = tk.Label(frame_table, text="1", font=('', font))
        label_no_2 = tk.Label(frame_table, text="2", font=('', font))
        label_no_3 = tk.Label(frame_table, text="3", font=('', font))
        label_no_4 = tk.Label(frame_table, text="4", font=('', font))
        label_no_5 = tk.Label(frame_table, text="5", font=('', font))
        label_no_6 = tk.Label(frame_table, text="6", font=('', font))
        self.entry_start_1 = tk.Entry(frame_table, font=('', font))
        self.entry_start_2 = tk.Entry(frame_table, font=('', font))
        self.entry_start_3 = tk.Entry(frame_table, font=('', font))
        self.entry_start_4 = tk.Entry(frame_table, font=('', font))
        self.entry_start_5 = tk.Entry(frame_table, font=('', font))
        self.entry_start_6 = tk.Entry(frame_table, font=('', font))
        label_symbol_1 = tk.Label(frame_table, text="～", font=('', font))
        label_symbol_2 = tk.Label(frame_table, text="～", font=('', font))
        label_symbol_3 = tk.Label(frame_table, text="～", font=('', font))
        label_symbol_4 = tk.Label(frame_table, text="～", font=('', font))
        label_symbol_5 = tk.Label(frame_table, text="～", font=('', font))
        label_symbol_6 = tk.Label(frame_table, text="～", font=('', font))
        self.entry_end_1 = tk.Entry(frame_table, font=('', font))
        self.entry_end_2 = tk.Entry(frame_table, font=('', font))
        self.entry_end_3 = tk.Entry(frame_table, font=('', font))
        self.entry_end_4 = tk.Entry(frame_table, font=('', font))
        self.entry_end_5 = tk.Entry(frame_table, font=('', font))
        self.entry_end_6 = tk.Entry(frame_table, font=('', font))
        label_1.grid(column=0, row=0, padx=pad_x, pady=pad_y)
        label_2.grid(column=1, row=0, padx=pad_x, pady=pad_y)
        label_3.grid(column=2, row=0, padx=pad_x, pady=pad_y)
        label_4.grid(column=3, row=0, padx=pad_x, pady=pad_y)
        label_no_1.grid(column=0, row=1, padx=pad_x, pady=pad_y)
        label_no_2.grid(column=0, row=2, padx=pad_x, pady=pad_y)
        label_no_3.grid(column=0, row=3, padx=pad_x, pady=pad_y)
        label_no_4.grid(column=0, row=4, padx=pad_x, pady=pad_y)
        label_no_5.grid(column=0, row=5, padx=pad_x, pady=pad_y)
        label_no_6.grid(column=0, row=6, padx=pad_x, pady=pad_y)
        self.entry_start_1.grid(column=1, row=1, padx=pad_x, pady=pad_y)
        self.entry_start_2.grid(column=1, row=2, padx=pad_x, pady=pad_y)
        self.entry_start_3.grid(column=1, row=3, padx=pad_x, pady=pad_y)
        self.entry_start_4.grid(column=1, row=4, padx=pad_x, pady=pad_y)
        self.entry_start_5.grid(column=1, row=5, padx=pad_x, pady=pad_y)
        self.entry_start_6.grid(column=1, row=6, padx=pad_x, pady=pad_y)
        label_symbol_1.grid(column=2, row=1, padx=pad_x, pady=pad_y)
        label_symbol_2.grid(column=2, row=2, padx=pad_x, pady=pad_y)
        label_symbol_3.grid(column=2, row=3, padx=pad_x, pady=pad_y)
        label_symbol_4.grid(column=2, row=4, padx=pad_x, pady=pad_y)
        label_symbol_5.grid(column=2, row=5, padx=pad_x, pady=pad_y)
        label_symbol_6.grid(column=2, row=6, padx=pad_x, pady=pad_y)
        self.entry_end_1.grid(column=3, row=1, padx=pad_x, pady=pad_y)
        self.entry_end_2.grid(column=3, row=2, padx=pad_x, pady=pad_y)
        self.entry_end_3.grid(column=3, row=3, padx=pad_x, pady=pad_y)
        self.entry_end_4.grid(column=3, row=4, padx=pad_x, pady=pad_y)
        self.entry_end_5.grid(column=3, row=5, padx=pad_x, pady=pad_y)
        self.entry_end_6.grid(column=3, row=6, padx=pad_x, pady=pad_y)
        self.entry_start_1.insert(tk.END, self.list_rest_before[0])
        self.entry_start_2.insert(tk.END, self.list_rest_before[2])
        self.entry_start_3.insert(tk.END, self.list_rest_before[4])
        self.entry_start_4.insert(tk.END, self.list_rest_before[6])
        self.entry_start_5.insert(tk.END, self.list_rest_before[8])
        self.entry_start_6.insert(tk.END, self.list_rest_before[10])
        self.entry_end_1.insert(tk.END, self.list_rest_before[1])
        self.entry_end_2.insert(tk.END, self.list_rest_before[3])
        self.entry_end_3.insert(tk.END, self.list_rest_before[5])
        self.entry_end_4.insert(tk.END, self.list_rest_before[7])
        self.entry_end_5.insert(tk.END, self.list_rest_before[9])
        self.entry_end_6.insert(tk.END, self.list_rest_before[11])

    def set(self):
        if self.value == 0:
            list_rest_after.append(["No", "day start", "day end"])
        elif self.value == 1:
            list_rest_after.append(["No", "night start", "night end"])

        list_temp = []
        list_temp.append("1")
        i = self.entry_start_1.get()
        i = i.translate(str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)}))
        list_temp.append(i)
        i = self.entry_end_1.get()
        i = i.translate(str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)}))
        list_temp.append(i)
        list_rest_after.append(list_temp)

        list_temp = []
        list_temp.append("2")
        i = self.entry_start_2.get()
        i = i.translate(str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)}))
        list_temp.append(i)
        i = self.entry_end_2.get()
        i = i.translate(str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)}))
        list_temp.append(i)
        list_rest_after.append(list_temp)

        list_temp = []
        list_temp.append("3")
        i = self.entry_start_3.get()
        i = i.translate(str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)}))
        list_temp.append(i)
        i = self.entry_end_3.get()
        i = i.translate(str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)}))
        list_temp.append(i)
        list_rest_after.append(list_temp)

        list_temp = []
        list_temp.append("4")
        i = self.entry_start_4.get()
        i = i.translate(str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)}))
        list_temp.append(i)
        i = self.entry_end_4.get()
        i = i.translate(str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)}))
        list_temp.append(i)
        list_rest_after.append(list_temp)

        list_temp = []
        list_temp.append("5")
        i = self.entry_start_5.get()
        i = i.translate(str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)}))
        list_temp.append(i)
        i = self.entry_end_5.get()
        i = i.translate(str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)}))
        list_temp.append(i)
        list_rest_after.append(list_temp)

        list_temp = []
        list_temp.append("6")
        i = self.entry_start_6.get()
        i = i.translate(str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)}))
        list_temp.append(i)
        i = self.entry_end_6.get()
        i = i.translate(str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)}))
        list_temp.append(i)
        list_rest_after.append(list_temp)
        
        if self.value == 0:
            with open(file_day, 'w', newline="") as f:
                writer = csv.writer(f)
                writer.writerows(list_rest_after)        
        elif self.value == 1:
            with open(file_night, 'w', newline="") as f:
                writer = csv.writer(f)
                writer.writerows(list_rest_after)

        self.root.destroy()
        self.app.destroy()

if __name__ == '__main__':
    restset = RestSet()
    restset.gui_first()
