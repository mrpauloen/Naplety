from PIL import Image, ImageDraw
import pystray
import subprocess
import time
import threading
import psutil

def get_sensor_data():
    """Pobiera temperaturę CPU i prędkość wentylatorów."""
    try:
        result = subprocess.run(["sensors"], capture_output=True, text=True)
        lines = result.stdout.split("\n")

        cpu_temp = "N/A"
        fan_speed1, fan_speed2 = "0", "0"
        cpu_usage = psutil.cpu_percent(interval=1)

        for line in lines:
            if "Package id" in line:
                cpu_temp = line.split("+")[1].split("°")[0].strip()
            elif "fan1" in line:
                fan_speed1 = line.split(":")[1].split("RPM")[0].strip()
            elif "fan2" in line:
                fan_speed2 = line.split(":")[1].split("RPM")[0].strip()

        return f"CPU: {cpu_temp}°C | Obciążenie: {cpu_usage}% | Fan1: {fan_speed1} rpm | Fan2: {fan_speed2} rpm"
    except Exception as e:
        return f"Error: {e}"

def create_icon():
    """Tworzy minimalistyczną ikonę."""
    size = 32  # Standardowy rozmiar ikony tray
    img = Image.new("RGBA", (size, size), (0, 0, 0, 255))  # Czarna ikona
    draw = ImageDraw.Draw(img)

    # Ikona wentylatora jako okrąg
    draw.ellipse((6, 6, 26, 26), outline="white", width=2)

    return img

def update_icon(icon):
    """Aktualizuje ikonę w trayu + wysyła powiadomienia."""
    while True:
        icon.icon = create_icon()

        # Wysyłanie powiadomienia zamiast title (bo title powoduje błąd)
        subprocess.Popen(["notify-send", "Monitor CPU", get_sensor_data()], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        time.sleep(60)  # Powiadomienie co 60 sekund

def close_applet(icon, item):
    """Zamyka aplet."""
    icon.stop()

def run_applet():
    """Uruchamia aplet w trayu."""
    icon = pystray.Icon("sys_monitor", create_icon(), menu=pystray.Menu(
        pystray.MenuItem("Exit", close_applet)
    ))

    threading.Thread(target=update_icon, args=(icon,), daemon=True).start()
    icon.run()

if __name__ == "__main__":
    run_applet()
