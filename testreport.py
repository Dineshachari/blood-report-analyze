import matplotlib.pyplot as plt

# Define the bands
low_band = 70
normal_band = 140
elevated_band = 180

# Define the data points
months = ['September', 'October', 'November']
values = [150, 232, 252]

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(months, values, marker='o', color='blue')

# Color the bands
plt.axhspan(0, low_band, color='red', alpha=0.3)
plt.axhspan(low_band, normal_band, color='green', alpha=0.3)
plt.axhspan(normal_band, elevated_band, color='yellow', alpha=0.3)
plt.axhspan(elevated_band, 300, color='red', alpha=0.3)

# Set the title and labels
plt.title('Blood Sugar Levels')
plt.xlabel('Month')
plt.ylabel('mg/dL')

# Show the plot
plt.show()


