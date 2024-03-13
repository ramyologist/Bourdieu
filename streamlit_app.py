import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def laden_und_berechnen_der_daten(uploaded_file):
    umfrage_ergebnisse = pd.read_excel(uploaded_file)
    umfrage_daten = umfrage_ergebnisse.iloc[2:, 3:].reset_index(drop=True) # Beginn der Daten ab der dritten Zeile und vierten Spalte annehmen
    umfrage_daten.columns = [
        'Bücher', 'Kulturelle Veranstaltungen', 'Bildungsniveau Eltern',
        'Lesen außerhalb', 'Kunstunterricht', 'Finanzielle Situation',
        'Wohnsituation', 'Studienfinanzierung', 'Urlaube', 'Ersparnisse'
    ]
    
    # Konvertierung der Antworten in numerische Werte
    for col in umfrage_daten.columns:
        umfrage_daten[col] = pd.to_numeric(umfrage_daten[col], errors='coerce')
    
    umfrage_daten['Kulturelles Kapital'] = umfrage_daten[['Bücher', 'Kulturelle Veranstaltungen', 'Bildungsniveau Eltern', 'Lesen außerhalb', 'Kunstunterricht']].mean(axis=1, skipna=True)
    umfrage_daten['Ökonomisches Kapital'] = umfrage_daten[['Finanzielle Situation', 'Wohnsituation', 'Studienfinanzierung', 'Urlaube', 'Ersparnisse']].mean(axis=1, skipna=True)
    
    umfrage_daten['X-Wert'] = umfrage_daten['Ökonomisches Kapital'] - umfrage_daten['Kulturelles Kapital']
    umfrage_daten['Y-Wert'] = umfrage_daten['Kulturelles Kapital'] + umfrage_daten['Ökonomisches Kapital']

    return umfrage_daten

def diagramm_erstellen(umfrage_daten):
    fig, ax = plt.subplots()
    ax.scatter(umfrage_daten['X-Wert'], umfrage_daten['Y-Wert'], c='blue', label='Teilnehmer')
    ax.axhline(0, color='black', linewidth=0.8)
    ax.axvline(0, color='black', linewidth=0.8)

    # Anpassung der Achsen um 10% über den größten absoluten Wert hinaus
    x_range = max(abs(umfrage_daten['X-Wert'].max()), abs(umfrage_daten['X-Wert'].min())) * 1.1
    y_range = max(abs(umfrage_daten['Y-Wert'].max()), abs(umfrage_daten['Y-Wert'].min())) * 1.1

    ax.set_xlim(-x_range if x_range != 0 else -1, x_range if x_range != 0 else 1)
    ax.set_ylim(-y_range if y_range != 0 else -1, y_range if y_range != 0 else 1)

    ax.set_title('Kreuzdiagramm des sozialen Raums')
    ax.set_xlabel('Kulturelles vs. Ökonomisches Kapital')
    ax.set_ylabel('Gesamtkapitalvolumen')
    ax.grid(True)
    ax.legend()

    return fig

st.title('Sozialer Raum Diagramm-Generator')

uploaded_file = st.file_uploader("Wählen Sie eine Excel-Datei aus", type="xlsx")
if uploaded_file is not None:
    umfrage_daten = laden_und_berechnen_der_daten(uploaded_file)
    fig = diagramm_erstellen(umfrage_daten)
    st.pyplot(fig)
