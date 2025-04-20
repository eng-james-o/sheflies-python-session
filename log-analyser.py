import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# === Step 1: Load the flight log CSV ===
df = pd.read_csv("flight_data.csv", parse_dates=["Timestamp"])

# === Step 2: Show basic info ===
print("\nFlight Log Summary:")
print(f"Total Records: {len(df)}")

# === Step 3: Basic Flight Stats ===
start_time = df['Timestamp'].min()
end_time = df['Timestamp'].max()
duration = end_time - start_time
max_altitude = df['Altitude'].max()
avg_speed = df['Speed'].mean()
min_battery = df['Battery_Level'].min()

print(f"Flight Duration     : {duration}")
print(f"Max Altitude (m)    : {max_altitude:.2f}")
print(f"Average Speed (m/s) : {avg_speed:.2f}")
print(f"Min Battery Level (%) : {min_battery:.2f}")

# === Step 4: Plot Altitude vs Time ===
plt.figure(figsize=(10, 5))
plt.plot(df['Timestamp'], df['Altitude'], color='blue')
plt.title('Altitude Over Time')
plt.xlabel('Time')
plt.ylabel('Altitude (m)')
plt.grid(True)
plt.tight_layout()
plt.show()

# === Step 5: Plot Speed vs Time and Total Distance Traveled with Dual Y-Axes ===
df['Elapsed_Time'] = (df['Timestamp'] - df['Timestamp'].min()).dt.total_seconds()
df['Distance'] = (df['Speed'] * df['Elapsed_Time'].diff()).fillna(0).cumsum()

fig, ax1 = plt.subplots(figsize=(10, 5))

# Plot speed on the right y-axis
ax1.plot(df['Timestamp'], df['Speed'], color='red', label='Speed (m/s)')
ax1.axhline(y=avg_speed, color='green', linestyle='--', label='Average Speed (m/s)')
ax1.set_xlabel('Time')
ax1.set_ylabel('Speed (m/s)', color='red')
ax1.tick_params(axis='y', labelcolor='red')
ax1.legend(loc='upper left')

# Create a second y-axis for total distance
ax2 = ax1.twinx()
ax2.plot(df['Timestamp'], df['Distance'], color='purple', label='Total Distance (m)')
ax2.set_ylabel('Distance (m)', color='purple')
ax2.tick_params(axis='y', labelcolor='purple')
ax2.legend(loc='upper right')

plt.title('Speed and Distance Over Time')
plt.grid(True)
plt.tight_layout()
plt.show()
