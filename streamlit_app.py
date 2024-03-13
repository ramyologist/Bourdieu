import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def laden_und_berechnen_der_daten(uploaded_file):
    df = pd.read_excel(uploaded_file)
    df = df.drop(index=[0, 1])
    df = df.fillna(0)
    cols_to_convert = df.columns[4:]
    df[cols_to_convert] = df[cols_to_convert].apply(pd.to_numeric, errors='coerce')
    df['Kulturelles Kapital'] = df.iloc[:, 4:9].mean(axis=1, skipna=True)
    df['Ökonomisches Kapital'] = df.iloc[:, 9:].mean(axis=1, skipna=True)
    df['X-Wert'] = df['Kulturelles Kapital'] - df['Ökonomisches Kapital']
    df['Y-Wert'] = df['Kulturelles Kapital'] + df['Ökonomisches Kapital']
    return df

def diagramm_erstellen(df):
    x_min, x_max = df['X-Wert'].min(), df['X-Wert'].max()
    y_min, y_max = df['Y-Wert'].min(), df['Y-Wert'].max()

    # Setze einen Puffer von 10% der Spanne, um sicherzustellen, dass alle Punkte sichtbar sind
    x_puffer = (x_max - x_min) * 0.1
    y_puffer = (y_max - y_min) * 0.1

    plt.figure(figsize=(10, 6))
    plt.scatter(df['X-Wert'], df['Y-Wert'], c='blue', label='Teilnehmer')
    plt.axhline(0, color='black', linewidth=0.8)
    plt.axvline(0, color='black', linewidth=0.8)
    plt.xlim(x_min - x_puffer, x_max + x_puffer)
    plt.ylim(y_min - y_puffer, y_max + y_puffer)
    plt.title('Kreuzdiagramm des sozialen Raums')
    plt.xlabel('Kulturelles vs. Ökonomisches Kapital')
    plt.ylabel('Gesamtkapitalvolumen')
    plt.grid(True)
    plt.legend()
    return plt

st.title('Sozialer Raum Diagramm-Generator')

uploaded_file = st.file_uploader("Wählen Sie eine Excel-Datei aus", type="xlsx")
if uploaded_file is not None:
    df = laden_und_berechnen_der_daten(uploaded_file)
    plt = diagramm_erstellen(df)
    st.pyplot(plt)
