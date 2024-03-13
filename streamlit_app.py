import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def laden_und_berechnen_der_daten(uploaded_file):
    # Lese die Excel-Datei
    df = pd.read_excel(uploaded_file)
    
    # Entfernen der nicht relevanten Zeilen und Spalten
    df = df.drop(index=[0, 1])
    
    # Ersetze NaN durch 0 oder eine geeignete Zahl
    df = df.fillna(0)

    # Konvertiere alle relevanten Spalten in numerische Werte
    cols_to_convert = df.columns[4:]  # oder eine genaue Liste der Spalten
    df[cols_to_convert] = df[cols_to_convert].apply(pd.to_numeric, errors='coerce')

    # Berechne das kulturelle und ökonomische Kapital
    df['Kulturelles Kapital'] = df.iloc[:, 4:9].mean(axis=1, skipna=True)
    df['Ökonomisches Kapital'] = df.iloc[:, 9:].mean(axis=1, skipna=True)

    # Berechne X-Wert und Y-Wert
    df['X-Wert'] = df['Kulturelles Kapital'] - df['Ökonomisches Kapital']
    df['Y-Wert'] = df['Kulturelles Kapital'] + df['Ökonomisches Kapital']
    return df
def diagramm_erstellen(umfrage_daten):
    # Erweiterung der Achsen für eine bessere Sichtbarkeit
    x_range = max(abs(umfrage_daten['X-Wert'].max()), abs(umfrage_daten['X-Wert'].min())) * 1.1
    y_range = max(abs(umfrage_daten['Y-Wert'].max()), abs(umfrage_daten['Y-Wert'].min())) * 1.1

    plt.figure(figsize=(10, 6))
    plt.scatter(umfrage_daten['X-Wert'], umfrage_daten['Y-Wert'], c='blue', label='Teilnehmer')
    plt.axhline(0, color='black', linewidth=0.8)
    plt.axvline(0, color='black', linewidth=0.8)
    plt.xlim(-x_range, x_range)
    plt.ylim(-y_range, y_range)
    plt.title('Kreuzdiagramm des sozialen Raums')
    plt.xlabel('Kulturelles vs. Ökonomisches Kapital')
    plt.ylabel('Gesamtkapitalvolumen')
    plt.grid(True)
    plt.legend()
    st.pyplot()


st.title('Sozialer Raum Diagramm-Generator')

uploaded_file = st.file_uploader("Wählen Sie eine Excel-Datei aus", type="xlsx")
if uploaded_file is not None:
    df = laden_und_berechnen_der_daten(uploaded_file)
    plt = diagramm_erstellen(df)
    st.pyplot(plt)
