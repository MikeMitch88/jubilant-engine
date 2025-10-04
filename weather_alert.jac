import random;

# Define the WeatherStation node with required attributes
node WeatherStation {
    has name: str;
    has temperature: float;
    has humidity: float;
    has wind_speed: float;
    has alert: str = "Normal";
}

# Define the WeatherMonitor walker with abilities to simulate weather and summarize
walker WeatherMonitor {
    has alert_count: int = 0;
    has total_stations: int = 0;

    # Ability to simulate weather data and generate alerts
    can simulate_weather with `root entry {
        self.alert_count = 0;
        self.total_stations = 0;

        visit [-->](`?WeatherStation) {
            # Generate random weather data
            here.temperature = random.uniform(10.0, 45.0);  # Temperature between 10 and 45
            here.humidity = random.uniform(10.0, 90.0);      # Humidity between 10% and 90%
            here.wind_speed = random.uniform(0.0, 100.0);    # Wind speed between 0 and 100 km/h

            # Apply alert logic
            if here.temperature > 35.0 and here.humidity < 30.0 {
                here.alert = "🔥 Heatwave Warning";
            } elif here.wind_speed > 80.0 {
                here.alert = "🌪️ Storm Alert";
            } elif here.temperature < 18.0 {
                here.alert = "❄️ Cold Weather Advisory";
            } else {
                here.alert = "✅ Normal Conditions";
            }

            # Print the readings and alert for the station
            std.out(f"Station: {here.name}");
            std.out(f"  Temperature: {here.temperature:.2f} °C");
            std.out(f"  Humidity: {here.humidity:.2f} %");
            std.out(f"  Wind Speed: {here.wind_speed:.2f} km/h");
            std.out(f"  Alert: {here.alert}");

            self.total_stations += 1;
            if here.alert != "✅ Normal Conditions" {
                self.alert_count += 1;
            }
        };
    }

    # Ability to print summary report
    can summary with `root entry {
        normal_count = self.total_stations - self.alert_count;
        std.out("--- Weather Alert Summary ---");
        std.out(f"Total Stations: {self.total_stations}");
        std.out(f"Stations Under Alert: {self.alert_count}");
        std.out(f"Stations Normal: {normal_count}");
        std.out("Weather Alert System Simulation Complete.");
    }
}

# Entry point to spawn stations and run the simulation
with entry: __main__ {
    # Spawn 5 WeatherStation nodes with given names
    station_names = ["Nairobi", "Mombasa", "Eldoret", "Kisumu", "Garissa"];
    for name in station_names {
        root ++> WeatherStation(name=name);
    }

    # Spawn the WeatherMonitor walker
    monitor = root spawn WeatherMonitor();

    # Run simulation and summary
    monitor::simulate_weather;
    monitor::summary;
}
