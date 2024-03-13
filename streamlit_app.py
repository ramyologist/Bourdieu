import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Angenommen, die ersten fünf Fragen (nach Datum, Session und Voter) sind für das kulturelle Kapital
# und die nächsten fünf Fragen für das ökonomische Kapital.
KULTURELLES_KAPITAL_START = 3  # Beginn bei der vierten Spalte
KULTURELLES_KAPITAL_END = 8  # Fünf Fragen für kulturelles Kapital
OEKONOMISCHES_KAPITAL_START = 8  # Beginn bei der neunten Spalte
OEKONOMISCHES_KAPITAL_END = 13  # Fünf Fragen für ökonomisches Kapital

def laden_und_berechnen_der_daten(uploaded_file):
    df = pd.read_excel(uploaded_file, skiprows=2)
    df.fillna(0, inplace=True)

    # Konvertiere Spalten in numerische Werte, falls notwendig
    for col in df.columns[KULTURELLES_KAPITAL_START:OEKONOMISCHES_KAPITAL_END]:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Berechnung der Werte für das Diagramm
    df['Kulturelles Kapital'] = df.iloc[:, KULTURELLES_KAPITAL_START:KULTURELLES_KAPITAL_END].mean(axis=1)
    df['Ökonomisches Kapital'] = df.iloc[:, OEKONOMISCHES_KAPITAL_START:OEKONOMISCHES_KAPITAL_END].mean(axis=1)
    df['X-Wert'] = df['Ökonomisches Kapital'] - df['Kulturelles Kapital']
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
    ax.set_xlabel('Ökonomisches Kapital (mehr ist links)')
    ax.set_ylabel('Kulturelles Kapital (mehr ist oben)')
    ax.grid(True)
    ax.legend()
    return fig

st.title('Sozialer Raum Diagramm-Generator')

uploaded_file = st.file_uploader("Wählen Sie eine Excel-Datei aus", type="xlsx")
if uploaded_file is not None:
    df = laden_und_berechnen_der_daten(uploaded_file)
    fig = diagramm_erstellen(df)
    st.pyplot(fig)
