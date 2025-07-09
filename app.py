
import streamlit as st
import pandas as pd
import openai
import os

st.set_page_config(page_title="🎯 Facebook Ads Analyzer IA", layout="wide")

st.image("assets/logo.png", width=150)
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>📊 Facebook Ads Analyzer avec Intelligence Artificielle</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size:18px;'>Analysez, optimisez et améliorez vos performances publicitaires grâce à l’IA.</p>", unsafe_allow_html=True)
st.markdown("---")

uploaded_file = st.file_uploader("📁 Importez un fichier CSV de vos données Facebook Ads", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("✅ Fichier chargé avec succès !")

    with st.expander("🧾 Aperçu des données"):
        st.dataframe(df.head())

    st.markdown("### 🔍 Analyse des indicateurs clés")
    try:
        col1, col2, col3 = st.columns(3)
        cpc = df['amount_spent'].sum() / df['clicks'].sum()
        ctr = (df['clicks'].sum() / df['impressions'].sum()) * 100
        roas = df['purchase_value'].sum() / df['amount_spent'].sum()
        col1.metric("💰 CPC Moyen", f"{cpc:.2f} €")
        col2.metric("📈 CTR Moyen", f"{ctr:.2f} %")
        col3.metric("🔁 ROAS", f"{roas:.2f}")
    except Exception as e:
        st.error("⚠️ Vérifiez que le CSV contient les colonnes : amount_spent, clicks, impressions, purchase_value.")

    st.markdown("---")
    st.markdown("### 🤖 Recommandations IA personnalisées")
    if st.button("✨ Générer avec IA"):
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        prompt = f"""Voici un résumé des performances :\n{df.describe(include='all')}\n\nFournis des recommandations concrètes pour améliorer les campagnes Facebook Ads."""

        with st.spinner("💡 L'IA analyse vos données..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}]
                )
                st.success("✅ Recommandations générées !")
                st.markdown("#### 💡 Suggestions stratégiques")
                st.write(response.choices[0].message.content)
            except Exception as e:
                st.error(f"Erreur OpenAI : {e}")
else:
    st.info("⏳ Veuillez importer un fichier CSV pour commencer.")
