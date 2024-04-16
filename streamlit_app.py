import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import re

def parse_gaussian_log(contents):
    """ Parses Gaussian log file contents to extract frequencies, IR and Raman intensities. """
    freq_pattern = r"Frequencies -- ([\d\.\- ]+)"
    ir_intensity_pattern = r"IR Inten -- ([\d\.\- ]+)"
    raman_intensity_pattern = r"Raman Activ -- ([\d\.\- ]+)"

    frequencies, ir_intensities, raman_intensities = [], [], []
    n_atoms = 0

    for line in contents.splitlines():
        if "NAtoms=" in line:
            n_atoms = int(line.split('=')[1])
        if re.search(freq_pattern, line):
            frequencies.extend([float(f) for f in re.search(freq_pattern, line).group(1).split()])
        if re.search(ir_intensity_pattern, line):
            ir_intensities.extend([float(i) for i in re.search(ir_intensity_pattern, line).group(1).split()])
        if re.search(raman_intensity_pattern, line):
            raman_intensities.extend([float(r) for r in re.search(raman_intensity_pattern, line).group(1).split()])

    return frequencies, ir_intensities, raman_intensities, n_atoms

def plot_spectrum(frequencies, intensities, title, color):
    """ Plots a spectrum given frequencies and intensities. """
    if not intensities:
        st.write(f"No data for {title}")
        return

    plt.figure(figsize=(10, 4))
    plt.plot(frequencies, intensities, color=color)
    plt.title(f"{title} Spectrum")
    plt.xlabel("Frequency (cm-1)")
    plt.ylabel("Intensity")
    plt.grid(True)
    st.pyplot(plt)

# Streamlit UI components
st.title('Gaussian .log File Analyzer')
uploaded_file = st.file_uploader("Upload your Gaussian .log file", type="log")
color_ir = st.color_picker("Choose a color for IR Spectrum", "#FF0000")
color_raman = st.color_picker("Choose a color for Raman Spectrum", "#0000FF")

if uploaded_file is not None:
    contents = uploaded_file.getvalue().decode("utf-8")
    frequencies, ir_intensities, raman_intensities, n_atoms = parse_gaussian_log(contents)

    if n_atoms == 0:
        st.error("No atomic data found in file.")
    else:
        st.write(f"Number of atoms: {n_atoms}")
        plot_spectrum(frequencies, ir_intensities, "IR", color_ir)
        plot_spectrum(frequencies, raman_intensities, "Raman", color_raman)

