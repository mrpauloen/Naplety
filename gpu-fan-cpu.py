"""
The provided code is a Python script that creates a system tray applet to monitor CPU temperature, fan speeds, and CPU usage. It uses several libraries, including PIL for image creation, pystray for system tray integration, subprocess for running shell commands, time for sleep intervals, threading for concurrent execution, and psutil for system utilization information.

The get_sensor_data function retrieves CPU temperature, fan speeds, and CPU usage. It runs the sensors command using subprocess.run and parses the output to extract the relevant data. If the command fails or an error occurs, it returns an error message.

The create_icon function generates an icon image with the sensor data text. It creates a new image with a transparent background, draws the text on it, and centers the text vertically. It attempts to use a specific font and falls back to the default font if the specified one is unavailable.

The update_icon function continuously updates the tray icon with the latest sensor data. It runs in an infinite loop, updating the icon and its title every second.

The close_applet function stops the tray applet when the "Exit" menu item is selected.

The run_applet function initializes and runs the tray applet. It creates a pystray.Icon object with the initial icon and a menu containing the "Exit" option. It starts a separate thread to update the icon and runs the applet.

Finally, the script checks if it is being run as the main module and calls run_applet to start the applet.

Author: Paweł Nowak
We współpracy z AI
Wydanie pierwsze 2025.02
v 0.1

"""

from PIL import Image, ImageDraw, ImageFont
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
        fan_speed1 = "0"
        fan_speed2 = "0"
        cpu_usage = psutil.cpu_percent(interval=1)  # Pobiera % użycia CPU

        for line in lines:
            if "Package id" in line:
                cpu_temp = line.split("+")[1].split("°")[0].strip()
            elif "fan1" in line:
                fan_speed1 = line.split(":")[1].split("RPM")[0].strip()
            elif "fan2" in line:
                fan_speed2 = line.split(":")[1].split("RPM")[0].strip()

        return f"CPU: {cpu_temp}°C . {cpu_usage}% | {fan_speed1} {fan_speed2} rpm"
    except Exception as e:
        return f"Error: {e}"

from PIL import Image, ImageDraw, ImageFont

def create_icon():
    """Tworzy ikonę z tekstem i centruje go w poziomie i pionie."""

    text = get_sensor_data()

    font_size = 20  # Możesz dostosować wielkość czcionki
    width, height = 500, 35  # Dopasuj szerokość do ilości tekstu

    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("DejaVuSansCondensed.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()  # Awaryjne ustawienie w razie braku czcionki

    # Nowe podejście do pobierania rozmiaru tekstu
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    # Wycentrowanie tekstu
    #text_x = (width - text_width) // 2
    text_y = (height - text_height) // 2

    draw.text((5, text_y), text, font=font, fill=(255, 255, 255))

    return img



def update_icon(icon):
    """Aktualizuje ikonę w trayu."""
    while True:
        icon.icon = create_icon()
        icon.title = get_sensor_data()
        time.sleep(1)

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
