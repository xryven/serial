import wmi
import platform
import socket
import uuid
from datetime import datetime

wmi_conn = wmi.WMI()
log_file = "hwids.txt"

def log(text=""):
    print(text)
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(text + "\n")

def safe_query(func):
    try:
        return func()
    except:
        return []

def print_kv(key, value):
    if not value:
        value = "N/A"
    log(f"{key}: {value}")

def section(title):
    log(f"\n[{title}]")

with open(log_file, "w", encoding="utf-8") as f:
    f.write(f"System Information Log - {datetime.now()}\n")

section("System")
print_kv("Hostname", socket.gethostname())
print_kv("OS", platform.system())
print_kv("Release", platform.release())
print_kv("Version", platform.version())
print_kv("Arch", platform.machine())
print_kv("CPU", platform.processor())

section("UUID & MAC")
node = uuid.getnode()
print_kv("UUID", hex(node))
mac = ':'.join(f"{(node >> i) & 0xff:02x}" for i in range(0, 48, 8))[::-1]
print_kv("MAC", mac)

section("BIOS")
bios_list = safe_query(lambda: wmi_conn.Win32_BIOS())
if bios_list:
    bios = bios_list[0]
    print_kv("BIOS Version", bios.SMBIOSBIOSVersion)
    print_kv("BIOS Serial", bios.SerialNumber)
else:
    print_kv("BIOS", "N/A")

section("Mainboard")
boards = safe_query(lambda: wmi_conn.Win32_BaseBoard())
if boards:
    board = boards[0]
    print_kv("Vendor", board.Manufacturer)
    print_kv("Model", board.Product)
    print_kv("Serial", board.SerialNumber)
else:
    print_kv("Mainboard", "N/A")

section("Drives")
drives = safe_query(lambda: wmi_conn.Win32_DiskDrive())
if drives:
    for i, d in enumerate(drives, 1):
        print_kv(f"Drive {i} Model", d.Model)
        print_kv(f"Drive {i} Serial", d.SerialNumber)
else:
    print_kv("Drives", "N/A")

section("CPU")
cpus = safe_query(lambda: wmi_conn.Win32_Processor())
if cpus:
    cpu = cpus[0]
    print_kv("CPU Name", cpu.Name)
    print_kv("CPU ID", cpu.ProcessorId)
else:
    print_kv("CPU", "N/A")

section("GPU")
gpus = safe_query(lambda: wmi_conn.Win32_VideoController())
if gpus:
    for i, gpu in enumerate(gpus, 1):
        print_kv(f"GPU {i}", gpu.Name)
        print_kv(f"Driver {i}", gpu.DriverVersion)
else:
    print_kv("GPU", "N/A")

section("OS Details")
oses = safe_query(lambda: wmi_conn.Win32_OperatingSystem())
if oses:
    os = oses[0]
    print_kv("Full Name", os.Caption)
    print_kv("Architecture", os.OSArchitecture)
    print_kv("Serial", os.SerialNumber)
else:
    print_kv("OS", "N/A")

section("TPM")
try:
    tpms = wmi_conn.Win32_Tpm()
    if tpms:
        tpm = tpms[0]
        print_kv("TPM Vendor", tpm.ManufacturerID)
        print_kv("Spec Version", tpm.SpecVersion)
        print_kv("Enabled", tpm.IsEnabled_InitialValue)
        print_kv("Activated", tpm.IsActivated_InitialValue)
    else:
        print_kv("TPM", "N/A")
except:
    print_kv("TPM", "N/A")
