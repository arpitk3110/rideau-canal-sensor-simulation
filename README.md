# Rideau Canal Sensor Simulation  
**CST8916 – Final Project Component**  
**Student: Arpit Patel**

---

## 1. Overview

This repository contains the **Python-based IoT sensor simulator** for the Rideau Canal Monitoring System final project.  
The purpose of this simulator is to replace physical IoT devices by generating **realistic, continuous telemetry data** for three canal locations:

- **Dows Lake**
- **Fifth Avenue**
- **NAC (National Arts Centre)**

Each simulated device sends environmental readings every few seconds to an **Azure IoT Hub**, forming the first step in a real-time data pipeline.

The data includes:

- Ice Thickness (cm)  
- Surface Temperature (°C)  
- Snow Accumulation (cm)  
- External Air Temperature (°C)  
- Timestamp (ISO 8601 UTC)

Downstream Azure services (Stream Analytics, Cosmos DB, Blob Storage) rely on this telemetry for aggregation, safety assessment, and dashboard visualization.

### **Technologies Used**
- **Python 3.x**
- **Azure IoT Device SDK (`azure-iot-device`)**
- **python-dotenv** for environment variable handling
- **JSON** for formatted sensor messages

---

## 2. Prerequisites

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

Follow these step inside the repository folder:

### ** Navigate to the repo**

cd "D:\Cloud_Sem_1\Remote data\CST8916_Final_Project\rideau-canal-sensor-simulation"

4. Configuration

Before running the simulator, you must configure your .env file using device connection strings from Azure IoT Hub.

Step 1 — Create three IoT devices in Azure IoT Hub

Example names:

DowsLakeDevice

FifthAvenueDevice

NACDevice

Step 2 — Retrieve the device connection strings

In Azure Portal:
IoT Hub → Devices → Select Device → “Primary Connection String”

Step 3 — Create your .env file

Copy the example file: