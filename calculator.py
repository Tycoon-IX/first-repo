from tkinter import Tk, Button, Entry, StringVar
import tkinter.font as tkFont

class ModernCalculator:
    def __init__(self, master):
        # Konfigurasi utama window
        master.title("Modern Calculator")  # Judul window
        master.geometry("350x500")        # Ukuran window
        master.resizable(False, False)    # Non-aktifkan resize
        master.configure(bg="#1e1e1e")    # Warna background gelap
        
        # Membuat custom font
        self.display_font = tkFont.Font(family="Segoe UI", size=24)  # Font untuk display
        self.button_font = tkFont.Font(family="Segoe UI", size=14, weight="bold")  # Font untuk tombol
        
        # Variabel untuk menyimpan persamaan
        self.equation = StringVar()
        
        # Membuat display/tampilan kalkulator
        self.display = Entry(master, textvariable=self.equation, 
                           font=self.display_font, bd=0, insertwidth=1,
                           bg="#2d2d2d", fg="#ffffff", justify="right",
                           highlightthickness=2, highlightcolor="#3e3e3e",
                           highlightbackground="#3e3e3e")
        self.display.grid(row=0, column=0, columnspan=4, padx=10, pady=20, sticky="nsew")
        
        # Layout tombol dengan warna modern dark theme
        # Format: (teks tombol, warna background, warna text)
        buttons = [
            ('7', '#3a3a3a', '#ffffff'), ('8', '#3a3a3a', '#ffffff'), ('9', '#3a3a3a', '#ffffff'), ('/', '#2a2a2a', '#ff9500'),
            ('4', '#3a3a3a', '#ffffff'), ('5', '#3a3a3a', '#ffffff'), ('6', '#3a3a3a', '#ffffff'), ('x', '#2a2a2a', '#ff9500'),
            ('1', '#3a3a3a', '#ffffff'), ('2', '#3a3a3a', '#ffffff'), ('3', '#3a3a3a', '#ffffff'), ('-', '#2a2a2a', '#ff9500'),
            ('C', '#2a2a2a', '#ff3b30'), ('0', '#3a3a3a', '#ffffff'), ('=', '#007aff', '#ffffff'), ('+', '#2a2a2a', '#ff9500')
        ]
        
        # Membuat tombol-tombol kalkulator
        row = 1  # Baris awal
        col = 0  # Kolom awal
        for (text, bg_color, fg_color) in buttons:
            # Membuat tombol dengan konfigurasi
            btn = Button(master, text=text, width=5, height=2,
                        command=lambda t=text: self.on_button_click(t),
                        font=self.button_font, bg=bg_color, fg=fg_color,
                        bd=0, activebackground="#4a4a4a", highlightthickness=0)
            # Menempatkan tombol di grid
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            
            # Efek hover saat mouse berada di atas tombol
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#4a4a4a"))
            # Efek saat mouse meninggalkan tombol
            btn.bind("<Leave>", lambda e, b=btn, c=bg_color: b.config(bg=c))
            
            col += 1  # Pindah ke kolom berikutnya
            if col > 3:  # Jika sudah di kolom ke-4
                col = 0   # Kembali ke kolom pertama
                row += 1 # Pindah ke baris berikutnya
        
        # Konfigurasi grid untuk layout yang responsif
        for i in range(5):
            master.grid_rowconfigure(i, weight=1)
        for i in range(4):
            master.grid_columnconfigure(i, weight=1)
    
    def on_button_click(self, text):
        """Fungsi yang dipanggil saat tombol diklik"""
        current = self.equation.get()  # Ambil nilai persamaan saat ini
        
        if text == 'C':
            # Tombol Clear: Hapus semua isi display
            self.equation.set('')
        elif text == '=':
            # Tombol sama dengan: Hitung hasil persamaan
            try:
                # Ganti 'x' dengan '*' untuk evaluasi matematika
                expression = current.replace('x', '*')
                result = str(eval(expression))  # Evaluasi ekspresi matematika
                self.equation.set(result)      # Tampilkan hasil
            except:
                # Jika terjadi error, tampilkan pesan error
                self.equation.set('Error')
        else:
            # Tombol angka/operator
            # Cegah multiple operator berturut-turut
            if current and current[-1] in '+-x/' and text in '+-x/':
                # Ganti operator terakhir dengan yang baru
                self.equation.set(current[:-1] + text)
            else:
                # Tambahkan tombol yang ditekan ke display
                self.equation.set(current + text)

if __name__ == "__main__":
    root = Tk()  # Membuat instance Tkinter
    app = ModernCalculator(root)  # Membuat kalkulator
    root.mainloop()  # Menjalankan aplikasi