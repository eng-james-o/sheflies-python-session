import csv
from datetime import datetime, timedelta
import random

# Starting timestamp
start_time = datetime(2025, 4, 1, 12, 0, 0)
latitude = 7.2534
longitude = 5.2162
altitude = 0
battery = 100

# Output file name
filename = "flight_data.csv"

# Create the file in write mode
with open(filename, mode='w', newline='') as file:
    # Use the CSV writer to add rows to the file
    # Write the header row
    writer = csv.writer(file)
    writer.writerow(['Timestamp', 'Altitude', 'Speed', 'Latitude', 'Longitude', 'Battery_Level'])

    # Loop 60 times, i.e., for 10 minutes of flight data
    for i in range(60):
        # Simulate data every 10 seconds
        # Update the timestamp, altitude, speed, latitude, longitude, and battery level
        current_time = start_time + timedelta(seconds=10 * i)
        altitude += random.uniform(0.5, 2.0) if i < 30 else -random.uniform(0.5, 2.0)  # ascend, then descend
        speed = random.uniform(3, 10)
        latitude += random.uniform(-0.0001, 0.0001)
        longitude += random.uniform(-0.0001, 0.0001)
        battery -= random.uniform(0.3, 0.8)

        # write the row to the file, following the header order defined earlier
        writer.writerow([
            current_time.strftime("%Y-%m-%d %H:%M:%S"),
            round(max(0, altitude), 2),
            round(speed, 2),
            round(latitude, 6),
            round(longitude, 6),
            round(max(0, battery), 2)
        ]) 

# Print confirmation
print(f"Mock flight log '{filename}' created successfully!")