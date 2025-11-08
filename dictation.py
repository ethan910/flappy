import tkinter as tk
import customtkinter
import pygame
import random
import threading
import time
import os
from tkinter import messagebox # Needed for the error popup

# Set the appearance mode
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

class ChineseIdiomSongGame:
    def __init__(self, app):
        self.root = app
        self.root.title("中文成語歌曲記憶遊戲")
        self.root.geometry("700x800")

        # Define gradient colors
        self.color_top = "#667eea"
        self.color_bottom = "#764ba2"

        # --- 1. The CORRECT Gradient Frame ---
        gradient_frame = customtkinter.CTkFrame(self.root,
                                                fg_color=(self.color_top, self.color_bottom),
                                                corner_radius=0)
        gradient_frame.pack(fill="both", expand=True)

        # Initialize pygame mixer
        pygame.mixer.init()

        # Get Base Path
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.sounds_dir = os.path.join(self.base_dir, 'sounds')

        # --- Song list with 'selected' flag ---
        self.songs = [
            {"name": "森森然", "url": "森森然.mp3", "selected": True},
            {"name": "翠色欲流", "url": "翠色欲流.mp3", "selected": True},
            {"name": "寵辱皆忘", "url": "寵辱皆忘.mp3", "selected": True},
            {"name": "一碧千里", "url": "一碧千里.mp3", "selected": True},
            {"name": "神清氣朗", "url": "神清氣朗.mp3", "selected": True},
            {"name": "含苞欲放", "url": "含苞欲放.mp3", "selected": True},
            {"name": "花紅柳綠", "url": "花紅柳綠.mp3", "selected": True},
            {"name": "奼紫嫣紅", "url": "奼紫嫣紅.mp3", "selected": True},
            {"name": "沁人心脾", "url": "沁人心脾.mp3", "selected": True},
            {"name": "巍巍然", "url": "巍巍然.mp3", "selected": True},
            {"name": "雲遮霧繞", "url": "雲遮霧繞.mp3", "selected": True},
            {"name": "危峯兀立", "url": "危峯兀立.mp3", "selected": True},
            {"name": "微波粼粼", "url": "微波粼粼.mp3", "selected": True},
            {"name": "淙淙流水", "url": "淙淙流水.mp3", "selected": True},
            {"name": "怪石嶙峋", "url": "怪石嶙峋.mp3", "selected": True},
            {"name": "夾道", "url": "夾道.mp3", "selected": True},
            {"name": "虯勁", "url": "虯勁.mp3", "selected": True},
            {"name": "偌大", "url": "偌大.mp3", "selected": True},
            {"name": "浩浩湯湯", "url": "浩浩湯湯.mp3", "selected": True},
            {"name": "極目四野", "url": "極目四野.mp3", "selected": True}
        ]
        self.song_checkbox_vars = [] # To hold checkbox variables

        # Game state
        self.total_selected_songs = len(self.songs) # Initially all are selected
        self.reset_game_state()

        # Create all widgets
        self.create_widgets(gradient_frame)

    def reset_game_state(self):
        self.is_playing = False
        self.is_paused = False
        self.current_song_index = 0
        self.played_songs = []
        self.shuffled_songs = [] # This will hold only selected songs during gameplay
        self.is_repeating = False
        self.timer_thread = None
        self.countdown = 0
        self.stop_timer = False
        # Don't reset total_selected_songs here

    def create_widgets(self, parent_frame):

        self.main_frame = customtkinter.CTkFrame(parent_frame,
                                                 fg_color='white',
                                                 corner_radius=20,
                                                 border_width=1,
                                                 border_color="#cccccc")
        self.main_frame.place(relx=0.5, rely=0.5, anchor='center')

        title_font = customtkinter.CTkFont(family='Microsoft JhengHei', size=24, weight='bold')
        title_label = customtkinter.CTkLabel(self.main_frame,
                                             text="🎵 中文成語歌曲記憶遊戲 🎵",
                                             font=title_font,
                                             fg_color='white',
                                             text_color='#333')
        title_label.pack(pady=(40, 30), padx=40)

        progress_frame = customtkinter.CTkFrame(self.main_frame, fg_color='transparent')
        progress_frame.pack(fill='x', padx=40)

        label_font = customtkinter.CTkFont(family='Microsoft JhengHei', size=12)
        # Initialize with total selected count
        self.progress_label = customtkinter.CTkLabel(progress_frame,
                                                     text=f"進度: 0 / {self.total_selected_songs}",
                                                     font=label_font,
                                                     text_color='#555')
        self.progress_label.pack()

        self.progress_var = tk.DoubleVar()
        self.progress_bar = customtkinter.CTkProgressBar(progress_frame,
                                                         variable=self.progress_var,
                                                         progress_color='#28a745',
                                                         fg_color='#e0e0e0',
                                                         height=10,
                                                         corner_radius=5)
        self.progress_bar.pack(pady=(10, 0), fill='x', expand=True)
        self.progress_var.set(0)

        timer_font = customtkinter.CTkFont(family='Microsoft JhengHei', size=10, weight='bold')
        self.timer_label = customtkinter.CTkLabel(self.main_frame,
                                                  text="",
                                                  font=timer_font,
                                                  text_color='#007bff')
        self.timer_label.pack(pady=(10, 0))

        status_font = customtkinter.CTkFont(family='Microsoft JhengHei', size=11, weight='bold')
        self.status_label = customtkinter.CTkLabel(self.main_frame,
                                                   text="點擊 START 開始遊戲",
                                                   font=status_font,
                                                   fg_color='#f8f9fa',
                                                   text_color='#333',
                                                   corner_radius=6)
        self.status_label.pack(pady=(15, 0), padx=40, fill='x', ipady=5)

        # --- Song Selection Button ---
        select_button_font = customtkinter.CTkFont(family='Microsoft JhengHei', size=12)
        self.select_songs_button = customtkinter.CTkButton(self.main_frame,
                                                          text="選擇歌曲",
                                                          font=select_button_font,
                                                          fg_color="#17a2b8", # Teal color
                                                          hover_color="#138496",
                                                          text_color="white",
                                                          corner_radius=8,
                                                          command=self.open_song_selection_window)
        self.select_songs_button.pack(pady=(15, 0), padx=40)


        control_frame = customtkinter.CTkFrame(self.main_frame, fg_color='transparent')
        control_frame.pack(pady=(10, 40), padx=40) # Reduced top padding slightly

        button_font = customtkinter.CTkFont(family='Microsoft JhengHei', size=14, weight='bold')

        self.start_button = customtkinter.CTkButton(control_frame,
                                                    text="START",
                                                    font=button_font,
                                                    fg_color='#28a745',
                                                    hover_color='#218838',
                                                    text_color='white',
                                                    corner_radius=10,
                                                    command=self.start_game)
        self.start_button.pack(side='left', padx=5)

        self.pause_button = customtkinter.CTkButton(control_frame,
                                                    text="PAUSE",
                                                    font=button_font,
                                                    fg_color='#dc3545',
                                                    hover_color='#c82333',
                                                    text_color='white',
                                                    corner_radius=10,
                                                    command=self.toggle_pause)

        self.song_order_frame = customtkinter.CTkFrame(self.main_frame,
                                                       fg_color='#f8f9fa',
                                                       corner_radius=10,
                                                       border_width=1,
                                                       border_color='#dddddd')

        order_title_font = customtkinter.CTkFont(family='Microsoft JhengHei', size=12, weight='bold')
        order_title = customtkinter.CTkLabel(self.song_order_frame,
                                             text="播放順序",
                                             font=order_title_font,
                                             text_color='#333')
        order_title.pack(pady=(10, 0))

        textbox_font = customtkinter.CTkFont(family='Microsoft JhengHei', size=12)
        self.song_list_text = customtkinter.CTkTextbox(self.song_order_frame,
                                                        width=400,
                                                        height=220,
                                                        font=textbox_font,
                                                        fg_color='white',
                                                        text_color='#333',
                                                        corner_radius=6,
                                                        border_width=1,
                                                        border_color='#ccc')
        self.song_list_text.pack(pady=(10, 10), padx=10, fill='both', expand=True)
        self.song_list_text.configure(state='disabled')

        self.song_order_frame.pack_forget()

    # --- New Function to Open Selection Window ---
    def open_song_selection_window(self):
        if self.is_playing:
             messagebox.showwarning("提示", "遊戲進行中，無法更改歌曲選擇。")
             return

        select_window = customtkinter.CTkToplevel(self.root)
        select_window.title("選擇要播放的歌曲")
        select_window.geometry("400x500")
        select_window.transient(self.root) # Keep on top of main window
        select_window.grab_set() # Block interaction with main window

        # Scrollable Frame for Checkboxes
        scrollable_frame = customtkinter.CTkScrollableFrame(select_window, label_text="歌曲列表")
        scrollable_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.song_checkbox_vars = [] # Clear previous vars if any
        checkbox_font = customtkinter.CTkFont(family='Microsoft JhengHei', size=12)

        for i, song in enumerate(self.songs):
            var = tk.BooleanVar(value=song["selected"])
            checkbox = customtkinter.CTkCheckBox(scrollable_frame,
                                                 text=song["name"],
                                                 variable=var,
                                                 font=checkbox_font)
            checkbox.grid(row=i, column=0, pady=(0, 10), padx=10, sticky="w")
            self.song_checkbox_vars.append(var) # Store the variable

        # Button Frame
        button_frame = customtkinter.CTkFrame(select_window, fg_color="transparent")
        button_frame.pack(pady=(0, 20))

        def select_all():
            for var in self.song_checkbox_vars:
                var.set(True)

        def deselect_all():
            for var in self.song_checkbox_vars:
                var.set(False)

        def confirm_selection():
            new_total = 0
            for i, song in enumerate(self.songs):
                is_selected = self.song_checkbox_vars[i].get()
                song["selected"] = is_selected
                if is_selected:
                    new_total += 1
            self.total_selected_songs = new_total
            # Update main window progress label immediately
            self.progress_label.configure(text=f"進度: 0 / {self.total_selected_songs}")
            select_window.destroy()

        button_font_small = customtkinter.CTkFont(family='Microsoft JhengHei', size=12)
        select_all_button = customtkinter.CTkButton(button_frame, text="全選", command=select_all, font=button_font_small, width=80)
        select_all_button.grid(row=0, column=0, padx=5)

        deselect_all_button = customtkinter.CTkButton(button_frame, text="全不選", command=deselect_all, font=button_font_small, width=80)
        deselect_all_button.grid(row=0, column=1, padx=5)

        confirm_button = customtkinter.CTkButton(button_frame, text="確定", command=confirm_selection, font=button_font_small, width=80)
        confirm_button.grid(row=0, column=2, padx=5)


    def update_progress(self):
        # Use length of shuffled_songs (which is the filtered list)
        total_songs_in_game = len(self.shuffled_songs)
        if total_songs_in_game == 0:
             progress = 0
        else:
             progress = (len(self.played_songs) / total_songs_in_game)

        self.progress_var.set(progress)
        self.progress_label.configure(text=f"進度: {len(self.played_songs)} / {total_songs_in_game}")


    def update_status(self, message, bg_color='#f8f9fa', fg_color='#333'):
        self.status_label.configure(text=message, fg_color=bg_color, text_color=fg_color)

    def update_timer_display(self):
        if self.countdown > 0:
            self.timer_label.configure(text=f"倒數: {self.countdown} 秒")
        else:
            self.timer_label.configure(text="")

    def display_song_order(self):
        self.song_list_text.configure(state='normal')
        self.song_list_text.delete("1.0", "end")

        for i, song in enumerate(self.shuffled_songs, 1): # Display only shuffled (selected) songs
            self.song_list_text.insert("end", f"{i:2d}. {song['name']}\n")

        self.song_list_text.configure(state='disabled')
        self.song_order_frame.pack(pady=(0, 40), padx=40, fill='both', expand=True)
        self.main_frame.place(relx=0.5, rely=0.5, anchor='center')

    def hide_song_order(self):
        self.song_order_frame.pack_forget()
        self.main_frame.place(relx=0.5, rely=0.5, anchor='center')

    def play_current_song(self):
        if self.current_song_index >= len(self.shuffled_songs): # Use shuffled_songs list
            return

        current_song = self.shuffled_songs[self.current_song_index] # Use shuffled_songs list

        def play_audio():
            try:
                audio_file_path = os.path.join(self.sounds_dir, current_song['url'])

                if not os.path.exists(audio_file_path):
                    print(f"File not found: {audio_file_path}")
                    self.root.after(0, lambda: self.update_status(f"音頻文件不存在: {current_song['url']}", '#f8d7da', '#721c24'))
                    self.root.after(2000, self.next_song)
                    return

                pygame.mixer.music.load(audio_file_path)
                pygame.mixer.music.play()

                if not self.is_repeating:
                    # Displaying song number relative to the selected list
                    display_index = self.current_song_index + 1
                    self.root.after(0, lambda: self.update_status(f"正在播放第 {display_index} 首歌曲...", '#d4edda', '#155724'))
                    self.countdown = 5
                    self.start_countdown_timer(5, self.repeat_current_song)
                else:
                    display_index = self.current_song_index + 1
                    self.root.after(0, lambda: self.update_status(f"重複播放第 {display_index} 首歌曲...", '#fff3cd', '#856404'))
                    self.countdown = 3
                    self.start_countdown_timer(3, self.next_song)

            except pygame.error as e:
                print(f"Error loading/playing audio: {e}")
                self.root.after(0, lambda: self.update_status(f"無法加載音頻: {current_song['url']}", '#f8d7da', '#721c24'))
                self.root.after(2000, self.next_song)
            except Exception as e:
                print(f"Error playing audio: {e}")
                self.root.after(0, lambda: self.update_status("播放錯誤，跳到下一首", '#f8d7da', '#721c24'))
                self.root.after(2000, self.next_song)

        audio_thread = threading.Thread(target=play_audio)
        audio_thread.daemon = True
        audio_thread.start()

    def start_countdown_timer(self, duration, callback):
        self.stop_timer = False

        def countdown():
            current_countdown = duration
            while current_countdown > 0 and not self.stop_timer:
                while self.is_paused and not self.stop_timer: time.sleep(0.1)
                if self.stop_timer: break
                self.countdown = current_countdown
                self.root.after(0, self.update_timer_display)
                time.sleep(1)
                while self.is_paused and not self.stop_timer: time.sleep(0.1)
                if self.stop_timer: break
                current_countdown -= 1

            if not self.stop_timer:
                self.countdown = 0
                self.root.after(0, self.update_timer_display)
                self.root.after(0, callback)

        self.timer_thread = threading.Thread(target=countdown)
        self.timer_thread.daemon = True
        self.timer_thread.start()

    def repeat_current_song(self):
        self.is_repeating = True
        pygame.mixer.music.stop()
        self.play_current_song()

    def next_song(self):
        self.stop_timer = True

        if self.current_song_index < len(self.shuffled_songs):
            current_song = self.shuffled_songs[self.current_song_index]
            self.played_songs.append(current_song)
            self.update_progress()

        self.current_song_index += 1
        self.is_repeating = False

        if self.current_song_index >= len(self.shuffled_songs): # Check against shuffled list length
            # Game completed
            pygame.mixer.music.stop()
            self.is_playing = False
            self.is_paused = False
            self.start_button.configure(text="RESTART",
                                        fg_color='#007bff',
                                        hover_color='#0056b3',
                                        state='normal')
            self.pause_button.pack_forget()
            self.select_songs_button.configure(state='normal') # Re-enable song selection
            self.update_status("🎉 遊戲完成！查看下方播放順序", '#d1ecf1', '#0c5460')
            self.timer_label.configure(text="")
            self.display_song_order()
        else:
            self.play_current_song()

    def start_game(self):
        if not self.is_playing:
            # --- Filter selected songs ---
            selected_songs_list = [song for song in self.songs if song["selected"]]

            if not selected_songs_list:
                messagebox.showerror("錯誤", "請至少選擇一首歌曲才能開始遊戲。")
                return

            self.reset_game_state()
            self.is_playing = True
            self.shuffled_songs = random.sample(selected_songs_list, len(selected_songs_list)) # Shuffle only selected
            self.total_selected_songs = len(self.shuffled_songs) # Update total count for progress

            self.start_button.configure(text="播放中...", state='disabled', fg_color='#6c757d')
            self.select_songs_button.configure(state='disabled') # Disable song selection during game
            self.pause_button.configure(text="PAUSE",
                                        fg_color='#dc3545',
                                        hover_color='#c82333',
                                        state='normal')
            self.pause_button.pack(side='left', padx=5)

            self.hide_song_order()
            self.update_progress() # Update progress bar for the selected count
            self.update_status("遊戲開始...", '#d1ecf1', '#0c5460')
            self.play_current_song()

    def toggle_pause(self):
        if not self.is_playing: return

        if self.is_paused:
            self.is_paused = False
            pygame.mixer.music.unpause()
            self.pause_button.configure(text="PAUSE",
                                        fg_color='#dc3545',
                                        hover_color='#c82333')
            display_index = self.current_song_index + 1
            self.update_status(f"繼續播放第 {display_index} 首歌曲...", '#d1ecf1', '#0c5460')
        else:
            self.is_paused = True
            pygame.mixer.music.pause()
            self.pause_button.configure(text="RESUME",
                                        fg_color='#007bff',
                                        hover_color='#0056b3')
            self.update_status("遊戲已暫停", '#fff3cd', '#856404')

    def cleanup(self):
        pygame.mixer.music.stop()
        self.stop_timer = True
        self.is_paused = False

    def on_closing(self):
        self.cleanup()
        self.root.destroy()

def main():
    app = customtkinter.CTk()
    game = ChineseIdiomSongGame(app)
    app.protocol("WM_DELETE_WINDOW", game.on_closing)
    app.mainloop()

if __name__ == "__main__":
    main()
