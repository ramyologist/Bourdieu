import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def laden_und_berechnen_der_daten(uploaded_file):
    df = pd.read_excel(uploaded_file, skiprows=2)  # Überspringe die ersten beiden Zeilen
    df.fillna(0, inplace=True)  # Ersetze alle NaN mit 0

    # Konvertiere Spalten in numerische Werte, falls notwendig
    for col in df.columns[3:]:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Berechnung der Werte für das Diagramm
    df['Kulturelles Kapital'] = df.iloc[:, 3:8].mean(axis=1)
    df['Ökonomisches Kapital'] = df.iloc[:, 8:].mean(axis=1)
    df['X-Wert'] = df['Kulturelles Kapital'] - df['Ökonomisches Kapital']
    df['Y-Wert'] = df['Kulturelles Kapital'] + df['Ökonomisches Kapital']

    return df

def diagramm_erstellen(df):
    x_min, x_max = df['X-Wert'].min(), df['X-Wert'].max()
    y_min, y_max = df['Y-Wert'].min(), df['Y-Wert'].max()
    x_puffer = (x_max - x_min) * 0.1 if x_max > x_min else 1
    y_puffer = (y_max - y_min) * 0.1 if y_max > y_min else 1

    fig, ax = plt.subplots()
    ax.scatter(df['X-Wert'], df['Y-Wert'], c='blue', label='Teilnehmer')
    ax.axhline(0, color='black', linewidth=0.8)
    ax.axvline(0, color='black', linewidth=0.8)
    ax.set_xlim(x_min - x_puffer, x_max + x_puffer)
    ax.set_ylim(y_min - y_puffer, y_max + y_puffer)
    ax.set_title('Kreuzdiagramm des sozialen Raums')
    ax.set_xlabel('Kulturelles vs. Ökonomisches Kapital')
    ax.set_ylabel('Gesamtkapitalvolumen')
    ax.grid(True)
    ax.legend()
    return fig

st.title('Sozialer Raum Diagramm-Generator')

uploaded_file = st.file_uploader("Wählen Sie eine Excel-Datei aus", type="xlsx")
if uploaded_file is not None:
    df = laden_und_berechnen_der_daten(uploaded_file)
    fig = diagramm_erstellen(df)
    st.pyplot(fig)
