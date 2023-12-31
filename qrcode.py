import qrcode  # Importa il modulo qrcode per generare codici QR.
from PIL import Image, ImageTk  # Importa le classi Image e ImageTk dal modulo PIL (Python Imaging Library) per lavorare con le immagini.
from pyzbar.pyzbar import decode  # Importa la funzione decode dal modulo pyzbar.pyzbar per decodificare i codici QR.
import tkinter as tk  # Importa il modulo tkinter per creare l'interfaccia utente.
from tkinter import filedialog  # Importa la classe filedialog dal modulo tkinter per aprire la finestra di dialogo dei file.
import webbrowser  # Importa il modulo webbrowser per aprire i collegamenti web.

# Definisce una funzione per generare un codice QR.
def genera_qr(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)  # Aggiunge i dati al codice QR.
    qr.make(fit=True)  # Crea il codice QR.
    img_pil = qr.make_image(fill='black', back_color='white')  # Crea un'immagine del codice QR.
    img_tk = ImageTk.PhotoImage(img_pil)  # Converte l'immagine PIL in un formato utilizzabile da tkinter.
    return img_tk, img_pil  # Restituisce l'immagine tkinter e l'immagine PIL.

# Definisce una funzione per leggere un codice QR.
def leggi_qr(nome_file):
    img = Image.open(nome_file)  # Apre l'immagine del codice QR.
    dati = decode(img)  # Decodifica il codice QR.
    for dato in dati:  # Per ogni dato nel codice QR...
        url = dato.data.decode("utf-8")  # Decodifica i dati in una stringa.
        if url.startswith("http://") or url.startswith("https://"):  # Se i dati sono un URL...
            webbrowser.open(url)  # Apri l'URL nel browser web.

# Definisce una funzione per generare un codice QR.
def genera():
    if hasattr(genera, "entry"):  # Se esiste già un campo di inserimento...
        genera.entry.destroy()  # Distruggilo.
        genera.ok_button.destroy()  # Distruggi anche il pulsante OK.
        genera.cancel_button.destroy()  # E il pulsante Annulla.

    bottone_leggi.pack_forget()  # Nasconde il pulsante Leggi.
    genera.entry = tk.Entry(frame_bottoni, width=50)  # Crea un nuovo campo di inserimento.
    genera.entry.pack(side='left')  # Posiziona il campo di inserimento a sinistra.
    genera.entry.insert(0, "https://translate.google.it/?hl=it")  # Inserisce un URL predefinito nel campo di inserimento.

    # Definisce una funzione per il pulsante OK.
    def ok():
        data = genera.entry.get()  # Ottiene i dati dal campo di inserimento.
        img_tk, img_pil = genera_qr(data)  # Genera un codice QR con i dati.
        mostra_qr(img_tk, img_pil)  # Mostra il codice QR.
        genera.entry.destroy()  # Distrugge il campo di inserimento.
        genera.ok_button.destroy()  # Distrugge il pulsante OK.
        genera.cancel_button.destroy()  # Distrugge il pulsante Annulla.
        bottone_leggi.pack(side='left')  # Mostra di nuovo il pulsante Leggi.

    genera.ok_button = tk.Button(frame_bottoni, text="OK", command=ok)  # Crea un pulsante OK.
    genera.ok_button.pack(side='left')  # Posiziona il pulsante OK a sinistra.

    # Crea un pulsante Annulla.
    genera.cancel_button = tk.Button(frame_bottoni, text="Annulla", command=lambda: [genera.entry.destroy(), genera.ok_button.destroy(), genera.cancel_button.destroy(), bottone_leggi.pack(side='left')])
    genera.cancel_button.pack(side='left')  # Posiziona il pulsante Annulla a sinistra.

# Definisce una funzione per mostrare un codice QR.
def mostra_qr(img_tk, img_pil):
    label.config(image=img_tk, bg='white')  # Configura l'etichetta per mostrare l'immagine del codice QR.
    label.image = img_tk  # Salva l'immagine tkinter nell'etichetta.
    label.image_pil = img_pil  # Salva l'immagine PIL nell'etichetta.
    if hasattr(mostra_qr, "bottone_salva"):  # Se esiste già un pulsante Salva...
        mostra_qr.bottone_salva.pack_forget()  # Nascondilo.
    bottone_salva = tk.Button(frame_bottoni, text="Salva QR Code", command=salva_qr)  # Crea un pulsante Salva.
    bottone_salva.pack(side='left')  # Posiziona il pulsante Salva a sinistra.
    mostra_qr.bottone_salva = bottone_salva  # Salva il pulsante Salva.

# Definisce una funzione per salvare un codice QR.
def salva_qr():
    nome_file = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png"), ("All Files", "*.*")])  # Chiede all'utente dove salvare il codice QR.
    if nome_file:  # Se l'utente ha scelto un percorso...
        label.image_pil.save(nome_file)  # Salva l'immagine PIL nel percorso scelto.

# Definisce una funzione per leggere un codice QR.
def leggi():
    nome_file = filedialog.askopenfilename()  # Chiede all'utente di scegliere un file.
    dati = leggi_qr(nome_file)  # Legge il codice QR dal file.

root = tk.Tk()  # Crea la finestra principale.
root.geometry('700x400')  # Imposta le dimensioni della finestra.
root.title("Genera/Leggi QRCODE")  # Imposta il titolo della finestra.

frame_bottoni = tk.Frame(root)  # Crea un frame per i pulsanti.
frame_bottoni.pack()  # Posiziona il frame nella finestra.

bottone_genera = tk.Button(frame_bottoni, text="Genera QR Code", command=genera)  # Crea un pulsante Genera.
bottone_genera.pack(side='left')  # Posiziona il pulsante Genera a sinistra.

bottone_leggi = tk.Button(frame_bottoni, text="Leggi QR Code", command=leggi)  # Crea un pulsante Leggi.
bottone_leggi.pack(side='left')  # Posiziona il pulsante Leggi a sinistra.

label = tk.Label(root)  # Crea un'etichetta per mostrare il codice QR.
label.pack()  # Posiziona l'etichetta nella finestra.

link_label = tk.Label(root, text="")  # Crea un'etichetta per mostrare il link.
link_label.pack()  # Posiziona l'etichetta nella finestra.

root.mainloop()  # Avvia il ciclo principale di tkinter.
