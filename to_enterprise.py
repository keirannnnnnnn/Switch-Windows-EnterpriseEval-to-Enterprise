import ctypes
import sys
import os
import urllib.request
import zipfile
import shutil
import subprocess

# ================
# ADMIN CHECK
# ================
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, __file__, None, 1
    )
    sys.exit(0)

print("[OK] Running as Administrator")

# ================
# CONFIG
# ================
ZIP_URL = "https://github.com/keirannnnnnnn/Switch-Windows-EnterpriseEval-to-Enterprise/archive/refs/heads/main.zip"
ZIP_FILE = "package.zip"
EXTRACT_DIR = "extracted"
TARGET_DIR = r"C:\Windows\System32\spp\tokens\skus"
DEST_ENTERPRISE = os.path.join(TARGET_DIR, "Enterprise")
EVAL_PATH = os.path.join(TARGET_DIR, "EnterpriseEval")
ACT_URL = "https://get.activated.win"
ACT_FILE = "act.ps1"

copy_success = False  # FLAG PENTING

try:
    # ================
    # DOWNLOAD
    # ================
    print("[INFO] Downloading ZIP...")
    urllib.request.urlretrieve(ZIP_URL, ZIP_FILE)
    print("[OK] Download completed")

    # ================
    # EXTRACT
    # ================
    print("[INFO] Extracting ZIP...")
    with zipfile.ZipFile(ZIP_FILE, "r") as zip_ref:
        zip_ref.extractall(EXTRACT_DIR)
    print("[OK] Extraction completed")

    # ================
    # FIND ENTERPRISE DIR
    # ================
    enterprise_path = None
    for root, dirs, files in os.walk(EXTRACT_DIR):
        if "Enterprise" in dirs:
            enterprise_path = os.path.join(root, "Enterprise")
            break

    if not enterprise_path:
        raise FileNotFoundError("Enterprise directory not found in package")

    print(f"[OK] Enterprise directory found: {enterprise_path}")

    # ================
    # COPY ENTERPRISE
    # ================
    print("[INFO] Copying Enterprise directory...")
    os.makedirs(TARGET_DIR, exist_ok=True)

    shutil.copytree(
        enterprise_path,
        DEST_ENTERPRISE,
        dirs_exist_ok=True
    )

    if not os.path.exists(DEST_ENTERPRISE):
        raise RuntimeError("Copy finished but destination not found")

    copy_success = True
    print("[SUCCESS] Enterprise directory copied")

    # ================
    # DELETE EnterpriseEval (ONLY IF COPY SUCCESS)
    # ================
    if copy_success and os.path.exists(EVAL_PATH):
        print("[INFO] Removing EnterpriseEval...")

        subprocess.run(
            f'takeown /f "{EVAL_PATH}" /r /d y',
            shell=True,
            check=True
        )

        subprocess.run(
            f'icacls "{EVAL_PATH}" /grant Administrators:F /t',
            shell=True,
            check=True
        )

        shutil.rmtree(EVAL_PATH)
        print("[SUCCESS] EnterpriseEval deleted")
    else:
        print("[SKIP] EnterpriseEval deletion skipped")

    # ================
    # COMMANDS (SAFE MODE)
    # ================
    print("\n[INFO] Executing commands...")
    commands = [
        'echo cscript.exe %windir%\\system32\\slmgr.vbs /upk >nul 2>&1',
        'echo cscript.exe %windir%\\system32\\slmgr.vbs /ckms >nul 2>&1',
        'echo cscript.exe %windir%\\system32\\slmgr.vbs /cpky >nul 2>&1',
        'echo cscript.exe %windir%\\system32\\slmgr.vbs /ipk NPPR9-FWDCX-D2C8J-H872K-2YT43',
        'sc query LicenseManager',
        'sc query wuauserv'
    ]

    for cmd in commands:
        print(f"\n[CMD] {cmd}")
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            check=True
        )
        if result.stdout:
            print(result.stdout.strip())

    # Download file dari web
    urllib.request.urlretrieve(ACT_URL, ACT_FILE)

    # Jalankan file PowerShell
    process = subprocess.run(
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", ACT_FILE, "1"],
        capture_output=True,
        text=True,
        check=True
    )
    print(process.stdout)

    print("\n[COMPLETED] All steps executed successfully")

except Exception as e:
    print("\n[FAILED] Process aborted")
    print("Reason:", str(e))

    # ================
    # OPTIONAL ROLLBACK
    # ================
    if copy_success and os.path.exists(DEST_ENTERPRISE):
        print("[ROLLBACK] Removing copied Enterprise directory")
        shutil.rmtree(DEST_ENTERPRISE, ignore_errors=True)

    sys.exit(1)
