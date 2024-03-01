import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')


def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule='D', on='dteday').agg({
        "cnt": "sum"
    })
    daily_orders_df = daily_orders_df.reset_index()
    daily_orders_df.rename(columns={
        "cnt": "rental_count"
    }, inplace=True)
    return daily_orders_df

def create_daily_register(df):
    daily_orders_df = df.resample(rule='D', on='dteday').agg({
        "registered": "sum"
    })
    daily_orders_df = daily_orders_df.reset_index()
    daily_orders_df.rename(columns={
        "registered": "register_count"
    }, inplace=True)
    return daily_orders_df

def create_daily_casual(df):
    daily_orders_df = df.resample(rule='D', on='dteday').agg({
        "casual": "sum"
    })
    daily_orders_df = daily_orders_df.reset_index()
    daily_orders_df.rename(columns={
        "casual": "casual_count"
    }, inplace=True)
    return daily_orders_df

def mean_per_season(df):
    per_season_df = df.groupby(['season'])[['casual', 'registered']].mean()
    return per_season_df

def mean_per_hour(df):
    per_hour_df = df.groupby("hr")["cnt"].agg("mean")
    return per_hour_df

# Pembagian kluster berdasarkan nilai temperatur
def temp_cluster(temp):
    if temp < 0.5:
        return 1
    elif temp >= 0.5 and temp < 0.75:
        return 2
    else:
        return 3

# Pembagian kluster berdasarkan nilai humidity
def hum_cluster(hum):
    if hum < 0.3:
        return 1
    elif hum >= 0.3 and hum < 0.6:
        return 2
    else:
        return 3

def clustering(df):
    df_cluster = df[['temp', 'hum']]
    df_cluster['temp_cluster'] = df_cluster['temp'].apply(temp_cluster)
    df_cluster['hum_cluster'] = df_cluster['hum'].apply(hum_cluster)
    return df_cluster


df_day = pd.read_csv("df_day.csv")
df_hour = pd.read_csv("df_hour.csv")

df_day["dteday"] = pd.to_datetime(df_day["dteday"])

min_date = df_day["dteday"].min()
max_date = df_day["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")

    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = df_day[(df_day["dteday"] >= str(start_date)) &
                (df_day["dteday"] <= str(end_date))]

per_hour_df = mean_per_hour(df_hour)
per_season_df = mean_per_season(main_df)
daily_orders_df = create_daily_orders_df(main_df)
daily_register_df = create_daily_register(main_df)
daily_casual_df = create_daily_casual(main_df)
df_cluster = clustering(df_day)

st.header('Bike Collection Dashboard :sparkles:')

st.subheader('Daily Orders')

col1, col2 , col3= st.columns(3)

# 3 teks diatas
with col1:
    total_orders = daily_orders_df.rental_count.sum()
    st.metric("Total Rental", value=total_orders)

with col2:
    total_registered = daily_register_df.register_count.sum()
    st.metric("Total Registered User", value=total_registered)

with col3:
    total_casual = daily_casual_df.casual_count.sum()
    st.metric("Total Casual User", value=total_casual)

# chart pertama
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_orders_df["dteday"],
    daily_orders_df["rental_count"],
    marker='o',
    linewidth=2,
    color="#90CAF9"
)

ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

# chart kedua
fig, ax = plt.subplots()
ax.plot(per_hour_df.index, per_hour_df.values)
ax.set_xticks(per_hour_df.index)
ax.set_xlabel("Jam")
ax.set_ylabel("Rata-rata Jumlah Rental")
ax.set_title("Rata-rata Jumlah Rental per Jam")
ax.axvline(x=17, color='red', linestyle='--')
ax.axvline(x=8, color='red', linestyle='--')

st.pyplot(fig)

# chart ketiga
nama_season = {1: 'Springer', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
fig, ax = plt.subplots(figsize=(8, 6))
per_season_df.plot(kind='bar', color=['green', 'red'], ax=ax)
ax.set_title('Rata-Rata User Casual dan Registered Tiap Musim')
ax.set_xlabel('Musim')
ax.set_xticks(range(0, 4))
ax.set_xticklabels(nama_season.values())
ax.set_ylabel('Rata-Rata User')
ax.legend(title='Tipe User')
ax.grid(axis='y', linestyle='--', alpha=0.7)

st.pyplot(fig)

# chart keempat
col1, col2= st.columns(2)
with col1:
    fig, ax = plt.subplots()
    scatter = ax.scatter(df_cluster['temp'], df_cluster['hum'], c=df_cluster['temp_cluster'], cmap='viridis')

    ax.set_xlabel('Temperatur')
    ax.set_ylabel('Humidity')
    ax.set_title('Pembagian Kluster Berdasarkan Temperatur')


    plt.colorbar(scatter, ax=ax, label='Cluster')

    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots()
    scatter = ax.scatter(df_cluster['temp'], df_cluster['hum'], c=df_cluster['hum_cluster'], cmap='viridis')

    ax.set_xlabel('Temperatur')
    ax.set_ylabel('Humidity')
    ax.set_title('Pembagian Kluster Berdasarkan Humidity')

    plt.colorbar(scatter, ax=ax, label='Cluster')

    st.pyplot(fig)