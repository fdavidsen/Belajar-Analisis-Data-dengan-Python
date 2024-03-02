import pandas as pd
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt


# Helper function
def create_daily_freq_df(df):
    return df.groupby("date")["cnt"].sum().reset_index()

def create_musim_freq_df(df):
    musim_freq_df = df.groupby("season")["cnt"].sum().reset_index().sort_values(by="cnt", ascending=False)
    musim_freq_df["season"] = musim_freq_df["season"].map({1: "Semi", 2: "Panas", 3: "Gugur", 4: "Dingin"})
    
    return musim_freq_df

def create_suhu_freq_df(df):
    return df.groupby("suhu")["cnt"].mean().reset_index().sort_values(by="cnt", ascending=False)

def create_jam_freq_df(df):
    return df.groupby("hr")["cnt"].sum().sort_values(ascending=False).reset_index()

def convert_year(year):
    return 0 if year == 2011 else 1



# Load data
df = pd.read_csv("main_data.csv")

df.drop(columns=["instant"], inplace=True)
df.rename({"dteday": "date"}, axis=1, inplace=True)

df["date"] = pd.to_datetime(df["date"])
df["holiday"] = df["holiday"].astype(bool)
df["workingday"] = df["workingday"].astype(bool)

df["atemp"] = df["atemp"].apply(lambda x: x * 50)
df["suhu"] = df["atemp"].apply(lambda x: "Dingin" if x < 25 else ("Normal" if x > 32 else "Panas"))



# Menyiapkan DataFrame
min_year = 2011
max_year = 2012
temp_df = df[(df["yr"] >= convert_year(min_year)) & (df["yr"] <= convert_year(max_year))]



with st.sidebar:
    min_year = st.number_input(label='Start Year', min_value=2011, max_value=2012, value=min_year)
    max_year = st.number_input(label='End Year', min_value=min_year, max_value=2012, value=max_year)
    
    temp_df = df[(df["yr"] >= convert_year(min_year)) & (df["yr"] <= convert_year(max_year))]
    
    daily_freq_df = create_daily_freq_df(temp_df)
    musim_freq_df = create_musim_freq_df(temp_df)
    suhu_freq_df = create_suhu_freq_df(temp_df)
    jam_freq_df = create_jam_freq_df(temp_df)
    
    
    
st.header("Frederic's Analysis Dashboard :sparkles:")



st.subheader("Transaksi Harian")

fig, ax = plt.subplots(figsize=(16, 8))
sns.lineplot(
    x="date",
    y="cnt",
    data=daily_freq_df,
    ax=ax
)
ax.set_xlabel(None)
ax.set_ylabel(None)

st.pyplot(fig)



st.subheader("Pengaruh Cuaca Terhadap Jumlah Transaksi")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 8))

sns.barplot(
    x="cnt",
    y="season",
    orient="h",
    order=musim_freq_df["season"],
    data=musim_freq_df,
    ax=ax[0]
)
ax[0].set_xlabel(None)
ax[0].set_ylabel(None)
ax[0].set_title("Musim", loc="center", fontsize=35)
ax[0].tick_params(axis='y', labelsize=20)

sns.barplot(
    x="cnt",
    y="suhu",
    orient="h",
    order=suhu_freq_df["suhu"],
    data=suhu_freq_df
)
ax[1].set_xlabel(None)
ax[1].set_ylabel(None)
ax[1].set_title("Suhu", loc="center", fontsize=35)
ax[1].tick_params(axis='y', labelsize=20)

st.pyplot(fig)



st.subheader("Jumlah Transaksi Tertinggi Terhadap Jam")

st.metric("Average Frequency Per Hour", value=round(jam_freq_df["cnt"].mean(), 2))

fig, ax = plt.subplots()
sns.barplot(
    x="hr",
    y="cnt",
    data=jam_freq_df.head(),
    ax=ax
)
ax.set_xlabel(None)
ax.set_ylabel(None)
ax.set_title("Musim", loc="center", fontsize=16)
ax.tick_params(axis='y', labelsize=8)

st.pyplot(fig)