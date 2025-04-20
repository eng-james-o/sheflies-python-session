import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
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

# === Step 4: Calculate Total Distance Traveled ===
df['Elapsed_Time'] = (df['Timestamp'] - df['Timestamp'].min()).dt.total_seconds()
df['Distance'] = (df['Speed'] * df['Elapsed_Time'].diff()).fillna(0).cumsum()

# === Step 5: Create a single canvas with subplots and animate ===
fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True)

# Subplot 1: Altitude vs Time
axes[0].set_title('Altitude Over Time')
axes[0].set_ylabel('Altitude (m)')
axes[0].grid(True)

# Subplot 2: Speed vs Time
axes[1].set_title('Speed Over Time')
axes[1].set_ylabel('Speed (m/s)')
axes[1].grid(True)

# Subplot 3: Total Distance vs Time
axes[2].set_title('Total Distance Over Time')
axes[2].set_xlabel('Time')
axes[2].set_ylabel('Distance (m)')
axes[2].grid(True)

# Initialize lines for animation
altitude_line, = axes[0].plot([], [], color='blue', label='Altitude')
speed_line, = axes[1].plot([], [], color='red', label='Speed')
avg_speed_line, = axes[1].plot([], [], color='green', linestyle='--', label='Cumulative Avg Speed')
distance_line, = axes[2].plot([], [], color='purple', label='Distance')

# Add legends
axes[0].legend()
axes[1].legend()
axes[2].legend()

# Animation function
def update(frame):
    current_data = df.iloc[:frame]
    cumulative_avg_speed = current_data['Speed'].expanding().mean()
    
    altitude_line.set_data(current_data['Timestamp'], current_data['Altitude'])
    speed_line.set_data(current_data['Timestamp'], current_data['Speed'])
    avg_speed_line.set_data(current_data['Timestamp'], cumulative_avg_speed)
    distance_line.set_data(current_data['Timestamp'], current_data['Distance'])
    
    # Adjust x-axis limits dynamically
    for ax in axes:
        ax.set_xlim(df['Timestamp'].min(), df['Timestamp'].max())
    axes[0].set_ylim(0, df['Altitude'].max() * 1.1)
    axes[1].set_ylim(0, df['Speed'].max() * 1.1)
    axes[2].set_ylim(0, df['Distance'].max() * 1.1)
    return altitude_line, speed_line, avg_speed_line, distance_line

# Create animation
ani = FuncAnimation(fig, update, frames=len(df), interval=50, blit=True, repeat=False)

plt.tight_layout()
plt.show()
