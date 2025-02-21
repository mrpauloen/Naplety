from PIL import Image, ImageDraw, ImageFont
import pystray
import subprocess
import time
import threading

def get_sensor_data():
    """Pobiera temperaturę CPU."""
    try:
        result = subprocess.run(["sensors"], capture_output=True, text=True)
        lines = result.stdout.split("\n")

        cpu_temp = "N/A"
        for line in lines:
            if "Package id 0" in line:  # Dopasowane do Twojego `sensors`
                cpu_temp = line.split("+")[1].split("°")[0].strip()
                break

        return cpu_temp  # Zwracamy tylko liczbę temperatury
    except Exception as e:
        return "ERR"

def create_icon():
    """Tworzy ikonę z temperaturą CPU."""
    temp = get_sensor_data()

    # Rozmiar ikony
    icon_width = 126  # Szersza ikona (możesz testować 128)
    icon_height = 64  # Wysokość
    font_size = 30  # Większa czcionka dla lepszej widoczności

    img = Image.new("RGBA", (icon_width, icon_height), (0, 0, 0, 255))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    # Ustawienie koloru tła w zależności od temperatury
    try:
        temp_value = float(temp)
        if temp_value >= 80:
            bg_color = (255, 0, 0, 255)  # Czerwone tło dla wysokiej temp
        elif temp_value >= 60:
            bg_color = (255, 165, 0, 255)  # Pomarańczowe dla średniej temp
        else:
            bg_color = (0, 0, 255, 255)  # Niebieskie dla niskiej temp
    except ValueError:
        bg_color = (0, 0, 0, 255)  # Czarne tło, jeśli błąd odczytu

    img.paste(bg_color, [0, 0, icon_width, icon_height])

    # Pobranie rozmiaru tekstu
    text_bbox = draw.textbbox((1, 1), temp + "°C", font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    text_x = (icon_width - text_width) // 2
    text_y = (icon_height - text_height) // 2

    # Rysowanie obramowania
    draw.rectangle([0, 0, icon_width - 1, icon_height - 1], outline=(255, 255, 255, 255), width=2)

    # Dodanie temperatury
    draw.text((text_x, text_y), temp + "°C", font=font, fill=(255, 255, 255))

    return img

def update_icon(icon):
    """Aktualizuje ikonę w trayu co 5 sekund."""
    while True:
        icon.icon = create_icon()
        time.sleep(5)

def close_applet(icon, item):
    """Zamyka aplet."""
    icon.stop()

def run_applet():
    """Uruchamia aplet w trayu."""
    icon = pystray.Icon("cpu_monitor", create_icon(), menu=pystray.Menu(
        pystray.MenuItem("Exit", close_applet)
    ))

    threading.Thread(target=update_icon, args=(icon,), daemon=True).start()
    icon.run()

if __name__ == "__main__":
    run_applet()
