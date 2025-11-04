# 🌦️ Weather Alert Simulation (Jac Project)

A simple weather monitoring system built using the **Jac programming language**.  
It simulates weather stations across different regions, generates random readings,  
and triggers alerts based on temperature, humidity, and wind speed.

## 🚀 Features
- Randomized weather data generation per station  
- Automatic alerts for heatwaves, storms, and cold weather  
- Summary report showing total stations and active alerts  
- 100% runnable in Jac CLI

## 🧠 How It Works
- Each `WeatherStation` node represents a location (e.g., Nairobi, Mombasa).  
- A `WeatherMonitor` walker collects readings and applies alert logic.  
- The system outputs station data and a summary to the console.

## 🧩 Tech Stack
- **Language:** Jac  
- **Execution:** Jac CLI or Jac Playground (https://app.jac-lang.org/)  
- **Modules Used:** `random` (for data simulation)

## ▶️ Running the Project
1. Run the program:
   ```bash
   jac weather_alert.jac
