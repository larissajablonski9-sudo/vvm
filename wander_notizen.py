import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import os

class WanderNotizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Wander-Notizbuch")
        self.root.geometry("500x600")
        self.root.configure(bg="#1e1e1e")  # Dunkler Hintergrund

        # Stil für die UI-Elemente
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TLabel", background="#1e1e1e", foreground="#ffffff", font=("Helvetica", 12))
        self.style.configure("TButton", background="#333333", foreground="#ffffff", font=("Helvetica", 10, "bold"))
        self.style.map("TButton", background=[("active", "#4d4d4d")])

        self.create_widgets()

    def create_widgets(self):
        # Titel
        self.title_label = ttk.Label(self.root, text="Meine Wander-Notizen", font=("Helvetica", 16, "bold"))
        self.title_label.pack(pady=15)

        # Eingabefeld für den Titel der Wanderung / Route
        self.route_label = ttk.Label(self.root, text="Route / Ort:")
        self.route_label.pack(anchor="w", px=20, pady=2)
        
        self.route_entry = tk.Entry(self.root, bg="#2d2d2d", fg="#ffffff", insertbackground="white", bd=0, font=("Helvetica", 11))
        self.route_entry.pack(fill="x", padx=20, ipady=8, pady=5)

        # Eingabefeld für die eigentlichen Notizen
        self.note_label = ttk.Label(self.root, text="Notizen (Wetter, Highlights, Ausrüstung...):")
        self.note_label.pack(anchor="w", px=20, pady=2)

        self.note_text = tk.Text(self.root, bg="#2d2d2d", fg="#ffffff", insertbackground="white", bd=0, font=("Helvetica", 11), wrap="word")
        self.note_text.pack(fill="both", expand=True, padx=20, pady=5)

        # Button zum Speichern
        self.save_button = ttk.Button(self.root, text="Notiz Speichern", command=self.speichere_notiz)
        self.save_button.pack(fill="x", padx=20, ipady=10, pady=20)

    def speichere_notiz(self):
        route = self.route_entry.get().strip()
        inhalt = self.note_text.get("1.0", tk.END).strip()

        if not route or not inhalt:
            messagebox.showwarning("Fehler", "Bitte fülle sowohl die Route als auch die Notiz aus!")
            return

        # Erstellt einen sauberen Dateinamen aus dem Routennamen
        dateiname = "".join(c for c in route if c.isalnum() or c in (" ", "_", "-")).rstrip()
        dateiname = f"Wanderung_{dateiname.replace(' ', '_')}.txt"

        try:
            with open(dateiname, "w", encoding="utf-8") as file:
                file.write(f"ROUTE: {route}\n")
                file.write("="*30 + "\n")
                file.write(inhalt)
            
            messagebox.showinfo("Erfolg", f"Deine Notiz wurde als '{dateiname}' gespeichert!")
            
            # Felder nach dem Speichern leeren
            self.route_entry.delete(0, tk.END)
            self.note_text.delete("1.0", tk.END)
            
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Speichern: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WanderNotizApp(root)
    root.mainloop()
