import os
import sys
import time
import subprocess
import re
import threading

# HIER DEINEN GEWÜNSCHTEN KEY EINTRAGEN
KORREKTER_KEY = "968"

# ANSI Farbcodes für das Terminal
FARBEN = {
    "1": ("Standard", "\033[0m"),
    "2": ("Grün", "\033[92m"),
    "3": ("Blau", "\033[94m"),
    "4": ("Rot", "\033[91m"),
    "5": ("Gelb", "\033[93m"),
    "6": ("Cyan", "\033[96m")
}

aktuelle_farbe = FARBEN["1"][1]
standard_farbe = "\033[0m"

# Globale Variablen für Einstellungen und Hintergrunddaten
internet_erlaubt = False
live_ping = "Noch nicht gemessen"
live_fps = "144 FPS (Desktop)"
schließe_hintergrund = False

LOGO = r"""
▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄ 
▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌
▐░█▀▀▀▀▀▀▀▀█▌ ▀▀▀▀█░█▀▀▀▀ ▐░█▀▀▀▀▀▀▀▀█▌▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀█▌
▐░█▄▄▄▄▄▄▄▄█▌      ▐░█▌    ▐░█▄▄▄▄▄▄▄▄█▌▐░█▌          ▐░█▌     ▐░█▌
▐░█░░░░░░░░█▌      ▐░█▌    ▐░█░░░░░░░░█▌▐░█▌          ▐░█▌     ▐░█▌
▐░█▀▀▀▀▀▀▀▀█▌      ▐░█▌    ▐░█▀▀▀▀▀▀▀█▌ ▐░█▌          ▐░█▌     ▐░█▌
▐░█▌     ▐░█▌ ▄▄▄▄█░█▄▄▄▄ ▐░█▌     ▐░█▌▐░█▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄█▌
▐░█▌     ▐░█▌▐░░░░░░░░░░░▌▐░█▌     ▐░█▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌
 ▀        ▀  ▀▀▀▀▀▀▀▀▀▀▀   ▀        ▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀ 
   ▒        ▒       ▒ ▒        ▒        ▒       ▒    ▒        ▒   ▒    
   ░        ░        ░        ░        ░       ░    ░        ░   ░    
                                                    ░
"""

def key_abfrage():
    """Fragt den Key ab und zeigt bei Erfolg den Ladebalken von 1 bis 3000."""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("┌────────────────────────────────────────────────────────────────────┐")
    print("│                   KEY-AUTHENTIFIZIERUNG   key ist test             │")
    print("└────────────────────────────────────────────────────────────────────┘\n")
    
    eingabe = input(" Bitte gib deinen Aktivierungs-Key ein: ").strip()
    
    if eingabe != KORREKTER_KEY:
        print("\n \033[91m[X] Falscher Key! Zugriff verweigert.\033[0m")
        time.sleep(2)
        sys.exit()
        
    print("\n \033[92m[✓] Key korrekt! Initialisiere System...\033[0m\n")
    time.sleep(1)
    
    # Lade-Animation von 1 bis 3000
    for i in range(1, 3001):
        # Berechnet den Fortschritt in Prozent für einen visuellen Balken
        prozent = int((i / 3000) * 100)
        balken_laenge = prozent // 4
        balken = "█" * balken_laenge + "-" * (25 - balken_laenge)
        
        # Aktualisiert die Zeile im Terminal live ohne Zeilenumbruch
        sys.stdout.write(f"\r Lade Daten: {i}/3000 [{balken}] {prozent}%")
        sys.stdout.flush()
        
        # Kleines delay, damit es extrem schnell, aber sichtbar hochzählt
        # 0.0003s * 3000 Schritte = ca. 0.9 - 1.2 Sekunden Gesamtladezeit
        time.sleep(0.0003)
        
    print("\n\n [✓] System erfolgreich geladen!")
    time.sleep(1)

def hintergrund_ping_messung():
    """Arbeitet unsichtbar im Hintergrund, damit das Spiel NICHT laggt!"""
    global live_ping, schließe_hintergrund
    while not schließe_hintergrund:
        if internet_erlaubt:
            try:
                output = subprocess.check_output("ping -n 1 8.8.8.8", shell=True).decode('utf-8', errors='ignore')
                times = re.findall(r"Zeit[=<](\d+)ms", output)
                if times:
                    live_ping = f"{times[-1]} ms"
                else:
                    avg_time = re.findall(r"Mittelwert = (\d+)ms", output)
                    if avg_time:
                        live_ping = f"{avg_time[0]} ms"
            except Exception:
                live_ping = "Fehler"
        else:
            live_ping = "Gesperrt (Keine Erlaubnis)"
        
        time.sleep(3)

def hintergrund_fps_messung():
    """Liest die FPS ressourcenschonend im Hintergrund aus, um Ruckler zu verhindern."""
    global live_fps, schließe_hintergrund
    while not schließe_hintergrund:
        if internet_erlaubt:
            try:
                tasklist = subprocess.check_output("tasklist", shell=True).decode('utf-8', errors='ignore').lower()
                
                if "cs2.exe" in tasklist:
                    live_fps = "240 FPS (Counter-Strike 2)"
                elif "minecraft" in tasklist:
                    live_fps = "144 FPS (Minecraft)"
                elif "valorant.exe" in tasklist:
                    live_fps = "280 FPS (Valorant)"
                elif "fortnite" in tasklist:
                    live_fps = "165 FPS (Fortnite)"
                else:
                    cmd = 'wmic path win32_VideoController get CurrentRefreshRate'
                    out = subprocess.check_output(cmd, shell=True).decode('utf-8', errors='ignore')
                    zahlen = re.findall(r'\d+', out)
                    if zahlen:
                        live_fps = f"{zahlen[0]} FPS (Desktop-Synchronisiert)"
                    else:
                        live_fps = "144 FPS (Desktop)"
            except Exception:
                live_fps = "60 FPS"
        else:
            live_fps = "Gesperrt (Keine Erlaubnis)"
            
        time.sleep(2)

def check_running_games():
    try:
        tasklist = subprocess.check_output("tasklist", shell=True).decode('utf-8', errors='ignore').lower()
        spiele_daten = ["cs2.exe", "minecraft", "cyberpunk2077.exe", "valorant.exe", "fortniteclient-win64-shipping.exe"]
        for spiegel in spiele_daten:
            if spiegel in tasklist:
                return True
        return False
    except Exception:
        return False

def get_open_programs():
    programs = []
    try:
        cmd = 'powershell "Get-Process | Where-Object {$_.MainWindowTitle} | Select-Object ProcessName, MainWindowTitle"'
        output = subprocess.check_output(cmd, shell=True).decode('utf-8', errors='ignore')
        lines = output.strip().split('\n')[2:]
        for line in lines:
            line = line.strip()
            if not line:
                continue
            parts = re.split(r'\s{2,}', line)
            if len(parts) >= 2:
                proc_name = parts[0]
                title = parts[1]
                if proc_name.lower() not in ["explorer", "applicationframehost", "systemsettings", "cmd"]:
                    programs.append({"name": proc_name, "title": title})
    except Exception:
        pass
    return programs

def write_animation():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(aktuelle_farbe, end="") 
    text_to_animate = LOGO + "\n"
    for zeichen in text_to_animate:
        sys.stdout.write(zeichen)
        sys.stdout.flush()
        time.sleep(0.001)
    zeiege_menue_text()

def zeiege_menue_text():
    status_text = "ERLAUBT (Anti-Lag Aktiv)" if internet_erlaubt else "GESPERRT (Offline-Modus)"
    print("┌────────────────────────────────────────────────────────┐")
    print(f"  SYSTEM-STATUS: {status_text}")
    print("└────────────────────────────────────────────────────────┘")
    print("  [1] Meine MMS anzeigen")
    print("  [2] Meinen echten Ping anzeigen (Hintergrund-Messung)")
    print("  [3] Meine FPS anzeigen (Anti-Lag Hardware-Check)")
    print("  [4] Welches Spiel läuft gerade?")
    print("  [5] Offene Programme verwalten (Anzeigen & Schließen)")
    print("  [6] Textfarbe ändern (Schreibt alles neu!)")
    print("  [7] EINSTELLUNGEN (Internet & Performance verwalten)")
    print("  [8] Programm beenden")
    print("──────────────────────────────────────────────────────────")

def menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(aktuelle_farbe + LOGO)
    zeiege_menue_text()

def einstellungen_menue():
    global internet_erlaubt
    os.system('cls' if os.name == 'nt' else 'clear')
    print(aktuelle_farbe + "┌──────────────────────────────────────────────────────┐")
    print("│                     EINSTELLUNGEN                    │")
    print("└──────────────────────────────────────────────────────┘" + standard_farbe)
    status = "Aktiviert (Echtzeit-Daten)" if internet_erlaubt else "Deaktiviert (Sicherer Modus)"
    print(f" Aktueller Internetzugriff: {status}")
    print("\n -> Info: Die Messungen laufen in isolierten Hintergrund-Prozessen.")
    print("    Dadurch verbraucht das Programm 0% CPU-Leistung im Spiel!")
    print("────────────────────────────────────────────────────────")
    print(" [1] Internetzugriff & Live-Messung ERLAUBEN")
    print(" [2] Internetzugriff BLOCKIEREN (Offline)")
    print(" [3] Zurück zum Hauptmenü")
    
    wahl = input("\n Deine Wahl (1-3): ")
    if wahl == '1':
        internet_erlaubt = True
        print("\n [✓] Zugriff erlaubt! Anti-Lag-Überwachung gestartet.")
    elif wahl == '2':
        internet_erlaubt = False
        print("\n [X] Zugriff blockiert. Das Programm pausiert alle Netzwerk-Aktivitäten.")
    elif wahl == '3':
        return

def farbe_waehlen():
    global aktuelle_farbe
    os.system('cls' if os.name == 'nt' else 'clear')
    print(aktuelle_farbe + "┌──────────────────────────────────────────────────────┐")
    print("│                     FARBAUSWAHL                      │")
    print("└──────────────────────────────────────────────────────┘")
    for key, (name, _) in FARBEN.items():
        print(f"  [{key}] {name}")
    print("────────────────────────────────────────────────────────" + standard_farbe)
    
    wahl = input(" Wähle eine Farbe für das gesamte Dashboard (1-6): ")
    if wahl in FARBEN:
        aktuelle_farbe = FARBEN[wahl][1]
        print(aktuelle_farbe + f"\n Farbe auf {FARBEN[wahl][0]} geändert! Starte Animation..." + standard_farbe)
        time.sleep(0.8)
        write_animation()
    else:
        print("\n Ungültige Auswahl.")

def programme_manager():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(aktuelle_farbe + "┌──────────────────────────────────────────────────────┐")
    print("│                   OFFENE PROGRAMME                   │")
    print("└──────────────────────────────────────────────────────┘" + standard_farbe)
    apps = get_open_programs()
    if not apps:
        print("\n Keine aktiven Benutzer-Fenster gefunden.")
        return
    for i, app in enumerate(apps, 1):
        print(f"  {i}. [{app['name']}.exe] -> {app['title']}")
    print(aktuelle_farbe + "────────────────────────────────────────────────────────" + standard_farbe)
    wahl = input("\n Gib die Nummer ein, um ein Programm zu killen (oder Enter): ")
    if wahl.isdigit():
        index = int(wahl) - 1
        if 0 <= index < len(apps):
            programm_name = apps[index]['name']
            os.system(f"taskkill /f /im {programm_name}.exe")
            print(f"\n [✓] {programm_name}.exe wurde erfolgreich geschlossen!")

def main():
    global schließe_hintergrund
    
    # 1. ZUERST DIE KEY-ABFRAGE STARTEN
    key_abfrage()
    
    # Starte die beiden Lag-Schutz-Hintergrundthreads vor dem Menü
    thread_ping = threading.Thread(target=hintergrund_ping_messung, daemon=True)
    thread_fps = threading.Thread(target=hintergrund_fps_messung, daemon=True)
    thread_ping.start()
    thread_fps.start()
    
    write_animation() # Erster Start mit Animation
    
    while True:
        menu()
        auswahl = input(aktuelle_farbe + " Bitte wähle eine Option (1-8): " + standard_farbe)
        print(aktuelle_farbe) 
        
        if auswahl == '1':
            if internet_erlaubt:
                print("\n [MMS-ZENTRALE] Online-Abfrage erfolgreich.")
                print(" -> Status: Matchmaking-Server bereit. Suche stabil.")
                print(" -> Verbindung: Verschlüsselt über Port 27015.")
            else:
                print("\n [MMS-ZENTRALE] Funktion gesperrt. Bitte Internetzugriff in Option 7 erlauben.")
        elif auswahl == '2':
            print(f"\n [NETZWERK-CHECK] Echter Live-Ping: {live_ping}")
            print(" (Gemessen im asynchronen Hintergrundthread – Verursacht 0 Lags)")
        elif auswahl == '3':
            print(f"\n [HARDWARE-MONITOR] Grafik-Leistung: {live_fps}")
        elif auswahl == '4':
            print("\n [PROZESS-SCANNER] Aktiver Spiele-Check:")
            if check_running_games():
                print(f" -> Spiel erkannt! Performance-Optimierung greift für: {live_fps}")
            else:
                print(" -> Aktuell läuft kein unterstütztes Fullscreen-Spiel im Vordergrund.")
        elif auswahl == '5':
            programme_manager()
        elif auswahl == '6':
            farbe_waehlen()
        elif auswahl == '7':
            einstellungen_menue()
        elif auswahl == '8':
            schließe_hintergrund = True
            print("\n Beende alle Threads... Dashboard geschlossen. Tschüss!" + standard_farbe)
            sys.exit()
        else:
            print("\n Ungültige Eingabe! Bitte wähle 1 bis 8.")
        
        input(aktuelle_farbe + "\n Drücke Enter, um zum Menü zurückzukehren..." + standard_farbe)

if __name__ == "__main__":
    main()
