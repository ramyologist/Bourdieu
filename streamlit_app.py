import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Antwortmöglichkeiten in numerische Werte umwandeln
antwort_codierung = {
    'keine': 0, 'weniger als 50': 1, '50-200': 2, 'mehr als 200': 3,
    'nie': 0, 'selten': 1, 'manchmal': 2, 'oft': 3,
    'kein Abschluss': 0, 'Sekundarstufe': 1, 'Hochschulreife': 2, 'Hochschulabschluss': 3,
    'kurzzeitig': 1, 'über mehrere Jahre': 2, 'aktuell noch': 3,
    'sehr angespannt': 0, 'angespannt': 1, 'ausreichend': 2, 'gut': 3,
    'im Wohnheim': 0, 'in einer WG': 1, 'alleine in einer Mietwohnung': 2, 
    'bei den Eltern/Verwandten': 3, 'Eigentumswohnung oder -haus': 4,
    'eigenes Einkommen': 3, 'Unterstützung durch Familie/Verwandte': 2, 'Stipendien/Bafög': 1, 'Kredite': 0,
    '1x/Jahr': 1, 'mehrmals pro Jahr': 2, 'regelmäßig': 3,
    'gering': 1, 'moderat': 2, 'umfangreich': 3
}

def laden_und_berechnen_der_daten(uploaded_file):
    df = pd.read_excel(uploaded_file)
    
    # Codierung der Antworten
    for column in df.columns:
        if column in antwort_codierung:
            df[column] = df[column].map(antwort_codierung)

    # Berechne das kulturelle und ökonomische Kapital
    df['Kulturelles Kapital'] = df.iloc[:, 1:6].mean(axis=1)
    df['Ökonomisches Kapital'] = df.iloc[:, 6:11].mean(axis=1)

    # Berechne die Werte für das Diagramm
    df['X-Wert'] = df['Kulturelles Kapital']
    df['Y-Wert'] = df['Ökonomisches Kapital']

    return df

def diagramm_erstellen(df):
    # Achsengrenzen dynamisch berechnen
    x_range = abs(df['X-Wert'].max() - df['X-Wert'].min())
    y_range = abs(df['Y-Wert'].max() - df['Y-Wert'].min())
    x_puffer = x_range * 0.1 if x_range else 0.5
    y_puffer = y_range * 0.1 if y_range else 0.5

    plt.figure(figsize=(10, 6))
    plt.scatter(df['X-Wert'], df['Y-Wert'], c='blue', label='Teilnehmer')
    plt.axhline(y=df['Y-Wert'].mean(), color='black', linestyle='--', linewidth=0.5)
    plt.axvline(x=df['X-Wert'].mean(), color='black', linestyle='--', linewidth=0.5)
    plt.xlim(df['X-Wert'].min() - x_puffer, df['X-Wert'].max() + x_puffer)
    plt.ylim(df['Y-Wert'].min() - y_puffer, df['Y-Wert'].max() + y_puffer)
    plt.title('Verteilung des sozialen Kapitals')
    plt.xlabel('Kulturelles Kapital')
    plt.ylabel('Ökonomisches Kapital')
    plt.grid(True)
    plt.legend()
    return plt

st.title('Sozialer Raum Diagramm-Generator')

uploaded_file = st.file_uploader("Wählen Sie eine Excel-Datei aus", type="xlsx")
if uploaded_file is not None:
    df = laden_und_berechnen_der_daten(uploaded_file)
    fig = diagramm_erstellen(df)
    st.pyplot(fig)
