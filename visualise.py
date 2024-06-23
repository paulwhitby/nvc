"""chatgpt-created program to visualise succession"""

import pandas as pd
# import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Define the succession data
data = {
    "Succession Stage": [
        "Initial Stage",
        "Early Successional Stage",
        "Mid-Successional Stage",
        "Mid-Successional Stage",
        "Late Successional Stage",
        "Late Successional Stage",
        "Potential Climax Community",
        "Potential Climax Community"
    ],
    "Community Type": [
        "Post-Disturbance Colonization",
        "Formation of Duckweed Communities",
        "Development of Submerged Vegetation",
        "Emergence of Floating-Leaved Macrophytes",
        "Establishment of Emergent Vegetation",
        "Establishment of Emergent Vegetation",
        "Stable Duckweed and Mixed Communities",
        "Impact of Eutrophication"
    ],
    "Description": [
        "Lemnetum gibbae is the only aquatic vegetation present after disturbance.",
        "Lemnetum gibbae coexists with other duckweed communities like Lemnetum minoris.",
        "Submerged plants develop beneath the duckweed mats (e.g., Ceratophyllum submersum, Elodea canadensis).",
        "Floating-leaved macrophytes grow among the duckweed mats (e.g., Potamogeton natans, Nuphar lutea).",
        "Emergent vegetation dominates and provides shelter for duckweed mats (e.g., Sparganietum erecti, Typhetum latifoliae).",
        "Emergent vegetation dominates and provides shelter for duckweed mats (e.g., Phragmitetum).",
        "Stable communities of Lemnetum gibbae alone or in mosaics with other plants (e.g., Spirodela-Hydrocharis).",
        "Lemnetum gibbae becomes dominant in eutrophic conditions, leading to a more stable but impoverished community."
    ]
}

# Create the DataFrame
df = pd.DataFrame(data)

# Create the plot
fig, ax = plt.subplots(figsize=(10, 6))
plt.axis('off')

def update(num, df, plot_text):
    plot_text.set_text(f"{df['Succession Stage'][num]}:\n\n{df['Community Type'][num]}\n\n{df['Description'][num]}")

plot_text = ax.text(0.5, 0.5, '', ha='center', va='center', fontsize=12, wrap=True)

ani = animation.FuncAnimation(fig, update, frames=len(df), fargs=[df, plot_text], interval=2000, repeat=True)

plt.show()
