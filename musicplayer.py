# Python Music Player,
# Graphical interface,
# Functionality: - Play music
#                - Pause music
#                - Skip to next music
#                - Return to the previous music

import pygame
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os
import time
from mutagen.mp3 import MP3

pygame.mixer.init()

playlist = []
current_index = 0
paused = False

def upload_music():
    global playlist, current_index
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        playlist = [os.path.join(folder_selected, f) for f in os.listdir(folder_selected) if f.endswith('.mp3')]
        current_index = 0
        play_music()

def play_music():
    global paused
    if playlist:
        pygame.mixer.music.load(playlist[current_index])
        pygame.mixer.music.play()
        update_title()
        update_progress()
        paused = False

def pause_music():
    global paused
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
        paused = True
    else:
        pygame.mixer.music.unpause()
        paused = False

def next_music():
    global current_index
    if playlist:
        current_index = (current_index + 1) % len(playlist)
        play_music()

def previous_music():
    global current_index
    if playlist:
        current_index = (current_index - 1) % len(playlist)
        play_music()

def update_title():
    if playlist:
        root.title(f"Playing: {os.path.basename(playlist[current_index])}")

def update_progress():
    if playlist:
        current_music = MP3(playlist[current_index])
        total_length = current_music.info.length
        progress_bar["maximun"] = total_length

        def update_time():
            if pygame.mixer.music.get_busy() and not paused:
                current_time = pygame.mixer.music.get_pos() / 1000
                progress_bar["value"] = current_time
                current_time.config(text=time.strftime('%M:%S', time.gmtime(current_time)))
                total_time.config(text=time.strftime('%M:%S', time.gmtime(total_length)))
                root.after(1000, update_time)

        update_time()
    
def change_progress_position(event):
    if playlist:
        new_time = progress_bar.get()
        pygame.mixer.music.set_pos(new_time)

def change_volume(val):
    pygame.mixer.music.set_volume(float(val))

root = tk.Tk()
root.title("Music Player")
root.geometry("400x300")

style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=5)

frame_top = ttk.Frame(root)
frame_top.pack(pady=10)

btn_upload = tk.Button(frame_top, text="📂 Upload Music", command=upload_music)
btn_play = tk.Button(frame_top, text="▶ Play/Pause", command=pause_music)
btn_next = tk.Button(frame_top, text="⏭ Next", command=next_music)
btn_previous = tk.Button(frame_top, text="⏮ Previous", command=previous_music)

btn_upload.grid(row=0, column=0, padx=5)
btn_play.grid(row=0, column=1, padx=5)
btn_previous.grid(row=0, column=2, padx=5)
btn_next.grid(row=0, column=3, padx=5)

progress_frame = ttk.Frame(root)
progress_frame.pack(pady=10)

current_time = ttk.Label(progress_frame, text="00:00")
current_time.pack(side="left")

progress_bar = ttk.Scale(progress_frame, from_=0, to=100, orient="horizontal", length=250, command=change_progress_position)
progress_bar.pack(side="left", padx=10)

total_time = ttk.Label(progress_frame, text="00:00")
total_time.pack(side="left")

frame_volume = ttk.Frame(root)
frame_volume.pack(pady=10)

ttk.Label(frame_volume, text="🔊 Volume").pack(side="left")
volume_slider = ttk.Scale(frame_volume, from_=0, to=1, orient="horizontal", length=150, command=change_volume)
volume_slider.set(0.5)
volume_slider.pack(side="left")

root.mainloop()