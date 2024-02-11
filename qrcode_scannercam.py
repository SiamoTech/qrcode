import cv2  # Importa la libreria OpenCV per il trattamento delle immagini.
import qrcode  # Importa la libreria per la generazione dei codici QR.
from PIL import Image, ImageTk  # Importa le classi Image e ImageTk dalla libreria PIL (Python Imaging Library) per la manipolazione delle immagini.
from pyzbar.pyzbar import decode  # Importa la funzione decode dalla libreria pyzbar per decodificare i codici QR.
import tkinter as tk  # Importa la libreria tkinter per la creazione dell'interfaccia grafica.
from tkinter import filedialog  # Importa la classe filedialog da tkinter per aprire la finestra di dialogo dei file.
import webbrowser  # Importa la libreria webbrowser per aprire i link nel browser web.

ultimo_url = ""  # Inizializza la variabile ultimo_url come stringa vuota. Questa variabile conterrà l'ultimo URL riconosciuto da un codice QR.
qr_riconosciuto = False  # Inizializza la variabile qr_riconosciuto come False. Questa variabile indica se un codice QR è stato riconosciuto o meno.
img_qr = None  # Inizializza la variabile img_qr come None. Questa variabile conterrà l'immagine del codice QR.


def genera_qr(data):  # Definisce la funzione genera_qr che genera un'immagine di un codice QR a partire da una stringa di dati.
    qr = qrcode.QRCode(  # Crea un oggetto QRCode.
        version=1,  # Imposta la versione del codice QR come 1.
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Imposta il livello di correzione degli errori come basso.
        box_size=10,  # Imposta la dimensione di ogni box del codice QR come 10.
        border=4,  # Imposta la dimensione del bordo del codice QR come 4.
    )
    qr.add_data(data)  # Aggiunge i dati al codice QR.
    qr.make(fit=True)  # Crea il codice QR.
    img = qr.make_image(fill='black', back_color='white')  # Crea un'immagine del codice QR con i box neri e lo sfondo bianco.
    return img  # Restituisce l'immagine del codice QR.

def leggi_qr(nome_file):  # Definisce la funzione leggi_qr che legge un codice QR da un'immagine.
    global ultimo_url, qr_riconosciuto  # Dichiarazione delle variabili globali ultimo_url e qr_riconosciuto.
    img = Image.open(nome_file)  # Apre l'immagine del file.
    dati = decode(img)  # Decodifica i dati del codice QR nell'immagine.
    if dati:  # Se ci sono dati nel codice QR...
        print("QR code riconosciuto!")  # Stampa un messaggio che indica che il codice QR è stato riconosciuto.
        for dato in dati:  # Per ogni dato nel codice QR...
            url = dato.data.decode("utf-8")  # Decodifica il dato in una stringa UTF-8.
            print("URL riconosciuto: ", url)  # Stampa l'URL riconosciuto.
            if url.startswith("http://") or url.startswith("https://"):  # Se l'URL inizia con "http://" o "https://", allora è un URL valido.
                link_label.config(text=url)  # Configura il testo del link_label con l'URL.
                if not webbrowser.open(url):  # Apri l'URL nel browser web. Se non riesce, stampa un messaggio di errore.
                    print("Errore nell'apertura del browser web.")
                ultimo_url = url  # Imposta l'ultimo URL come l'URL corrente.
                qr_riconosciuto = True  # Imposta qr_riconosciuto come True perché un codice QR è stato riconosciuto.
                label.config(image='')  # Rimuove l'immagine dal label.
        qr_riconosciuto = False  # Imposta qr_riconosciuto come False perché non ci sono più codici QR da riconoscere.
        return True  # Restituisce True perché un codice QR è stato riconosciuto.
    else:  # Se non ci sono dati nel codice QR...
        print("Nessun QR code riconosciuto.")  # Stampa un messaggio che indica che nessun codice QR è stato riconosciuto.
        return False  # Restituisce False perché nessun codice QR è stato riconosciuto.

def genera():  # Definisce la funzione genera che genera un codice QR.
    entry = tk.Entry(frame_bottoni, width=50)  # Crea un campo di inserimento testuale nel frame_bottoni con una larghezza di 50 caratteri.
    entry.pack(side='left')  # Posiziona il campo di inserimento testuale a sinistra nel frame_bottoni.
    entry.insert(0, "")  # Inserisce l'URL di Google Translate come testo predefinito nel campo di inserimento testuale.

    def ok():  # Definisce la funzione ok che viene chiamata quando si fa clic sul pulsante OK.
        data = entry.get()  # Ottiene i dati dal campo di inserimento testuale.
        global img_qr  # Dichiarazione della variabile globale img_qr.
        img_qr = genera_qr(data)  # Genera un'immagine di un codice QR a partire dai dati e la salva in img_qr.
        imgtk = ImageTk.PhotoImage(image=img_qr)  # Crea un'immagine tkinter a partire dall'immagine del codice QR.
        label.config(image=imgtk, bg='white')  # Configura l'immagine e lo sfondo del label con l'immagine tkinter e il colore bianco.
        label.image = imgtk  # Imposta l'immagine del label come l'immagine tkinter.
        entry.destroy()  # Distrugge il campo di inserimento testuale.
        ok_button.destroy()  # Distrugge il pulsante OK.
        cancel_button.destroy()  # Distrugge il pulsante Annulla.
        bottone_salva = tk.Button(frame_bottoni, text="Salva QR Code", command=salva_qr)  # Crea un pulsante Salva QR Code nel frame_bottoni che chiama la funzione salva_qr quando si fa clic su di esso.
        bottone_salva.pack(side='left')  # Posiziona il pulsante Salva QR Code a sinistra nel frame_bottoni.

    ok_button = tk.Button(frame_bottoni, text="OK", command=ok)  # Crea un pulsante OK nel frame_bottoni che chiama la funzione ok quando si fa clic su di esso.
    ok_button.pack(side='left')  # Posiziona il pulsante OK a sinistra nel frame_bottoni.

    cancel_button = tk.Button(frame_bottoni, text="Annulla", command=lambda: [entry.destroy(), ok_button.destroy(), cancel_button.destroy()])  # Crea un pulsante Annulla nel frame_bottoni che distrugge il campo di inserimento testuale, il pulsante OK e se stesso quando si fa clic su di esso.
    cancel_button.pack(side='left')  # Posiziona il pulsante Annulla a sinistra nel frame_bottoni.


def mostra_qr(img):  # Definisce la funzione mostra_qr che mostra un'immagine di un codice QR.
    imgtk = ImageTk.PhotoImage(img)  # Crea un'immagine tkinter a partire dall'immagine del codice QR.
    label.config(image=imgtk, bg='white')  # Configura l'immagine e lo sfondo del label con l'immagine tkinter e il colore bianco.
    label.image = imgtk  # Imposta l'immagine del label come l'immagine tkinter.
    bottone_salva = tk.Button(frame_bottoni, text="Salva QR Code", command=salva_qr)  # Crea un pulsante Salva QR Code nel frame_bottoni che chiama la funzione salva_qr quando si fa clic su di esso.
    bottone_salva.pack(side='left')  # Posiziona il pulsante Salva QR Code a sinistra nel frame_bottoni.

def salva_qr():
    nome_file = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png"), ("All Files", "*.*")])  # Chiede all'utente dove salvare il codice QR.
    if nome_file:  # Se l'utente ha scelto un percorso...
        global img_qr  # Dichiarazione della variabile globale img_qr.
        img_qr.save(nome_file)  # Salva l'immagine PIL nel percorso scelto.

def leggi():  # Definisce la funzione leggi che legge un codice QR da un'immagine.
    nome_file = filedialog.askopenfilename()  # Apre una finestra di dialogo per aprire il file e restituisce il nome del file.
    dati = leggi_qr(nome_file)  # Legge un codice QR dall'immagine del file e restituisce i dati del codice QR.
    print(dati)  # Stampa i dati del codice QR.

def leggi_da_fotocamera():  # Definisce la funzione leggi_da_fotocamera che legge un codice QR da una fotocamera.
    global qr_riconosciuto  # Dichiarazione della variabile globale qr_riconosciuto.
    qr_riconosciuto = False  # Imposta qr_riconosciuto come False perché non ci sono più codici QR da riconoscere.
    cap = cv2.VideoCapture(1)  # Apre la fotocamera con l'indice 1.

    def mostra_frame():  # Definisce la funzione mostra_frame che mostra un frame dalla fotocamera.
        if not qr_riconosciuto:  # Se non è stato riconosciuto un codice QR...
            ret, frame = cap.read()  # Legge un frame dalla fotocamera.
            if ret:  # Se la lettura del frame è stata riuscita...
                cv2.imwrite('frame.jpg', frame)  # Salva il frame come un'immagine JPEG.
                img = Image.open('frame.jpg')  # Apre l'immagine del frame.
                imgtk = ImageTk.PhotoImage(image=img)  # Crea un'immagine tkinter a partire dall'immagine del frame.
                label.config(image=imgtk)  # Configura l'immagine del label con l'immagine tkinter.
                label.image = imgtk  # Imposta l'immagine del label come l'immagine tkinter.
                if not leggi_qr('frame.jpg'):  # Se non è stato riconosciuto un codice QR nell'immagine del frame...
                    label.after(10, mostra_frame)  # Chiama la funzione mostra_frame dopo 10 millisecondi.
                else:  # Se è stato riconosciuto un codice QR nell'immagine del frame...
                    cap.release()  # Rilascia la fotocamera.
                    label.config(image='')  # Rimuove l'immagine dal label.

    mostra_frame()  # Chiama la funzione mostra_frame.

root = tk.Tk()  # Crea la finestra principale dell'applicazione.
root.geometry('700x400')  # Imposta le dimensioni della finestra principale come 700x400 pixel.
root.title("Genera/Leggi QRCODE")  # Imposta il titolo della finestra principale come "Genera/Leggi QRCODE".

frame_bottoni = tk.Frame(root)  # Crea un frame per i pulsanti nella finestra principale.
frame_bottoni.pack()  # Posiziona il frame per i pulsanti nella finestra principale.

bottone_genera = tk.Button(frame_bottoni, text="Genera QR Code",
                           command=genera)  # Crea un pulsante Genera QR Code nel frame per i pulsanti che chiama la funzione genera quando si fa clic su di esso.
bottone_genera.pack(side='left')  # Posiziona il pulsante Genera QR Code a sinistra nel frame per i pulsanti.

bottone_leggi = tk.Button(frame_bottoni, text="Leggi QR Code",
                          command=leggi)  # Crea un pulsante Leggi QR Code nel frame per i pulsanti che chiama la funzione leggi quando si fa clic su di esso.
bottone_leggi.pack(side='left')  # Posiziona il pulsante Leggi QR Code a sinistra nel frame per i pulsanti.

bottone_fotocamera = tk.Button(frame_bottoni, text="Leggi QR Code da fotocamera",
                               command=leggi_da_fotocamera)  # Crea un pulsante Leggi QR Code da fotocamera nel frame per i pulsanti che chiama la funzione leggi_da_fotocamera quando si fa clic su di esso.
bottone_fotocamera.pack(
    side='left')  # Posiziona il pulsante Leggi QR Code da fotocamera a sinistra nel frame per i pulsanti.

label = tk.Label(root)  # Crea un label nella finestra principale.
label.pack()  # Posiziona il label nella finestra principale.

link_label = tk.Label(root, text="")  # Crea un label per i link nella finestra principale con il testo vuoto.
link_label.pack()  # Posiziona il label per i link nella finestra principale.

root.mainloop()  # Avvia il ciclo principale dell'applicazione.
