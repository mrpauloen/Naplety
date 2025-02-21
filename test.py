import subprocess
import time
import psutil

def get_sensor_data():
    """Pobiera temperaturę CPU i prędkość wentylatorów."""
    try:
        result = subprocess.Popen(["sensors"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
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

def send_notification():
    """Uruchamia powiadomienie w tle."""
    while True:
        data = get_sensor_data()
        process = subprocess.Popen(["notify-send", "Monitor CPU", data], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(60)  # Powiadomienie co 60 sekund

if __name__ == "__main__":
    send_notification()
