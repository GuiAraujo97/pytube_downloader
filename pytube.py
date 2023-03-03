import tkinter as tk
from tkinter import messagebox
from pytube import YouTube

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Download de Vídeo do YouTube")
        self.create_widgets()

    def create_widgets(self):
        self.url_label = tk.Label(self.master, text="Insira o link do vídeo do YouTube:")
        self.url_label.pack(pady=5)

        self.url_entry = tk.Entry(self.master, width=40)
        self.url_entry.pack(pady=5)

        self.load_button = tk.Button(self.master, text="Carregar", command=self.load_resolutions)
        self.load_button.pack(pady=5)

        self.res_label = tk.Label(self.master, text="Selecione a resolução do vídeo:")
        self.res_label.pack(pady=5)

        self.res_options = tk.Listbox(self.master, width=20, height=5)
        self.res_options.pack(pady=5)

        self.download_button = tk.Button(self.master, text="Baixar", command=self.download_video, state=tk.DISABLED)
        self.download_button.pack(pady=5)

        self.quit_button = tk.Button(self.master, text="Sair", command=self.master.quit)
        self.quit_button.pack(pady=5)

    def load_resolutions(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showerror("Erro", "Por favor, insira um link válido do YouTube.")
            return

        self.res_options.delete(0, tk.END)
        self.download_button.config(state=tk.DISABLED)

        video = YouTube(url)
        resolutions = []
        for stream in video.streams.filter(progressive=True):
            if stream.resolution not in resolutions:
                resolutions.append(stream.resolution)
                self.res_options.insert(tk.END, stream.resolution)

        if resolutions:
            self.download_button.config(state=tk.NORMAL)

    def download_video(self):
        res_index = self.res_options.curselection()
        if not res_index:
            messagebox.showerror("Erro", "Por favor, selecione uma resolução.")
            return

        url = self.url_entry.get()
        video = YouTube(url)
        res_choice = self.res_options.get(res_index)
        stream = video.streams.filter(res=res_choice, progressive=True).first()
        stream.download()
        messagebox.showinfo("Sucesso", "O vídeo foi baixado com sucesso!")

root = tk.Tk()
app = Application(master=root)
app.mainloop()