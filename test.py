import os
import time
import msvcrt
import sys
import random

def zeige_menue(auswahl):
    """Zeigt das Menü an und markiert die aktuelle Auswahl."""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=== DOWNLOAD MANAGER ===")
    print("Nutze 'W' (hoch) und 'S' (runter). Bestätige mit der ENTER-Taste.\n")
    
    optionen = [
        "[1] Download für Windows",
        "[2] Download für Desktop",
        "[3] Download für Neptune Bot Beta"
    ]
    
    for idx, option in enumerate(optionen):
        if idx == auswahl:
            print(f" > {option}")
        else:
            print(f"   {option}")


def hauptmenue():
    auswahl = 0
    zeige_menue(auswahl)
    
    while True:
        taste = msvcrt.getch()
        try:
            taste = taste.decode('utf-8').lower()
        except UnicodeDecodeError:
            continue
            
        if taste == 'w':  # Hoch
            auswahl = auswahl - 1
            if auswahl < 0:
                auswahl = 2
            zeige_menue(auswahl)
        elif taste == 's':  # Runter
            auswahl = auswahl + 1
            if auswahl > 2:
                auswahl = 0
            zeige_menue(auswahl)
        elif taste == '\r':  # ENTER-Taste
            if auswahl == 0:
                return "Windows"
            elif auswahl == 1:
                return "Desktop"
            else:
                return "Neptune Bot Beta"

def ordner_erstellen_und_pfad_holen():
    print("\n-------------------------------------------")
    print("Bitte gib den Pfad an, wo die Ordner erstellt werden sollen.")
    print("Beispiel: C:\\Users\\Name\\Desktop\\MeinDownload")
    print("-------------------------------------------")
    
    ziel_pfad = input("Pfad eingeben und mit ENTER bestätigen:\n> ").strip().strip('"').strip("'")
    
    if not os.path.exists(ziel_pfad):
        try:
            os.makedirs(ziel_pfad)
            print(f"\n[Info] Ziel-Verzeichnis erstellt unter: {ziel_pfad}")
        except Exception as e:
            print(f"\n[Fehler] Pfad konnte nicht erstellt werden: {e}")
            sys.exit()
            
    return ziel_pfad

def simuliere_download(ziel_pfad, modus):
    print("\n[Status] Download wird vorbereitet...")
    print("[Info] Bitte warten, dieser Vorgang dauert ca. 10 Sekunden.")
    print("-------------------------------------------")
    
    wartezeit_sekunden = 10 
    for i in range(wartezeit_sekunden):
        prozent = int(((i + 1) / wartezeit_sekunden) * 100)
        print(f"Lade Daten für {modus} herunter... {prozent}%", end="\r")
        time.sleep(1)
    
    print("\n\n[Status] Download abgeschlossen! Erstelle Ordnerstruktur...")
    
    # Alle 5 Ordner werden jetzt direkt NEBENEINANDER im Zielpfad erstellt (außerhalb voneinander)
    ordner_liste = [
        os.path.join(ziel_pfad, "Neptune Bot Beta"),
        os.path.join(ziel_pfad, "configs"),
        os.path.join(ziel_pfad, "dc"),
        os.path.join(ziel_pfad, "logs"),
        os.path.join(ziel_pfad, "plugins")
    ]
    
    # Alle Ordner auf der Festplatte erstellen
    for ordner in ordner_liste:
        if not os.path.exists(ordner):
            os.makedirs(ordner)
            
    # 2000 Dateien pro Ordner generieren
    anzahl_dateien = 2000
    
    for ordner in ordner_liste:
        ordner_name = os.path.basename(ordner)
        print(f"[Info] Erstelle {anzahl_dateien} Dateien in '{ordner_name}'... Bitte warten...")
        
        for i in range(1, anzahl_dateien + 1):
            dateiname = f"{ordner_name.lower().replace(' ', '_')}_datei_{i:04d}.txt"
            datei_pfad = os.path.join(ordner, dateiname)
            
            with open(datei_pfad, "w", encoding="utf-8") as f:
                zufalls_zahlen = "-".join([str(random.randint(1000, 9999)) for _ in range(3)])
                f.write(f"Kategorie: {ordner_name}\n")
                f.write(f"Dokument Nummer: {i}\n")
                f.write(f"Generierter Code: {zufalls_zahlen}\n")
                f.write(f"Zeitstempel: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        
    print(f"\n[Erfolg] Fertig! Alle Ordner wurden außerhalb voneinander in '{ziel_pfad}' angelegt.")
    print("Folgende Ordner wurden befüllt:")
    for ordner in ordner_liste:
        print(f" -> {ordner} ({anzahl_dateien} Dateien)")

# Hauptprogramm starten
if __name__ == "__main__":
    gewaehlter_modus = hauptmenue()
    print(f"\nDu hast ausgewählt: Download für {gewaehlter_modus}")
    
    ziel_ordner = ordner_erstellen_und_pfad_holen()
    simuliere_download(ziel_ordner, gewaehlter_modus)
    
    print("\nDas Programm ist beendet. Drücke eine Taste zum Schließen.")
    msvcrt.getch()
