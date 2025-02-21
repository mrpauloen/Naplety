# Naplety
 Aplety i powiadomienia w tray'u


# 🖥️ GPU/CPU Fan Monitor & Control

Aplet dla systemu Linux do monitorowania temperatury CPU/GPU, wykorzystania CPU oraz prędkości wentylatorów w pasku systemowym. Dodatkowo umożliwia sterowanie wentylatorami poprzez `fancontrol`.

---

## 📌 Funkcje
✅ **Wyświetlanie w tray'u**: temperatura CPU/GPU, prędkość wentylatorów, wykorzystanie CPU
✅ **Automatyczny start z systemem**
✅ **Integracja z `fancontrol`** – dynamiczne sterowanie prędkością wentylatorów
✅ **Obsługa systemów Dell i innych laptopów z `dell_smm_hwmon`**

---

## 🔹 1. Instalacja

### **🔧 Zainstaluj wymagane pakiety**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv python3-gi python3-gi-cairo gir1.2-appindicator3-0.1 fancontrol
```

### **📦 Utwórz środowisko wirtualne i zainstaluj zależności**
```bash
python3 -m venv ~/.gpu_applet_venv
source ~/.gpu_applet_venv/bin/activate
pip install psutil pystray pillow
```

### **📜 Pobierz skrypt**
```bash
wget -O ~/gpu-fan-cpu.py https://github.com/TWOJE_REPO/gpu-fan-cpu/raw/main/gpu-fan-cpu.py
chmod +x ~/gpu-fan-cpu.py
```

### **🚀 Uruchomienie**
```bash
python3 ~/gpu-fan-cpu.py
```

---

## 🔹 2. Automatyczny Start z Systemem

1. **Utwórz plik autostartu:**
   ```bash
   nano ~/.config/autostart/gpu-fan-cpu.desktop
   ```
2. **Dodaj zawartość:**
   ```ini
   [Desktop Entry]
   Type=Application
   Name=GPU/CPU Monitor
   Exec=/home/atom/.gpu_applet_venv/bin/python3 /home/atom/gpu-fan-cpu.py
   Hidden=false
   NoDisplay=false
   X-GNOME-Autostart-enabled=true
   ```
3. **Nadaj uprawnienia i przetestuj:**
   ```bash
   chmod +x ~/.config/autostart/gpu-fan-cpu.desktop
   gtk-launch gpu-fan-cpu
   ```

---

## 🔹 3. Sterowanie Wentylatorami w Linuxie

🔹 Sprawdzenie wentylatorów:
```bash
sensors
cat /sys/class/hwmon/hwmon6/fan1_input
cat /sys/class/hwmon/hwmon6/fan2_input
```

🔹 Ustawienie manualnego sterowania:
```bash
echo user_space | sudo tee /sys/class/thermal/thermal_zone*/policy
```

🔹 Instalacja `fancontrol` i konfiguracja:
```bash
sudo apt install fancontrol
sudo pwmconfig
```

🔹 Włączenie `fancontrol`:
```bash
sudo systemctl enable fancontrol
sudo systemctl start fancontrol
sudo systemctl status fancontrol
```

---

## 🔹 4. Debugowanie i Problemy
| Problem | Rozwiązanie |
|---------|------------|
| Aplet się nie uruchamia | `source ~/.gpu_applet_venv/bin/activate && python3 ~/gpu-fan-cpu.py` |
| Wentylatory nie działają | `echo user_space | sudo tee /sys/class/thermal/thermal_zone*/policy` |
| `fancontrol` nie działa | `sudo pwmconfig` i ponowne zapisanie konfiguracji |
| Nie można ustawić PWM | `sudo modprobe dell_smm_hwmon` |

🔹 **Restart apletu:**
```bash
ps aux | grep gpu-fan-cpu.py
kill -9 $(pgrep -f gpu-fan-cpu.py)
python3 ~/gpu-fan-cpu.py
```

🔹 **Sprawdzenie logów:**
```bash
cat log.txt
```

---

## 🔹 5. Jak zacząć od nowa?
Jeśli chcesz usunąć wszystko i skonfigurować od nowa:
```bash
sudo systemctl disable fancontrol
sudo rm -rf ~/.gpu_applet_venv ~/gpu-fan-cpu.py ~/.config/autostart/gpu-fan-cpu.desktop
sudo apt remove fancontrol
```
Następnie **zacznij od kroku 1**.

---

## 📌 Podsumowanie
✅ **Aplet działa i monitoruje CPU, GPU, FAN – startuje z systemem**  
✅ **Wentylatory są sterowane przez `fancontrol`**  
✅ **Możesz debugować i rozwiązywać problemy**  
✅ **Instrukcja umożliwia pełną konfigurację od zera**  

---

💡 **Twój system jest teraz w pełni monitorowany i wentylatory są pod Twoją kontrolą!** 🚀
