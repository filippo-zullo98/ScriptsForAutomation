import os
import psutil
import sys

def create_iso_windows():
    print("===================================================")
    print("💿 Windows ISO Creator (PS2 & DVD) 💿")
    print("===================================================")

    # 1. Trova il lettore CD-ROM
    drive_letter = None
    for part in psutil.disk_partitions():
        if 'cdrom' in part.opts:
            drive_letter = part.device.rstrip('\\')
            break

    if not drive_letter:
        print("❌ ERRORE: Nessun lettore CD/DVD rilevato.")
        return

    print(f"✅ Lettore trovato: {drive_letter}")

    # 2. Chiedi il nome del file di output
    file_name = input("Inserisci il nome del gioco (senza estensione): ").strip()
    if not file_name:
        file_name = "gioco_estratto"
    
    output_path = f"{file_name}.iso"

    # 3. Accesso grezzo al disco
    # Su Windows, il percorso fisico è \\.\LetteraUnità:
    raw_device_path = f"\\\\.\\{drive_letter}"

    print(f"🚀 Avvio estrazione da {raw_device_path}...")
    print("⏳ Nota: Il processo può richiedere tempo. Non chiudere la finestra.")

    try:
        # Apriamo il dispositivo fisico in lettura binaria
        with open(raw_device_path, 'rb') as disk:
            with open(output_path, 'wb') as iso_file:
                # Usiamo un buffer di 2048 byte (standard per settori DVD/ISO)
                buffer_size = 2048 * 512  # Leggiamo 1MB alla volta per velocità
                while True:
                    data = disk.read(buffer_size)
                    if not data:
                        break
                    iso_file.write(data)
                    
        print("\n" + "="*50)
        print(f"✅ OPERAZIONE COMPLETATA!")
        print(f"Il tuo file è pronto: {os.path.abspath(output_path)}")
        print("="*50)

    except PermissionError:
        print("\n❌ ERRORE DI PERMESSI!")
        print("Devi eseguire il terminale (o l'IDE) come AMMINISTRATORE.")
    except Exception as e:
        print(f"\n❌ Si è verificato un errore: {e}")

if __name__ == "__main__":
    create_iso_windows()
