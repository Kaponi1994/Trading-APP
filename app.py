import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import ta

st.set_page_config(page_title="Analizador Trading", layout="centered")
st.title("📈 Analizador de Señales de Trading")

ticker = st.text_input("Símbolo del activo (ej. BTC-USD, AAPL, EURUSD=X):", "BTC-USD").upper()
periodo = st.selectbox("Período de análisis:", ["3mo", "6mo", "1y", "2y"], index=2)

if st.button("Analizar Mercado"):
    with st.spinner("Descargando datos y generando gráfico..."):
        df = yf.download(ticker, period=periodo, interval="1d")
        
        if df.empty:
            st.error("No se encontraron datos. Revisa el símbolo ingresado.")
        else:
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)

            df['SMA_20'] = ta.trend.sma_indicator(df['Close'], window=20)
            df['SMA_50'] = ta.trend.sma_indicator(df['Close'], window=50)
            df['RSI'] = ta.momentum.rsi(df['Close'], window=14)

            df['Alza'] = (df['SMA_20'] > df['SMA_50']) & (df['SMA_20'].shift(1) <= df['SMA_50'].shift(1)) & (df['RSI'] < 70)
            df['Baja'] = (df['SMA_20'] < df['SMA_50']) & (df['SMA_20'].shift(1) >= df['SMA_50'].shift(1)) & (df['RSI'] > 30)

            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(df.index, df['Close'], label='Precio', color='black', alpha=0.7)
            ax.plot(df.index, df['SMA_20'], label='Media 20', color='blue', linestyle='--')
            ax.plot(df.index, df['SMA_50'], label='Media 50', color='orange', linestyle='--')

            ax.scatter(df.index[df['Alza']], df['Close'][df['Alza']], label='Posible Alza', marker='^', color='green', s=120, zorder=5)
            ax.scatter(df.index[df['Baja']], df['Close'][df['Baja']], label='Posible Baja', marker='v', color='red', s=120, zorder=5)

            ax.set_title(f'Análisis - {ticker}')
            ax.legend()
            ax.grid(True, alpha=0.3)

            st.pyplot(fig)
            st.caption("⚠️ Herramienta educativa. No representa asesoría financiera.")
          
