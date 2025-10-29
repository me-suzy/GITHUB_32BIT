#!/usr/bin/env python3
"""
Script de diagnostic pentru verificarea executabilului 32-bit
Verifică dacă executabilul este cu adevărat 32-bit și compatible cu Windows vechi
"""

import os
import sys
import struct
import platform

def check_pe_architecture(exe_path):
    """Verifică arhitectura unui fișier PE (executabil Windows)."""
    print("=" * 60)
    print(f"VERIFICARE ARHITECTURĂ: {os.path.basename(exe_path)}")
    print("=" * 60)
    
    if not os.path.exists(exe_path):
        print(f"✗ Fișierul nu există: {exe_path}")
        return None
    
    try:
        with open(exe_path, 'rb') as f:
            # Citește DOS header
            dos_header = f.read(64)
            if dos_header[:2] != b'MZ':
                print("✗ Nu este un executabil valid (lipsește MZ signature)")
                return None
            
            # Poziția PE header
            pe_offset = struct.unpack('<I', dos_header[60:64])[0]
            
            # Sare la PE header
            f.seek(pe_offset)
            pe_signature = f.read(4)
            
            if pe_signature != b'PE\x00\x00':
                print("✗ Nu este un executabil PE valid")
                return None
            
            # Citește Machine type (2 bytes)
            machine_bytes = f.read(2)
            machine = struct.unpack('<H', machine_bytes)[0]
            
            # Machine types
            MACHINE_I386 = 0x014c   # Intel 386 (32-bit)
            MACHINE_AMD64 = 0x8664  # AMD64 (64-bit)
            
            print(f"\n📊 Machine Type: 0x{machine:04x}")
            
            if machine == MACHINE_I386:
                print("✅ Executabil 32-bit (x86) - Compatible cu Windows XP/7 32-bit")
                return "32bit"
            elif machine == MACHINE_AMD64:
                print("⚠️  Executabil 64-bit (x64) - NU funcționează pe Windows XP/7 32-bit!")
                return "64bit"
            else:
                print(f"❓ Arhitectură necunoscută: 0x{machine:04x}")
                return "unknown"
    
    except Exception as e:
        print(f"✗ Eroare la citirea executabilului: {e}")
        return None

def check_python_environment():
    """Verifică mediul Python actual."""
    print("\n" + "=" * 60)
    print("VERIFICARE MEDIU PYTHON CURENT")
    print("=" * 60)
    
    arch = platform.architecture()[0]
    print(f"Arhitectura Python: {arch}")
    print(f"Versiune Python: {sys.version}")
    print(f"Platform: {platform.platform()}")
    print(f"Machine: {platform.machine()}")
    print(f"Processor: {platform.processor()}")
    
    is_32bit = arch == '32bit'
    
    if is_32bit:
        print("\nOK - Python 32-bit - Perfect pentru compilare executabile 32-bit!")
    else:
        print("\nATENTIE - Python 64-bit - Va produce executabile 64-bit!")
        print("    Pentru executabile 32-bit, instaleaza Python 32-bit!")

def check_dependencies():
    """Verifică dependențele instalate."""
    print("\n" + "=" * 60)
    print("VERIFICARE DEPENDENȚE")
    print("=" * 60)
    
    required = {
        'paramiko': 'SSH client',
        'requests': 'HTTP requests',
        'tkinter': 'GUI framework',
        'PIL': 'Image processing (Pillow)',
        'pyautogui': 'GUI automation',
        'PyInstaller': 'Exe builder'
    }
    
    for module, description in required.items():
        try:
            if module == 'tkinter':
                import tkinter
            elif module == 'PIL':
                import PIL
            elif module == 'PyInstaller':
                import PyInstaller
            else:
                __import__(module)
            
            # Obține versiunea
            try:
                if module == 'tkinter':
                    version = "Built-in"
                elif module == 'PIL':
                    import PIL
                    version = PIL.__version__
                elif module == 'PyInstaller':
                    import PyInstaller
                    version = PyInstaller.__version__
                else:
                    mod = __import__(module)
                    version = getattr(mod, '__version__', 'Unknown')
            except:
                version = "Installed"
            
            print(f"✅ {module:15s} - {version:15s} ({description})")
        except ImportError:
            print(f"✗ {module:15s} - LIPSEȘTE! ({description})")

def diagnose_all():
    """Rulează toate diagnosticele."""
    print("=" * 60)
    print("DIAGNOSTIC EXECUTABIL 32-BIT")
    print("=" * 60)
    
    # Verifică mediul Python
    check_python_environment()
    
    # Verifică dependențele
    check_dependencies()
    
    # Verifică executabilele existente
    print("\n" + "=" * 60)
    print("VERIFICARE EXECUTABILE EXISTENTE")
    print("=" * 60)
    
    exe_files = [
        'dist/AlephMonitor-AutoLogin-32bit.exe',
        'dist/AlephMonitor-AutoLogin-32bit-FIXED.exe',
    ]
    
    found_any = False
    for exe_path in exe_files:
        if os.path.exists(exe_path):
            found_any = True
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"\n📁 Fișier: {exe_path}")
            print(f"   Dimensiune: {size_mb:.2f} MB")
            check_pe_architecture(exe_path)
    
    if not found_any:
        print("\n⚠️  Nu s-au găsit executabile în folderul dist/")
        print("   Rulează build_exe_32bit_FIXED.py pentru a crea executabilul")
    
    # Recomandări
    print("\n" + "=" * 60)
    print("RECOMANDĂRI")
    print("=" * 60)
    
    arch = platform.architecture()[0]
    if arch != '32bit':
        print("\n⚠️  ATENȚIE: Python-ul tău este 64-bit!")
        print("\n📋 Pentru a crea un executabil 32-bit funcțional:")
        print("   1. Descarcă Python 3.8.10 (32-bit) de la:")
        print("      https://www.python.org/downloads/release/python-3810/")
        print("   2. Instalează Python 32-bit")
        print("   3. Instalează dependențele: pip install paramiko requests pyautogui pyinstaller pillow")
        print("   4. Rulează: python build_exe_32bit_FIXED.py")
    else:
        print("\n✅ Mediul tău este corect pentru compilare 32-bit!")
        print("\n📋 Pentru a crea executabilul:")
        print("   1. Rulează: python build_exe_32bit_FIXED.py")
        print("   2. Testează executabilul pe Windows 7/XP")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    diagnose_all()
    
    print("\nDiagnostic complet!")
    input("\nApasă Enter pentru a închide...")

