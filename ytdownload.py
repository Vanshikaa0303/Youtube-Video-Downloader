import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import yt_dlp
import os


# ---------- Colors ----------
BG = "#F5E6D3"
CARD = "#FFF8E7"
BROWN = "#8B5E3C"
DARK = "#4B3621"
LIGHT_BROWN = "#C19A6B"


download_folder = ""


# ---------- Functions ----------

def choose_folder():
    global download_folder

    download_folder = filedialog.askdirectory()

    if download_folder:
        folder_label.config(
            text=download_folder
        )


def update_progress(d):
    if d["status"] == "downloading":

        total = d.get("total_bytes") or d.get("total_bytes_estimate")

        if total:
            percent = int(
                d["downloaded_bytes"] * 100 / total
            )

            progress["value"] = percent
            status.config(
                text=f"Downloading... {percent}%"
            )


    elif d["status"] == "finished":

        progress["value"] = 100
        status.config(
            text="Processing video..."
        )


def download_video():

    url = url_entry.get()

    if not url:
        messagebox.showwarning(
            "Missing URL",
            "Please enter YouTube URL"
        )
        return


    if not download_folder:
        messagebox.showwarning(
            "Folder Missing",
            "Select download folder"
        )
        return


    quality = quality_var.get()


    if quality == "1080p":
        format_type = "bestvideo[height<=1080]+bestaudio/best"

    elif quality == "720p":
        format_type = "bestvideo[height<=720]+bestaudio/best"

    elif quality == "480p":
        format_type = "bestvideo[height<=480]+bestaudio/best"

    else:
        format_type = "best"


    options = {

        "format": format_type,

        "outtmpl":
        os.path.join(
            download_folder,
            "%(title)s.%(ext)s"
        ),

        "progress_hooks":
        [update_progress],

        "merge_output_format":
        "mp4"
    }


    try:

        status.config(
            text="Starting download..."
        )


        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])


        status.config(
            text="Download Completed ✓"
        )


        messagebox.showinfo(
            "Success",
            "Video saved successfully!"
        )


    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e)
        )



# ---------- Hover Effect ----------

def hover(button):

    button.bind(
        "<Enter>",
        lambda e:
        button.config(
            bg=LIGHT_BROWN
        )
    )

    button.bind(
        "<Leave>",
        lambda e:
        button.config(
            bg=BROWN
        )
    )



# ---------- Window ----------

root = tk.Tk()

root.title(
    "YouTube Video Downloader"
)

root.geometry(
    "600x520"
)

root.configure(
    bg=BG
)

root.resizable(
    False,
    False
)



# ---------- Card ----------

card = tk.Frame(
    root,
    bg=CARD
)

card.place(
    x=50,
    y=40,
    width=500,
    height=430
)



title = tk.Label(

    card,

    text="▶ YouTube Downloader",

    font=(
        "Georgia",
        22,
        "bold"
    ),

    bg=CARD,

    fg=DARK
)

title.pack(
    pady=25
)



subtitle = tk.Label(

    card,

    text="Download videos with style",

    font=(
        "Arial",
        11
    ),

    bg=CARD,

    fg=DARK
)

subtitle.pack()



url_entry = tk.Entry(

    card,

    width=50,

    font=(
        "Arial",
        11
    ),

    bg="#FFFDF5",

    fg=DARK

)

url_entry.pack(
    pady=20
)

folder_button = tk.Button(

    card,

    text="Choose Folder",

    command=choose_folder,

    bg=BROWN,

    fg="white",

    relief="flat",

    font=(
        "Arial",
        10,
        "bold"
    )

)

folder_button.pack()

hover(folder_button)



folder_label = tk.Label(

    card,

    text="No folder selected",

    bg=CARD,

    fg=DARK,

    wraplength=400

)

folder_label.pack(
    pady=10
)
quality_var = tk.StringVar()

quality_var.set(
    "1080p"
)



quality = ttk.Combobox(

    card,

    textvariable=quality_var,

    values=[
        "Best",
        "1080p",
        "720p",
        "480p"
    ],

    width=15

)

quality.pack(
    pady=10
)



download = tk.Button(

    card,

    text="Download Video",

    command=download_video,

    bg=BROWN,

    fg="white",

    relief="flat",

    font=(
        "Georgia",
        12,
        "bold"
    )

)

download.pack(
    pady=15
)

hover(download)



progress = ttk.Progressbar(

    card,

    length=350,

    mode="determinate"

)

progress.pack()



status = tk.Label(

    card,

    text="Ready",

    bg=CARD,

    fg=DARK,

    font=(
        "Arial",
        10
    )

)

status.pack(
    pady=15
)



root.mainloop()