import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import re
from io import BytesIO

def parse_gaussian_log(contents):
    """
    Parses Gaussian log file contents to extract frequencies and IR intensities.
    """
    freq_pattern = r"Frequencies -- ([\d\.\- ]+)"
    ir_intensity_pattern = r"IR Inten"
    frequencies, ir_intensities = [], []

    for line in contents.splitlines():
        if "Frequencies --" in line:
            freq_matches = re.search(freq_pattern, line)
            if freq_matches:
                frequencies.extend([float(f) for f in freq_matches.group(1).split()])
        elif "IR Inten" in line:
            words = line.split()
            for i in range(3,len(words)):
                ir_intensities.append(float(words[i]))

    return frequencies, ir_intensities

def gaussian(x, mu, sigma):
    return np.exp(-0.5 * ((x - mu) / sigma) ** 2)

def broadening(frequencies, intensities, sigma, num_points=1000):
    x_vals = np.linspace(min(frequencies) - 10 * sigma, max(frequencies) + 10 * sigma, num_points)
    y_vals = np.zeros(num_points)

    for freq, intensity in zip(frequencies, intensities):
        y_vals += intensity * gaussian(x_vals, freq, sigma)

    return x_vals, y_vals

def plot_spectrum(frequencies, intensities, title, color):
    sigma = 10  # Standard deviation for Gaussian broadening
    x_vals, y_vals = broadening(frequencies, intensities, sigma)

    plt.figure(figsize=(10, 4))
    plt.plot(x_vals, y_vals, color=color)
    plt.title(f"{title} Spectrum")
    plt.xlabel("Frequency (cm^-1)")
    plt.ylabel("Intensity")
    plt.grid(True)
    plt.xlim(5000, 0)

    plt.gca().invert_yaxis()  # Optional: Invert y-axis if needed

    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    return buf

st.title("IR Spectrum visualizer from Gaussian .log files")
uploaded_file = st.file_uploader("Upload your Gaussian .log file", type="log")
color = st.color_picker("Choose a color for the IR Spectrum plot", "#FF0000")

if uploaded_file is not None:
    contents = uploaded_file.getvalue().decode("utf-8")
    frequencies, ir_intensities = parse_gaussian_log(contents)

    if frequencies and ir_intensities:
        buf = plot_spectrum(frequencies, ir_intensities, "IR", color)
        st.pyplot(plt)
        st.download_button("Save plot", buf, "plot.png", "Download plot")
    else:
        st.error("No IR frequency or intensity data found in the file.")

# next step: add RAMAN as well
