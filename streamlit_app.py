import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import re

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

def plot_spectrum(frequencies, intensities, title, color):
    """
    Plots a spectrum given frequencies and intensities.
    """
    plt.figure(figsize=(10, 4))
    plt.stem(frequencies, intensities, linefmt=color, markerfmt=' ', basefmt=" ")
    plt.title(f"{title} Spectrum")
    plt.xlabel("Frequency (cm^-1)")
    plt.ylabel("Intensity")
    plt.grid(True)
    st.pyplot(plt)

# Streamlit UI components
st.title('Gaussian .log File IR Spectrum Analyzer')
uploaded_file = st.file_uploader("Upload your Gaussian .log file", type="log")
color = st.color_picker("Choose a color for the IR Spectrum plot", "#FF0000")


if uploaded_file is not None:
    contents = uploaded_file.getvalue().decode("utf-8")
    frequencies, ir_intensities = parse_gaussian_log(contents)
    print("frequencies", frequencies)
    print("IR intensities",ir_intensities)
    if frequencies and ir_intensities:
        plot_spectrum(frequencies, ir_intensities, "IR", color)
    else:
        st.error("No IR frequency or intensity data found in the file.")

