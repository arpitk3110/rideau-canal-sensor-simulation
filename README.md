The sensor simulation repository README.md includes: 


## **1. Overview**

The Sensor Simulation module generates realistic environmental readings for the Rideau Canal Monitoring System. It mimics three physical sensor stations located at Dow's Lake, Fifth Avenue, and NAC, producing data such as ice thickness, surface temperature, and snow accumulation.
The simulator sends these readings to Azure IoT Hub, where they are processed by a Stream Analytics job and stored in Azure Cosmos DB for dashboard visualization.

## Technologies Used

 * **Python 3**

 * **Azure IoT Device SDK for Python** — Sends telemetry messages from simulated devices to Azure IoT Hub.

 * **Azure IoT Hub** — Receives device messages and routes them to downstream services.

 * **JSON** — Standard message format for all telemetry sent to the cloud.


---

## **2. Prerequisites**

Before running the simulator:

- Python **3.9+** installed on Windows
- VS Code (recommended for development)
- An **Azure Subscription**
- An **Azure IoT Hub** created in the Azure portal
- **Three IoT Device Identities** created within the IoT Hub  
  (one for each monitoring location)
- Basic command-line knowledge (PowerShell or Command Prompt)

---

## 3. Installation

Follow these steps to install and prepare the simulator:

**1. Clone the repository**

**2. Install required Python libraries** -- pip install -r requirements.txt

**3. Configure your device connection string**
   * Create a .env file in the project root.
   * Add your IoT Hub device connection string

**4. Run the simulator**
### ** Navigate to the repo**



### 4. Configuration

The simulator is configured using a `.env` file stored in the same folder as `sensor_simulator.py`.

Create a file named `.env` 

```env
DEVICE1_CONNECTION_STRING=HostName=<your-iothub-name>.azure-devices.net;DeviceId=DowsLakeDevice;SharedAccessKey=<device1-key>
DEVICE2_CONNECTION_STRING=HostName=<your-iothub-name>.azure-devices.net;DeviceId=FifthAvenueDevice;SharedAccessKey=<device2-key>
DEVICE3_CONNECTION_STRING=HostName=<your-iothub-name>.azure-devices.net;DeviceId=NACDevice;SharedAccessKey=<device3-key>

# How often to send messages (in seconds)
MESSAGE_INTERVAL_SECONDS=10


```


## **5. Usage**

After installing the dependencies and configuring your .env file, you can start the simulator using : python simulator.py

The simulator will begin generating synthetic winter condition data (ice thickness, snow accumulation, surface temperature) at regular intervals and send it to Azure IoT Hub.
You can monitor incoming telemetry from the Azure Portal or Azure CLI.

**Code Structure**

The sensor-simulator project is organized into a simple and clear folder structure that separates core functionality, configuration, and documentation. The main logic for generating and sending simulated sensor readings is contained in simulator.py, while supporting tasks—such as creating random sensor values or managing timing—are handled inside utils.py. All device credentials and environment-specific settings are loaded through config.py, keeping sensitive or configurable information separate from the main code. The requirements.txt file lists the Python libraries needed to run the simulator, ensuring easy setup on any machine. Finally, the README.md provides documentation to help users understand how the simulator works and how to run it.

**Main Components Explained**

**1. simulator.py**

This is the core of the application.
It performs three major tasks:

 * Generates synthetic sensor readings for each location.

 * Formats data into JSON payloads.

 * Sends messages to Azure IoT Hub using the IoT Hub Device SDK.

 **2. config.py**

 * Loads the device connection string from .env.

 * Validates required configuration values.


 ## Key functions

**1. generate_sensor_payload(location)**

  * Purpose:

    Creates one complete synthetic sensor reading for a given location.

Why it is useful:

Your system depends on continuous, realistic sensor data. This function simulates that by generating random—but believable—values for ice thickness, temperature, and snow accumulation.

**2. create_device_clients(locations)**

  * Purpose:

Creates an Azure IoT Hub device client for each physical location (Dow’s Lake, Fifth Avenue, NAC).

Why it is useful:

Each location acts like a separate IoT device.
This function connects each device to Azure using its connection string.

**3. send_telemetry_loop(clients, interval_seconds)**

Purpose:

 * This is the main engine of your simulator.

 * It repeatedly sends live sensor readings to IoT Hub.

 ## 6. Sensor Data Format

Each simulated device sends telemetry to Azure IoT Hub as a **single JSON object**.  
This JSON represents one reading from one location at a specific point in time.

---

### 6.1 JSON Schema

```jsonc
{
  "location": "DowsLake",          // Canal section name (DowsLake, FifthAvenue, NAC)
  "iceThickness": 32.1,            // Ice thickness in centimeters
  "surfaceTemperature": -4.3,      // Ice surface temperature in °C
  "snowAccumulation": 1.2,         // Snow depth on top of ice, in centimeters
  "externalTemperature": -7.0,     // Ambient air temperature in °C
  "timestamp": "2025-11-27T15:05:23Z" // ISO 8601 timestamp (UTC)
}


### 6.2 Example Output

Below is a real example of one message sent by the simulator for each location:

{
  "location": "DowsLake",
  "iceThickness": 28.4,
  "surfaceTemperature": -12.9,
  "snowAccumulation": 13.8,
  "externalTemperature": -11.5,
  "timestamp": "2025-11-27T23:45:43.391644+00:00"
}

```

## 7. Troubleshooting

Most issues in the sensor simulator are related to missing configuration or connectivity. If no data appears in IoT Hub, first check that all three device connection strings are correctly placed in the `.env` file and match the devices registered in Azure. If the simulator prints warnings like “No valid device clients created,” it means the Azure IoT SDK is not installed or the environment variables were not loaded—reinstall dependencies using `pip install -r requirements.txt` and confirm `.env` is in the same folder as the script. 

If some messages fail to send, verify your internet connection and ensure the IoT Hub is not paused or deleted. In cases where only some locations send data, recheck the corresponding DEVICE# connection strings. Finally, if timestamps or sensor values look incorrect, restart the simulator to reset its random generation logic.