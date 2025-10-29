# build_exe_32bit_FIXED.py
# Script ÎMBUNĂTĂȚIT pentru crearea executabilului 32-bit compatibil cu Windows 7 și XP

"""
INSTRUCȚIUNI IMPORTANTE PENTRU BUILD 32-BIT:

⚠️ ATENȚIE: Pentru a crea un executabil 32-bit funcțional, TREBUIE:

1. Instalează Python 32-bit (nu 64-bit!):
   - Descarcă de la: https://www.python.org/downloads/
   - Alege versiunea 3.8.10 (32-bit) pentru compatibilitate maximă cu Windows 7/XP
   - La instalare, bifează "Add Python to PATH"

2. Verifică că rulezi Python 32-bit:
   python -c "import platform; print(platform.architecture())"
   # Trebuie să afișeze: ('32bit', ...)

3. Instalează dependențele în Python 32-bit:
   pip install paramiko requests pyautogui pyinstaller pillow pygetwindow

4. Rulează acest script CU PYTHON 32-BIT:
   python build_exe_32bit_FIXED.py

5. Testează executabilul pe Windows 7 sau XP

NOTĂ: Dacă compilezi pe Windows 10/11 64-bit, va crea un executabil 64-bit chiar dacă
      folosești flaguri 32-bit. Trebuie să compilezi PE UN SISTEM CU PYTHON 32-BIT!
"""

import PyInstaller.__main__
import os
import sys
import platform

def check_python_architecture():
    """Verifică dacă Python-ul este 32-bit."""
    arch = platform.architecture()[0]
    is_32bit = arch == '32bit'
    
    print("=" * 60)
    print("VERIFICARE ARHITECTURĂ PYTHON")
    print("=" * 60)
    print(f"Arhitectură Python: {arch}")
    print(f"Versiune Python: {sys.version}")
    print(f"Platform: {platform.platform()}")
    print(f"Machine: {platform.machine()}")
    print("=" * 60)
    
    if not is_32bit:
        print("\n⚠️  AVERTISMENT: Python-ul tău este 64-bit!")
        print("Pentru un executabil 32-bit funcțional, trebuie să folosești Python 32-bit.")
        print("\nVrei să continui oricum? (Executabilul poate să nu funcționeze pe Windows 7/XP)")
        response = input("Continuă? (da/nu): ").strip().lower()
        if response not in ['da', 'yes', 'y']:
            print("Build anulat.")
            sys.exit(1)
        print("\n⚠️  Continuare cu Python 64-bit... Executabilul va fi 64-bit!")
    else:
        print("\n✓ Python 32-bit detectat! Perfect pentru Windows 7/XP!")
    
    return is_32bit

def create_icon():
    """Creează o iconiță simplă pentru aplicație."""
    try:
        from PIL import Image, ImageDraw

        # Creează o iconiță 256x256
        img = Image.new('RGBA', (256, 256), color=(52, 152, 219, 255))
        draw = ImageDraw.Draw(img)

        # Desenează un server/computer
        draw.rectangle([64, 80, 192, 176], fill=(255, 255, 255, 255))
        draw.rectangle([80, 96, 176, 112], fill=(46, 204, 113, 255))
        draw.rectangle([80, 128, 176, 144], fill=(52, 152, 219, 255))
        draw.ellipse([112, 188, 144, 220], fill=(255, 255, 255, 255))

        img.save('aleph_icon_autologin_32bit_fixed.ico', format='ICO')
        print("Iconita creata: aleph_icon_autologin_32bit_fixed.ico")
        return 'aleph_icon_autologin_32bit_fixed.ico'
    except Exception as e:
        print(f"Nu s-a putut crea iconita: {e}")
        return None

def build_executable():
    """Construiește executabilul folosind PyInstaller."""

    print("\n" + "=" * 60)
    print("CREARE EXECUTABIL ALEPH MONITOR - 32-BIT (FIXED)")
    print("=" * 60)

    # Verifică arhitectura Python
    is_32bit = check_python_architecture()

    # Creează iconița
    icon_path = create_icon()

    # Configurație PyInstaller OPTIMIZATĂ pentru 32-bit
    pyinstaller_args = [
        'monitor-server-autologin-32bit.py',  # Fișierul principal
        '--onefile',                          # Un singur fișier executabil
        '--windowed',                         # Fără consolă (GUI mode)
        '--name=AlephMonitor-AutoLogin-32bit-FIXED',  # Numele executabilului
        '--clean',                            # Curăță fișierele temporare
        '--noconfirm',                        # Nu cere confirmare
        '--noupx',                            # Dezactivează UPX (mai bună compatibilitate cu Windows vechi)
    ]

    # Adaugă iconița dacă există
    if icon_path and os.path.exists(icon_path):
        pyinstaller_args.append(f'--icon={icon_path}')

    # Excluderi pentru a reduce dimensiunea și a îmbunătăți compatibilitatea
    excluded_modules = [
        'PIL.ImageQt',  # Nu e necesar pentru Windows 7/XP
        'PyQt5',        # Nu e folosit
        'PyQt6',        # Nu e folosit
        'PySide2',      # Nu e folosit
        'PySide6',      # Nu e folosit
        'numpy',        # Poate cauza probleme pe sisteme vechi
        'matplotlib',   # Nu e folosit
        'scipy',        # Nu e folosit
    ]

    for module in excluded_modules:
        pyinstaller_args.extend(['--exclude-module', module])

    # Adaugă metadata
    pyinstaller_args.extend([
        '--version-file=version_info_autologin_32bit_fixed.txt',
    ])

    # Hidden imports pentru a asigura că toate modulele necesare sunt incluse
    hidden_imports = [
        'paramiko',
        'requests',
        'tkinter',
        'threading',
        'webbrowser',
        'logging',
        'datetime',
    ]

    for module in hidden_imports:
        pyinstaller_args.extend(['--hidden-import', module])

    print("\nPornire build PyInstaller...\n")
    print("Argumente PyInstaller:")
    for arg in pyinstaller_args:
        print(f"  {arg}")
    print()

    try:
        PyInstaller.__main__.run(pyinstaller_args)

        print("\n" + "=" * 60)
        print("EXECUTABIL CREAT CU SUCCES!")
        print("=" * 60)
        
        exe_path = os.path.abspath('dist/AlephMonitor-AutoLogin-32bit-FIXED.exe')
        print(f"\nLocatie: {exe_path}")
        
        # Afișează dimensiunea fișierului
        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"Dimensiune: {size_mb:.2f} MB")
        
        print("\nINSTRUCTIUNI TESTARE:")
        print("   1. Copiază executabilul pe un calculator Windows 7 sau XP")
        print("   2. Rulează executabilul și verifică dacă pornește")
        print("   3. Verifică log-ul: aleph_monitor.log pentru erori")
        
        if not is_32bit:
            print("\n⚠️  AVERTISMENT IMPORTANT:")
            print("   Executabilul a fost compilat cu Python 64-bit!")
            print("   Va funcționa DOAR pe Windows 64-bit (Windows 7 64-bit, Windows 10/11)")
            print("   NU va funcționa pe Windows XP sau Windows 7 32-bit!")
            print("\n   Pentru Windows 7/XP 32-bit, trebuie să recompilezi cu Python 32-bit!")
        else:
            print("\n✓ Executabilul a fost compilat cu Python 32-bit!")
            print("  Ar trebui să funcționeze pe:")
            print("    - Windows XP (32-bit)")
            print("    - Windows 7 (32-bit)")
            print("    - Windows 7 (64-bit)")
            print("    - Windows 10/11 (64-bit)")
        
        print("\nIMPORTANT:")
        print("   - Executabilul contine parola SSH (criptata in exe)")
        print("   - Utilizator implicit: admin / admin123")
        print("   - Catalog.exe trebuie să existe la: C:\\AL500\\catalog\\bin\\Catalog.exe")
        print("   - Restrictii de timp: NU poate fi lansat intre 23:00 PM si 02:00 AM")
        print("\n" + "=" * 60)

    except Exception as e:
        print(f"\nEROARE la creare executabil: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def create_version_info():
    """Creează fișier cu informații despre versiune."""
    version_info = """# UTF-8
#
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 2, 0, 0),
    prodvers=(1, 2, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Biblioteca'),
        StringStruct(u'FileDescription', u'Monitor Server ALEPH - Auto Login 32-bit FIXED'),
        StringStruct(u'FileVersion', u'1.2.0.0'),
        StringStruct(u'InternalName', u'AlephMonitor-AutoLogin-32bit-FIXED'),
        StringStruct(u'LegalCopyright', u'© 2025'),
        StringStruct(u'OriginalFilename', u'AlephMonitor-AutoLogin-32bit-FIXED.exe'),
        StringStruct(u'ProductName', u'ALEPH Server Monitor - Auto Login 32-bit'),
        StringStruct(u'ProductVersion', u'1.2.0.0')])
      ]
    ),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
"""

    try:
        with open('version_info_autologin_32bit_fixed.txt', 'w', encoding='utf-8') as f:
            f.write(version_info)
        print("Fisier versiune creat: version_info_autologin_32bit_fixed.txt")
    except Exception as e:
        print(f"Nu s-a putut crea fisierul de versiune: {e}")

def create_test_script():
    """Creează un script de test pentru verificarea compatibilității."""
    test_script = """# test_compatibility.py
# Script pentru testarea compatibilității pe Windows 7/XP

import sys
import platform
import tkinter as tk
from tkinter import messagebox

def test_system():
    info = []
    info.append(f"Python Version: {sys.version}")
    info.append(f"Platform: {platform.platform()}")
    info.append(f"Machine: {platform.machine()}")
    info.append(f"Architecture: {platform.architecture()[0]}")
    info.append(f"Windows Version: {platform.win32_ver()}")
    
    # Test Tkinter
    try:
        root = tk.Tk()
        root.title("Test Compatibilitate")
        root.geometry("400x300")
        
        text = "\\n".join(info)
        label = tk.Label(root, text=text, justify=tk.LEFT, padx=20, pady=20)
        label.pack()
        
        btn = tk.Button(root, text="OK - Sistemul este compatibil!", 
                       command=root.destroy, padx=20, pady=10)
        btn.pack(pady=20)
        
        root.mainloop()
        return True
    except Exception as e:
        print(f"Eroare: {e}")
        return False

if __name__ == "__main__":
    test_system()
"""
    
    try:
        with open('test_compatibility.py', 'w', encoding='utf-8') as f:
            f.write(test_script)
        print("Script de test creat: test_compatibility.py")
    except Exception as e:
        print(f"Nu s-a putut crea scriptul de test: {e}")

if __name__ == "__main__":
    # Verifică dacă fișierul principal există
    if not os.path.exists('monitor-server-autologin-32bit.py'):
        print("EROARE: Nu gasesc fisierul 'monitor-server-autologin-32bit.py'!")
        print("   Asigură-te că ești în folderul corect și că fișierul există.")
        sys.exit(1)

    # Creează fișierele auxiliare
    create_version_info()
    create_test_script()

    # Construiește executabilul
    print()
    build_executable()

