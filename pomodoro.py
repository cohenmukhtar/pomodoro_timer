import time
import tkinter as tk
from tkinter import ttk, StringVar, messagebox
import threading
import numpy as np

# Initialize the main window
root = tk.Tk()
root.title("Stretchy Preferences")
root.geometry("400x400")

#####     SETTINGS TABS     #####

# Variables for radio buttons and checkboxes
language_var = StringVar(value="English")
start_on_login_var = tk.BooleanVar(value=False)
display_mode_var = StringVar(value="Window")
exercise_tips_var = tk.BooleanVar(value=True)
all_monitors_var = tk.BooleanVar(value=True)
idle_time_var = tk.BooleanVar(value=True)
dnd_mode_var = tk.BooleanVar(value=False)

tabControl = ttk.Notebook(root)
settings = ttk.Frame(tabControl)
schedules = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tab4 = ttk.Frame(tabControl)

tabControl.add(settings, text='Setting')
tabControl.add(schedules, text='Schedule')
tabControl.add(tab3, text='Theme')
tabControl.add(tab4, text='About')
tabControl.pack(expand=2, fill="both")

# Checkbox: Start Stretchly automatically when logging in
tk.Checkbutton(settings, text="Start Stretchly automatically when logging in", variable=start_on_login_var).grid(row=1, columnspan=2, padx=25, pady=(15,0), sticky=tk.W)

# Radio Buttons: Window and Full screen
tk.Label(settings, text ="Shows breaks in:").grid(row=2, columnspan=2, padx=25, pady=5, sticky=tk.W)
tk.Radiobutton(settings, text="Window", variable=display_mode_var, value="Window",width=1).grid(row=3, column=0, padx=(25,0), sticky=tk.EW)
tk.Radiobutton(settings, text="Full screen", variable=display_mode_var, value="Full screen").grid(row=3, column=1, sticky=tk.W)

# Checkboxes for other options
tk.Checkbutton(settings, text="Show exercise tips during breaks", variable=exercise_tips_var).grid(row=4, columnspan=2, padx=25, sticky=tk.W)
tk.Checkbutton(settings, text="Show breaks on all monitors", variable=all_monitors_var).grid(row=5, columnspan=2, padx=25, sticky=tk.W)
tk.Checkbutton(settings, text="Monitor system idle time", variable=idle_time_var).grid(row=6, columnspan=2, padx=25, sticky=tk.W)
tk.Checkbutton(settings, text="Show breaks even in Do Not Disturb mode", variable=dnd_mode_var).grid(row=7, columnspan=2, padx=25, sticky=tk.W)

# Dropdown Menu: Language Selection
language_var = tk.StringVar(value="English")
language_label = tk.Label(settings, text="Select Language : ").grid(row=9,column=0, padx=25, pady=20, sticky=tk.W)

language_combobox = ttk.Combobox(settings, textvariable=language_var, values=["English", "Spanish", "French", "German"])
language_combobox.grid(row=9,column=1, sticky=tk.W, padx=10)

# Button: Restore Defaults
def restore_defaults():
    start_on_login_var.set(False)
    display_mode_var.set("Window")
    exercise_tips_var.set(True)
    all_monitors_var.set(True)
    idle_time_var.set(True)
    dnd_mode_var.set(False)
    language_var.set("English")

restore_defaults_button = tk.Button(settings, text="Restore defaults", command=restore_defaults)
restore_defaults_button.grid(row=10, padx=25, pady=10)

###############################################################################################################################

#####     SCHEDULE TABS     #####

# Fungsi untuk mendapatkan nilai dari Spinbox
def get_timer_values():
    # Ambil nilai dari Spinbox
    mini_break_for = (mini_break_for_hour.get() * 3600 +
                            mini_break_for_minute.get() * 60 +
                            mini_break_for_second.get())
    mini_break_duration = (mini_break_duration_hour.get() * 3600 +
                            mini_break_duration_minute.get() * 60 +
                            mini_break_duration_second.get())
    long_break_for = (long_break_for_hour.get() * 3600 +
                            long_break_for_minute.get() * 60 +
                            long_break_for_second.get())
    long_break_duration = (long_break_duration_hour.get() * 3600 +
                            long_break_duration_minute.get() * 60 +
                            long_break_duration_second.get())

    # Reset Spinbox ke 0
    reset_spinboxes()

    # Jalankan hitung mundur dengan durasi di thread terpisah
    threading.Thread(target=hitung_mundur, args=(mini_break_for, mini_break_duration, long_break_for, long_break_duration)).start()

def reset_spinboxes():
    mini_break_for_hour.set(0)
    mini_break_for_minute.set(0)
    mini_break_for_second.set(0)
    mini_break_duration_hour.set(0)
    mini_break_duration_minute.set(0)
    mini_break_duration_second.set(0)

    long_break_for_hour.set(0)
    long_break_for_minute.set(0)
    long_break_for_second.set(0)
    long_break_duration_hour.set(0)
    long_break_duration_minute.set(0)
    long_break_duration_second.set(0)

# Fungsi untuk validasi input
def validate_input(P, max_val):
    if P == "":
        return True  # Izinkan kosong
    if P.isdigit():
        num = int(P)
        if 0 <= num <= max_val:
            return True
    return False

# Variabel untuk Mini Break
enable_minibreak_timer = tk.BooleanVar(value=True)
mini_break_for_hour = tk.IntVar(value=0)
mini_break_for_minute = tk.IntVar(value=0)
mini_break_for_second = tk.IntVar(value=0)
mini_break_duration_hour = tk.IntVar(value=0)
mini_break_duration_minute = tk.IntVar(value=0)
mini_break_duration_second = tk.IntVar(value=0)

# Daftarkan fungsi validasi
validate_cmd_hour = root.register(lambda P: validate_input(P, 23))  # Batas jam 23
validate_cmd_min_sec = root.register(lambda P: validate_input(P, 59))  # Batas menit & detik 59

## MINI BREAK SECTION ##
tk.Label(schedules, text="Mini break", font=("Helvetica", 14)).grid(row=0, column=0, padx=10, pady=(5,0), sticky=tk.W)
tk.Checkbutton(schedules, text="Enable timer", variable=enable_minibreak_timer).grid(padx=10, row=1, column=0, sticky=tk.W)

# Time between breaks
tk.Label(schedules, text="Break for :").grid(padx=10, row=2, column=0, sticky=tk.W)
tk.Spinbox(schedules, from_=0, to=23, textvariable=mini_break_for_hour, width=3, validate='key', validatecommand=(validate_cmd_hour, "%P")).grid(row=2, column=1, padx=5)
tk.Label(schedules, text=":").grid(row=2, column=2, sticky=tk.W)
tk.Spinbox(schedules, from_=0, to=59, textvariable=mini_break_for_minute, width=3, validate='key', validatecommand=(validate_cmd_min_sec, "%P")).grid(row=2, column=3, padx=5)
tk.Label(schedules, text=":").grid(row=2, column=4, sticky=tk.W)
tk.Spinbox(schedules, from_=0, to=59, textvariable=mini_break_for_second, width=3, validate='key', validatecommand=(validate_cmd_min_sec, "%P")).grid(row=2, column=5, padx=5)

# Break duration
tk.Label(schedules, text="Break duration :").grid(padx=10, row=3, column=0, sticky=tk.W)
tk.Spinbox(schedules, from_=0, to=23, textvariable=mini_break_duration_hour,width=3, validate='key', validatecommand=(validate_cmd_hour, "%P")).grid(row=3, column=1, padx=5)
tk.Label(schedules, text=":").grid(row=3, column=2, sticky=tk.W)
tk.Spinbox(schedules, from_=0, to=59, textvariable=mini_break_duration_minute,width=3, validate='key', validatecommand=(validate_cmd_min_sec, "%P")).grid(row=3, column=3, padx=5)
tk.Label(schedules, text=":").grid(row=3, column=4, sticky=tk.W)
tk.Spinbox(schedules, from_=0, to=59, textvariable=mini_break_duration_second,width=3, validate='key', validatecommand=(validate_cmd_min_sec, "%P")).grid(row=3, column=5, padx=5)

# Variabel untuk Long Break
enable_longbreak_timer = tk.BooleanVar(value=True)
long_break_for_hour = tk.IntVar(value=0)
long_break_for_minute = tk.IntVar(value=0)
long_break_for_second = tk.IntVar(value=0)
long_break_duration_hour = tk.IntVar(value=0)
long_break_duration_minute = tk.IntVar(value=0)
long_break_duration_second = tk.IntVar(value=0)

## LONG BREAK SECTION ##
tk.Label(schedules, text="Long break", font=("Helvetica", 14)).grid(row=4, column=0, padx=10, pady=(15,0), sticky=tk.W)
tk.Checkbutton(schedules, text="Enable timer", variable=enable_longbreak_timer).grid(row=5, column=0, padx=10, sticky=tk.W)

# Time between breaks
tk.Label(schedules, text="Break for :").grid(padx=10, row=6, column=0, sticky=tk.W)
tk.Spinbox(schedules, from_=0, to=23, textvariable=long_break_for_hour, width=3, validate='key', validatecommand=(validate_cmd_hour, "%P")).grid(row=6, column=1, padx=5)
tk.Label(schedules, text=":").grid(row=6, column=2, sticky=tk.W)
tk.Spinbox(schedules, from_=0, to=59, textvariable=long_break_for_minute, width=3, validate='key', validatecommand=(validate_cmd_min_sec, "%P")).grid(row=6, column=3, padx=5)
tk.Label(schedules, text=":").grid(row=6, column=4, sticky=tk.W)
tk.Spinbox(schedules, from_=0, to=59, textvariable=long_break_for_second, width=3, validate='key', validatecommand=(validate_cmd_min_sec, "%P")).grid(row=6, column=5, padx=5)

# Break duration
tk.Label(schedules, text="Break duration :").grid(padx=10, row=7, column=0, sticky=tk.W)
tk.Spinbox(schedules, from_=0, to=23, textvariable=long_break_duration_hour,width=3, validate='key', validatecommand=(validate_cmd_hour, "%P")).grid(row=7, column=1, padx=5)
tk.Label(schedules, text=":").grid(row=7, column=2, sticky=tk.W)
tk.Spinbox(schedules, from_=0, to=59, textvariable=long_break_duration_minute,width=3, validate='key', validatecommand=(validate_cmd_min_sec, "%P")).grid(row=7, column=3, padx=5)
tk.Label(schedules, text=":").grid(row=7, column=4, sticky=tk.W)
tk.Spinbox(schedules, from_=0, to=59, textvariable=long_break_duration_second,width=3, validate='key', validatecommand=(validate_cmd_min_sec, "%P")).grid(row=7, column=5, padx=5)

# Tombol untuk mendapatkan nilai
tk.Button(schedules, text="Dapatkan Nilai", command=get_timer_values).grid(row=9, column=0, columnspan=6, pady=20)

def show_popup(message, time):
    # Membuat jendela pop-up
    root = tk.Tk()
    root.title("Alarm")
    root.configure(background="#1D1F21")
    root.attributes("-topmost", 1)
    root.attributes('-fullscreen', True)

    label = tk.Label(root, text=message, font=("Helvetica", 16), fg="white", bg="#1D1F21")
    label.pack(expand=True)
    
    # Menutup jendela setelah 5 detik
    root.after(time, root.destroy)  # 5000 ms = 5 detik
    root.mainloop()

def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        t -= 1
    print("00:00", end="\r")  # Menampilkan 00:00 setelah countdown selesai

# Fungsi untuk menghitung interval dan waktu mundur
def hitung_mundur(mini_break_for, mini_break_duration, long_break_for, long_break_duration):
    # Hitung interval
    interval = (long_break_duration / mini_break_duration)
    print(f"Interval awal: {interval:.1f} kali")

    # Waktu mundur
    print(f"Mini Break for: {mini_break_for // 3600} jam {(mini_break_for % 3600) // 60} menit {mini_break_for % 60} detik")
    print(f"Mini Break duration: {mini_break_duration // 3600} jam {(mini_break_duration % 3600) // 60} menit {mini_break_duration % 60} detik")
    print(f"Long Break for: {long_break_for // 3600} jam {(long_break_for % 3600) // 60} menit {long_break_for % 60} detik")
    print(f"Long Break duration: {long_break_duration // 3600} jam {(long_break_duration % 3600) // 60} menit {long_break_duration % 60} detik")

    reset_spinboxes()

    # Mulai countdown untuk jam1 dan jam2
    for i in np.arange(interval):
        if interval > 1.0:
            print(f"\nCountdown Mini Break: {mini_break_duration // 60} menit")
            countdown(mini_break_duration)  # Countdown untuk jam1
            print("Alarm Mini Break berbunyi!")
            show_popup("Alarm Mini Break berbunyi!", mini_break_for)  # Tampilkan alarm jam1

            # Kurangi waktu jam2 dengan jam1
            long_break_duration -= mini_break_duration
            
            # Hitung ulang interval
            interval -= 1
        else:
            print(f"\nSisa waktu Long Break: {long_break_duration // 60} menit")
            print(f"Countdown Long Break: {long_break_duration // 60} menit")
            countdown(long_break_duration)  # Countdown untuk jam2
            print("Alarm Long Break berbunyi!")
            print("Jam sudah habis!")
            show_popup("Alarm Long Break berbunyi!", long_break_for)  # Tampilkan alarm jam2
            break

# Run the application
root.mainloop()
