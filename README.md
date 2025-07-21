# 🏎️ F1 Race & Qualifying Predictor

A machine learning-powered system that predicts **qualifying times**, **race outcomes**, and **winning probabilities** for upcoming Formula 1 Grand Prix weekends — using historical race data, track characteristics, weather forecasts, and driver performance trends.

> [!IMPORTANT]  
> This project now uses **real Formula 1 data** via the Fast-F1 API, making predictions more accurate and realistic. The simulation combines historical F1 performance data with advanced modeling algorithms.

---

## 🎯 Project Goals

This project aims to answer key performance questions like:

- What will a driver's **qualifying time** be on a given track?
- How long will their **race time** be given tire strategies and weather?
- Who is **most likely to win** the upcoming Grand Prix?

By combining real-world motorsport data with predictive modeling, the project teaches advanced ML & AI skills while building a realistic F1 simulation engine.

---

## 🧱 Core Features

- ✅ **Track-aware prediction**: Considers circuit layout, length, speed profile, corner count.
- 🌡️ **Weather-influenced pace**: Uses real or simulated air temp, track temp, humidity, wind.
- 🏁 **Qualifying Time Prediction**: Regression models using XGBoost/LightGBM.
- 🕰️ **Race Time Estimation**: Predict race stints, pit stops, and total time.
- 🥇 **Winner Prediction**: Classifier to estimate the most likely race winner.
- 📊 **Visualization & Dashboards**: Streamlit interface to explore predictions and run simulations.

---

## 📊 Data Sources

- [FastF1 API](https://theoehrly.github.io/Fast-F1/)
- [Ergast F1 API](https://ergast.com/mrd/)
- Real-time or synthetic weather conditions
- Manually curated track metadata (length, corner count, etc.)
