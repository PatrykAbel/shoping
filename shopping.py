import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Wczytaj dane
@st.cache_data
def load_data():
    return pd.read_csv('shopping_trends (2).csv')

data = load_data()

# Ustawienia strony
st.title("Shopping Trends Dashboard")
st.sidebar.title("Opcje analizy")

# Nowe filtry
age_filter = st.sidebar.slider("Wiek klienta", int(data["Age"].min()), int(data["Age"].max()), (18, 60))
category_filter = st.sidebar.multiselect("Kategorie produktów", data["Category"].unique(), data["Category"].unique())
gender_filter = st.sidebar.multiselect("Płeć klienta", data["Gender"].unique(), data["Gender"].unique())
price_range = st.sidebar.slider("Zakres kwoty zakupów (USD)", float(data["Purchase Amount (USD)"].min()), float(data["Purchase Amount (USD)"].max()), (0.0, 500.0))
season_filter = st.sidebar.multiselect("Sezon zakupów", data["Season"].unique(), data["Season"].unique())

# Filtruj dane
filtered_data = data[(data["Age"] >= age_filter[0]) &
                     (data["Age"] <= age_filter[1]) &
                     (data["Category"].isin(category_filter)) &
                     (data["Gender"].isin(gender_filter)) &
                     (data["Purchase Amount (USD)"] >= price_range[0]) &
                     (data["Purchase Amount (USD)"] <= price_range[1]) &
                     (data["Season"].isin(season_filter))]

# Wyświetlanie danych
st.write("### Filtrowane dane", filtered_data)

# Wykresy
st.write("## Analiza wizualna")

# Wykres 1: Zakupy wg kategorii
st.write("### Liczba zakupów wg kategorii")
category_counts = filtered_data["Category"].value_counts()
fig, ax = plt.subplots()
category_counts.plot(kind="bar", ax=ax)
ax.set_xlabel("Kategoria")
ax.set_ylabel("Liczba zakupów")
st.pyplot(fig)

# Wykres 2: Średnia kwota zakupów wg sezonu
st.write("### Średnia kwota zakupów wg sezonu")
season_mean = filtered_data.groupby("Season")["Purchase Amount (USD)"].mean()
fig, ax = plt.subplots()
season_mean.plot(kind="bar", ax=ax)
ax.set_xlabel("Sezon")
ax.set_ylabel("Średnia kwota zakupów (USD)")
st.pyplot(fig)

# Nowy wykres: Wykres kołowy dla płci klientów
st.write("### Proporcja płci klientów")
gender_counts = filtered_data["Gender"].value_counts()
fig, ax = plt.subplots()
ax.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', startangle=90, colors=["#ff9999", "#66b3ff"])
ax.axis('equal')
st.pyplot(fig)

# Nowy wykres: Wykres liniowy średnich wydatków wg wieku
st.write("### Średnia kwota zakupów wg wieku")
age_mean_spend = filtered_data.groupby("Age")["Purchase Amount (USD)"].mean()
fig, ax = plt.subplots()
age_mean_spend.plot(kind="line", ax=ax)
ax.set_xlabel("Wiek")
ax.set_ylabel("Średnia kwota zakupów (USD)")
st.pyplot(fig)

# Nowy wykres: Boxplot kwoty zakupów wg kategorii
st.write("### Rozkład kwoty zakupów w różnych kategoriach")
fig, ax = plt.subplots(figsize=(10, 5))
sns.boxplot(x="Category", y="Purchase Amount (USD)", data=filtered_data, ax=ax)
ax.set_xlabel("Kategoria")
ax.set_ylabel("Kwota zakupów (USD)")
plt.xticks(rotation=45)
st.pyplot(fig)
