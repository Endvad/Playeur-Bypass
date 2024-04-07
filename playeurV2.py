import tkinter as tk
import tkinter.ttk as ttk
import webbrowser
import pyperclip
import urllib.request
import urllib.error
import os 
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def convert_image_to_video(image_url):
    if manual_checkbox_var.get() == False:
        debug_mode = [False, True]
        static_part, dynamic_part = image_url.rsplit('/', 1)
        filename_part = dynamic_part[:11]
        qualities = ["original", "1080p", "720p", "480p", "360p", "240p", "144p"]
        for debug_yon in debug_mode:
            for quality in qualities:
                if debug_yon:
                    if static_part.startswith("https://data-1.utreon.com/"):
                        static_part = static_part.replace("https://data-1.utreon.com/", "https://data-2.playeur.com/")
                    elif static_part.startswith("https://data-2.playeur.com/"):
                        static_part = static_part.replace("https://data-2.playeur.com/", "https://data-1.utreon.com/")
                video_filename = f"{filename_part}_{quality}.mp4"
                video_url = f"{static_part}/{video_filename}"
                try:
                    urllib.request.urlopen(video_url)
                    return video_url
                except:
                    pass
        return "Introuvable"


    else:
        debug_mode = debug_var.get()
        static_part, dynamic_part = image_url.rsplit('/', 1)
        filename_part = dynamic_part[:11]
        quality = quality_var.get()
        if quality == "Original":
            quality = "original"
        if debug_mode:
            if static_part.startswith("https://data-1.utreon.com/"):
                static_part = static_part.replace("https://data-1.utreon.com/", "https://data-2.playeur.com/")
            elif static_part.startswith("https://data-2.playeur.com/"):
                static_part = static_part.replace("https://data-2.playeur.com/", "https://data-1.utreon.com/")
        video_filename = f"{filename_part}_{quality}.mp4"
        video_url = f"{static_part}/{video_filename}"
        return video_url

def convert_and_display():
    image_url = entry_url.get()
    video_url = convert_image_to_video(image_url)
    result_var.set(video_url)

def toggle_visibility():
    if manual_checkbox_var.get():
        button_copy.grid(row=3, column=2, padx=5, pady=5)
        label_quality.grid(row=3, column=0, padx=5, pady=5)
        quality_menu.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        button_download.grid(row=3, column=1, padx=5, pady=5, sticky="e")
        debug_checkbox.grid(row=3, column=1, padx=5, pady=5)
    else:
        button_copy.grid_forget()
        label_quality.grid_forget()
        quality_menu.grid_forget()
        button_download.grid_forget()
        debug_checkbox.grid_forget()

def open_in_browser():
    webbrowser.open(result_var.get())

def copy_to_clipboard():
    pyperclip.copy(result_var.get())

def download_file():
    url = result_var.get()
    file_name = url.split('/')[-1]
    urllib.request.urlretrieve(url, file_name)

# Création de la fenêtre principale
root = tk.Tk()
root.title("Playeur Bypass")
root.iconbitmap(resource_path('./icon.ico'))
root.resizable(width=False, height=False)
ttk.Style().theme_use('clam')

# Création des widgets
label_url = tk.Label(root, text="URL de la miniature de la vidéo :")
label_url.grid(row=0, column=0, padx=5, pady=5)

entry_url = tk.Entry(root, width=50)
entry_url.grid(row=0, column=1, padx=5, pady=5)

button_convert = tk.Button(root, text="Convertir", command=convert_and_display)
button_convert.grid(row=0, column=2, padx=5, pady=5)

label_result = tk.Label(root, text="Résultat de la conversion :")
label_result.grid(row=1, column=0, padx=5, pady=5)

result_var = tk.StringVar()
result_entry = tk.Entry(root, textvariable=result_var, state='readonly', width=50)
result_entry.grid(row=1, column=1, padx=5, pady=5)

button_open = tk.Button(root, text="Ouvrir", command=open_in_browser)
button_open.grid(row=1, column=2, padx=5, pady=5)

button_copy = tk.Button(root, text="Copier", command=copy_to_clipboard)
button_copy.grid_forget()

# Menu déroulant pour sélectionner la qualité de la vidéo
quality_var = tk.StringVar()
quality_var.set("original")

label_quality = tk.Label(root, text="Qualité :")
label_quality.grid_forget()

quality_menu = ttk.OptionMenu(root, quality_var, "Original", "144p", "240p", "360p", "480p", "720p", "1080p", "Original")
quality_menu.grid_forget()


# Bouton de téléchargement
button_download = tk.Button(root, text="Télécharger", command=download_file)
button_download.grid_forget()

# Case à cocher pour le mode manuel
manual_checkbox_var = tk.BooleanVar()
manual_checkbox_var.set(False)

manual_checkbox = tk.Checkbutton(root, text="Mode Manuel", variable=manual_checkbox_var, command=toggle_visibility)
manual_checkbox.grid(row=2, column=0, padx=5, pady=5)

# Case à cocher pour le mode debug
debug_var = tk.BooleanVar()
debug_var.set(False)

debug_checkbox = tk.Checkbutton(root, text="Debug", variable=debug_var)
debug_checkbox.grid_forget()

# Lancement de la boucle principale
root.mainloop()