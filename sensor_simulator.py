import os
import time
import json
import random
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

try:
    from azure.iot.device import IoTHubDeviceClient, Message
except ImportError:
    IoTHubDeviceClient = None
    Message = None


def load_config():
    """
    Load configuration from .env and return interval + location mapping.
    """
    # Load .env from the same folder as this script
    base_dir = Path(__file__).resolve().parent
    env_path = base_dir / ".env"

    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
        print(f"[INFO] Loaded .env from: {env_path}")
    else:
        print(f"[WARN] .env file not found at: {env_path}")

    # Debug flags to verify environment variables are visible
    print("[DEBUG] DEVICE1_CONNECTION_STRING present:",
          bool(os.getenv("DEVICE1_CONNECTION_STRING")))
    print("[DEBUG] DEVICE2_CONNECTION_STRING present:",
          bool(os.getenv("DEVICE2_CONNECTION_STRING")))
    print("[DEBUG] DEVICE3_CONNECTION_STRING present:",
          bool(os.getenv("DEVICE3_CONNECTION_STRING")))

    # Read message interval (default 10 seconds)
    try:
        interval = int(os.getenv("MESSAGE_INTERVAL_SECONDS", "10"))
    except ValueError:
        interval = 10

    # Mapping between logical locations and env variable names
    locations = [
        ("DowsLake", "DEVICE1_CONNECTION_STRING"),
        ("FifthAvenue", "DEVICE2_CONNECTION_STRING"),
        ("NAC", "DEVICE3_CONNECTION_STRING"),
    ]

    return interval, locations


def create_device_clients(locations):
    """
    Create IoT Hub device clients for each configured location.
    """
    if IoTHubDeviceClient is None:
        print(
            "ERROR: azure-iot-device is not installed.\n"
            "Install dependencies with: pip install -r requirements.txt"
        )
        return []

    clients = []

    for location_name, env_var in locations:
        conn_str = os.getenv(env_var)

        if not conn_str:
            print(
                f"[WARN] No connection string configured for {location_name} "
                f"(expected in env variable {env_var}). This device will be skipped."
            )
            continue

        try:
            client = IoTHubDeviceClient.create_from_connection_string(conn_str)
            clients.append((location_name, client))
            print(f"[INFO] Created IoT Hub client for {location_name}")
        except Exception as ex:
            print(f"[ERROR] Failed to create client for {location_name}: {ex}")

    if not clients:
        print(
            "ERROR: No valid device clients created. "
            "Check your .env file for device connection strings."
        )

    return clients


def generate_sensor_payload(location: str) -> dict:
    """
    Generate one random sensor reading for a given location.
    """
    ice_thickness_cm = round(random.uniform(20, 40), 1)
    surface_temp_c = round(random.uniform(-15, 2), 1)
    snow_accum_cm = round(random.uniform(0, 15), 1)
    external_temp_c = round(random.uniform(-25, 5), 1)

    payload = {
        "location": location,
        "iceThickness": ice_thickness_cm,
        "surfaceTemperature": surface_temp_c,
        "snowAccumulation": snow_accum_cm,
        "externalTemperature": external_temp_c,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    return payload


def send_telemetry_loop(clients, interval_seconds: int):
    """
    Main loop: send telemetry for all clients every interval_seconds.
    """
    if not clients:
        print("No clients available. Exiting.")
        return

    print(f"[INFO] Starting telemetry loop. Interval = {interval_seconds} seconds.")
    print("Press Ctrl + C to stop.\n")

    try:
        while True:
            for location, client in clients:
                payload = generate_sensor_payload(location)
                message_json = json.dumps(payload)

                try:
                    msg = Message(message_json)
                    msg.content_type = "application/json"
                    msg.content_encoding = "utf-8"

                    client.send_message(msg)
                    print(f"[SENT] {location}: {message_json}")
                except Exception as ex:
                    print(f"[ERROR] Failed to send message for {location}: {ex}")

            time.sleep(interval_seconds)

    except KeyboardInterrupt:
        print("\n[INFO] Telemetry loop stopped by user.")
    finally:
        for location, client in clients:
            try:
                client.shutdown()
                print(f"[INFO] Closed client for {location}")
            except Exception:
                pass


def main():
    interval, locations = load_config()
    clients = create_device_clients(locations)
    send_telemetry_loop(clients, interval)


if __name__ == "__main__":
    main()
