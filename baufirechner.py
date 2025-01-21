import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import random
import time

# Generiere Zinssatz zufällig zwischen 3,1% und 3,5%
def get_random_interest_rate():
    return round(random.uniform(3.1, 3.3), 2) / 100  # Umwandlung in Dezimalform

# Berechnung der monatlichen Rate (Annuität)
def calculate_monthly_rate(kreditbetrag, zinssatz, laufzeit):
    r = zinssatz / 12  # Monatlicher Zinssatz
    n = laufzeit * 12  # Gesamtlaufzeit in Monaten
    annuitaet = kreditbetrag * (r * (1 + r)**n) / ((1 + r)**n - 1)
    return annuitaet

# Berechnung der Zins- und Tilgungsanteile über die Laufzeit
def calculate_zins_tilgung(kreditbetrag, zinssatz, laufzeit, monatliche_rate):
    zins_anteile = []
    tilgungs_anteile = []
    restschuld = kreditbetrag

    for _ in range(laufzeit * 12):
        zins = restschuld * (zinssatz / 12)  # Monatliche Zinsen
        tilgung = monatliche_rate - zins  # Monatliche Tilgung
        restschuld -= tilgung
        zins_anteile.append(zins)
        tilgungs_anteile.append(tilgung)

    return zins_anteile, tilgungs_anteile

# Berechnung des anfänglichen Tilgungssatzes
def calculate_initial_tilgungssatz(kreditbetrag, monatliche_rate, zinssatz):
    erste_monatszinsen = kreditbetrag * (zinssatz / 12)  # Zinsen der ersten Monatsrate
    erste_monatstilgung = monatliche_rate - erste_monatszinsen  # Tilgung der ersten Monatsrate
    erste_jahrestilgung = erste_monatstilgung * 12  # Tilgung auf das Jahr hochgerechnet
    return (erste_jahrestilgung / kreditbetrag) * 100  # Tilgungssatz in %

# Interaktive Eingaben
st.title("🏡 Baufinanzierungsrechner")
st.markdown("Berechnen Sie Ihre optimale monatliche Rate und gewinnen Sie einen Überblick über die Zinskosten! 📈")

# Schritt 1: Finanzierungsbedarf eingeben
st.markdown("### 🛠️ Schritt 1: Finanzierungsbedarf eingeben")
kreditbetrag = st.number_input("💰 Finanzierungsbedarf (€):", min_value=10000.0, max_value=1000000.0, step=1000.0, format="%.2f")

st.markdown("### 🛠️ Schritt 2: Laufzeit eingeben")
laufzeit = st.number_input("⏳ Gewünschte Laufzeit (in Jahren):", min_value=5, max_value=40, step=1)

st.markdown("### 🛠️ Schritt 3: Kapitaldienst eingeben")
kapitaldienst = st.number_input("🏦 Aktueller Kapitaldienst (€):", min_value=0.0, step=100.0, format="%.2f")

# Berechnung starten Button immer anzeigen
if st.button("📊 Berechnung starten"):
    if kreditbetrag and laufzeit and kapitaldienst:
        with st.spinner("🔄 Berechnung wird durchgeführt..."):
            time.sleep(2)  # Simulierte Ladezeit

        zinssatz = get_random_interest_rate()
        monatliche_rate = calculate_monthly_rate(kreditbetrag, zinssatz, laufzeit)

        # Laufzeit anpassen, falls Kapitaldienst nicht ausreicht
        original_laufzeit = laufzeit
        while monatliche_rate > kapitaldienst and laufzeit < 40:
            laufzeit += 1
            monatliche_rate = calculate_monthly_rate(kreditbetrag, zinssatz, laufzeit)

        if monatliche_rate > kapitaldienst:
            st.error("❌ Selbst bei einer Laufzeit von 40 Jahren passt die Rate nicht in den Kapitaldienst.")
        elif laufzeit > original_laufzeit:
            st.markdown(
                f"⚠️ **Die Laufzeit wurde auf {laufzeit} Jahre verlängert, um die monatliche Rate an den Kapitaldienst anzupassen.**"
            )

        # Berechnung von Zins- und Tilgungsanteilen
        zins_anteile, tilgungs_anteile = calculate_zins_tilgung(kreditbetrag, zinssatz, laufzeit, monatliche_rate)
        gesamtzins = sum(zins_anteile)
        gesamtaufwand = gesamtzins + kreditbetrag

        # Anfänglicher Tilgungssatz
        anf_tilgungssatz = calculate_initial_tilgungssatz(kreditbetrag, monatliche_rate, zinssatz)

        # Ergebnisse anzeigen
        st.markdown("## 📋 Ergebnisse")
        st.markdown(
            f"""
            ### 💵 Monatliche Rate
            **{monatliche_rate:,.2f} €**
            *Der Betrag, den Sie monatlich zahlen würden.*

            ### 🔍 Zinssatz
            **{zinssatz * 100:.2f}%**
            *Der Zinssatz entspricht Ihrer Bonität, Ihrem Eigenkapital und weiteren Faktoren.*

            ### 🧮 Anfänglicher Tilgungssatz
            **{anf_tilgungssatz:.2f}%**
            *Der prozentuale Anteil der Tilgung im ersten Jahr.*

            ### 📉 Gesamter Zinsaufwand
            **{gesamtzins:,.2f} €**
            *Die gesamten Kosten durch Zinsen während der Laufzeit.*

            ### 💸 Gesamtaufwand (Kreditbetrag + Zinsen)
            **{gesamtaufwand:,.2f} €**
            *Die Gesamtsumme aller Zahlungen während der Laufzeit.*
            """
        )
    else:
        st.error("❌ Bitte geben Sie alle notwendigen Informationen ein, bevor Sie die Berechnung starten.")










