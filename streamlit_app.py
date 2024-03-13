import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO


def diagramm_erstellen(umfrage_daten):
    # Berechnung der neuen X- und Y-Werte für die neuen Daten
    umfrage_daten['X-Wert'] = umfrage_daten['Kulturelles Kapital'] - umfrage_daten['Ökonomisches Kapital']
    umfrage_daten['Y-Wert'] = umfrage_daten['Kulturelles Kapital'] + umfrage_daten['Ökonomisches Kapital']

    plt.figure(figsize=(10, 6))
    plt.scatter(umfrage_daten['X-Wert'], umfrage_daten['Y-Wert'], c='blue', label='Teilnehmer')
    plt.axhline(0, color='black', linewidth=0.8)
    plt.axvline(0, color='black', linewidth=0.8)
    plt.title('Kreuzdiagramm des sozialen Raums')
    plt.xlabel('Kulturelles vs. Ökonomisches Kapital')
    plt.ylabel('Gesamtkapitalvolumen')
    plt.grid(True)
    plt.legend()
    return plt


def laden_und_berechnen_der_daten(uploaded_file):
    umfrage_ergebnisse = pd.read_excel(uploaded_file)
    umfrage_daten = umfrage_ergebnisse.drop(index=[0, 1]).reset_index(drop=True)
    umfrage_daten.columns = [
        'Datum', 'Session', 'Voter', 'Instructions',
        'Bücher', 'Kulturelle Veranstaltungen', 'Bildungsniveau Eltern',
        'Lesen außerhalb', 'Kunstunterricht', 'Finanzielle Situation',
        'Wohnsituation', 'Studienfinanzierung', 'Urlaube', 'Ersparnisse'
    ]

    # Hier müsste die Codierung angepasst werden
    codierung = {
        # Fügen Sie hier die Codierung für jede Antwortmöglichkeit ein
    }

    for column in umfrage_daten.columns[4:]:
        umfrage_daten[column] = umfrage_daten[column].apply(lambda x: codierung.get(x, x))

    umfrage_daten['Kulturelles Kapital'] = umfrage_daten[
        ['Bücher', 'Kulturelle Veranstaltungen', 'Bildungsniveau Eltern', 'Lesen außerhalb', 'Kunstunterricht']].mean(
        axis=1)
    umfrage_daten['Ökonomisches Kapital'] = umfrage_daten[
        ['Finanzielle Situation', 'Wohnsituation', 'Studienfinanzierung', 'Urlaube', 'Ersparnisse']].mean(axis=1)

    return umfrage_daten


st.title('Sozialer Raum Diagramm-Generator')

uploaded_file = st.file_uploader("Wählen Sie eine Excel-Datei aus", type="xlsx")
if uploaded_file is not None:
    umfrage_daten = laden_und_berechnen_der_daten(uploaded_file)
    plt = diagramm_erstellen(umfrage_daten)
    st.pyplot(plt)
