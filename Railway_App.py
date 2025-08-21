
# Importing Libraries.
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Railway Dashboard" , layout='wide')

# Loadind Cleaned Dataset.
df = pd.read_csv('railway cleaned version.csv')
df["Date of Journey"] = pd.to_datetime(df["Date of Journey"])




# sidebar.
# 1- sidebar title.
st.sidebar.header("***Maven Railway Dashboard***") 

# 2- adding Image.
st.sidebar.image("Untitled design.png")

# 3- adding brief.
st.sidebar.markdown("An interactive dashboard to analyze Maven Railway operations data." \
"It provides insights into ticket sales, passenger trends, train routes, pricing, and revenue performance, helping to identify key patterns and improve decision-making.")


filtered_df = df.copy()



# 4- adding Filters.
st.sidebar.write("")
st.sidebar.markdown("**Filter Your Analysis🔍**") 

start_date = df["Date of Journey"].min()
end_date = df["Date of Journey"].max()

date_range = st.sidebar.date_input(
    "Select Journey Date Range",
    [start_date, end_date]
)

filtered_df = df[(df["Date of Journey"] >= start_date) & 
                 (df["Date of Journey"] <= end_date)]



Purchase_type = st.sidebar.selectbox("Purchase Type" , options= [None , 'Online' , 'Station'])
Payment_method = st.sidebar.selectbox("Payment Method" , [None , 'Credit Card' , 'Contactless' , 'Debit Card'])
railcard = st.sidebar.selectbox("Railcard" , options=df['Railcard'].unique())
journey_status = st.sidebar.multiselect("Journey Status" , options= df['Journey Status'].unique())
price_range = st.sidebar.slider(
    "Price Range",
    int(df["Price"].min()),   # min value in data
    int(df["Price"].max()),   # max value in data
    (int(df["Price"].min()), int(df["Price"].max()))  # default: full range
)

### Connect Filters With Graphs.


if len(date_range) == 2:
    filtered_df = filtered_df[
        (filtered_df["Date of Journey"] >= pd.to_datetime(date_range[0])) &
        (filtered_df["Date of Journey"] <= pd.to_datetime(date_range[1]))
    ]


## filter by purchase type.
if Purchase_type:
    filtered_df = filtered_df[ filtered_df['Purchase Type'] == Purchase_type ]

## filter by payment_method,
if Payment_method:
    filtered_df = filtered_df[ filtered_df['Payment Method'] == Payment_method ]

## filter by railcard.
if railcard:
    filtered_df = filtered_df[ filtered_df['Railcard'] == railcard ]


## filter by journey stauts.
if journey_status:
    filtered_df = filtered_df[filtered_df["Journey Status"].isin(journey_status)]

## filter by Price Range.
filtered_df = filtered_df[
    (filtered_df["Price"] >= price_range[0]) & (filtered_df["Price"] <= price_range[1])]


# 5- Main Page.

# first row of App.
st.subheader("**📊 Railway Overview**")


c1,c2,c3,c4,c5 = st.columns(5)

with c1:
    TotalRevenue = filtered_df['Price'].sum()
    st.metric("**💰 Total Revenue**", f"${TotalRevenue:,.0f}")

with c2:
    
    st.metric("👥 Total Passengers" , len(filtered_df))

with c3:
    total_journey = len(filtered_df)
    total_delay_journey = ( filtered_df['Journey Status'] == 'Delayed' ).sum() 
    Perce_for_dalay_journey = (total_delay_journey / total_journey ) * 100
    st.metric("⏱️ % Delay Trains" , f"{Perce_for_dalay_journey:.0f}%")
with c4:
    ontime_trips = (filtered_df["Journey Status"] == "On Time").sum()
    ontime_percentage = (ontime_trips / total_journey) * 100
    st.metric("🚆 On-time Journeys %", f"{ontime_percentage:.0f}%")
with c5:
    avg_price = filtered_df['Price'].mean()
    st.metric("🎟️ Average Ticket Price", f"${avg_price:.2f}")  


# second row of App.

c6, c7 = st.columns(2)




with c6:
    fig, ax = plt.subplots(facecolor="none")  
    ticket_type_counts = filtered_df["Ticket Type"].value_counts()
    colors = plt.cm.Set3(range(len(ticket_type_counts)))

    ax.pie(
        ticket_type_counts,
        labels=ticket_type_counts.index,
        autopct='%1.1f%%',
        startangle=90,
        colors=colors,
        textprops={'color': 'gray'} 
        
    )
    ax.axis("equal")
    ax.set_title(" Ticket Type Distribution", fontsize=14, fontweight="bold", color="white")  

    
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)
    ax.tick_params(colors="white")

    st.pyplot(fig, transparent=True)

with c7:
    fig, ax = plt.subplots(facecolor="none")  # خلي الخلفية شفافة
    colors = plt.cm.Set3(range(len(ticket_type_counts)))

    ax.hist(filtered_df['Price'], bins=20, color="skyblue", edgecolor="white")
    ax.set_title(" Price Distribution", fontsize=14, fontweight="bold", color="white")

    # خلي الخطوط والأرقام تظهر بلون أبيض عشان يبانوا في الدارك مود
    ax.tick_params(colors="white")
    ax.yaxis.label.set_color("white")
    ax.xaxis.label.set_color("white")

    # خلي الـ spines (الإطار حوالين الرسم) أبيض برضو
    for spine in ax.spines.values():
        spine.set_color("white")

    # شفافية الخلفية
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)
    ax.tick_params(colors="white")

    st.pyplot(fig, transparent=True)

c8,c9,c10 = st.columns(3)

with c8:
    fig, ax = plt.subplots()
    sns.boxplot(x='Ticket Type', y='Price', data=filtered_df, ax=ax , showfliers=False)

    # تحسين الشكل لو دارك مود
    ax.set_title(" Ticket Price Distribution", fontsize=14, fontweight="bold", color="white")
    ax.tick_params(colors="white")
    ax.yaxis.label.set_color("white")
    ax.xaxis.label.set_color("white")
    for spine in ax.spines.values():
        spine.set_color("white")

    ax.tick_params(colors="white")    

    st.pyplot(fig, transparent=True)

with c9:
    # تجميع البيانات بعدد العمليات
    payment_method_with_purchase_type = (
        filtered_df.groupby(["Payment Method", "Purchase Type"]).size().reset_index(name="Count")
    )
    
    ax.tick_params(colors="white")

    st.bar_chart(payment_method_with_purchase_type, x="Payment Method", y="Count", color="Purchase Type")

with c10:
    st.markdown("Revenue Trend by Day of Week")
    Revenue_per_week = filtered_df.groupby('Journey Day')["Price"].sum()

    ax.tick_params(colors="white")
    st.line_chart(Revenue_per_week , x_label="Days" , y_label="Total Revenue")



c11, = st.columns(1)   

with c11:
    st.title("Top 5 Common Routes")

    # حساب أكتر 5 Routes شيوعاً
    top_5_common_routes = filtered_df["Route"].value_counts().head(5).reset_index()
    top_5_common_routes.columns = ["Route", "Count"]

    # رسم البار تشارت
    fig, ax = plt.subplots(figsize=(8,6), facecolor="none")  # الخلفية None

    sns.barplot(
        x="Count", 
        y="Route", 
        data=top_5_common_routes, 
        ax=ax, 
        palette="Blues_r"   # تدريج ألوان أزرق
    )

    # تنسيقات إضافية
    ax.set_xlabel("Counts", fontsize=12, color="white")   # خلي النص أبيض زي الباي
    ax.set_ylabel("Routes", fontsize=12, color="white")
    ax.set_title("Top 5 Common Routes", fontsize=14, weight="bold", color="white")

    # خلي tick labels كمان أبيض
    ax.tick_params(axis="x", colors="white")
    ax.tick_params(axis="y", colors="white")

    # شفافية الخلفية
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)

    ax.tick_params(colors="white")
    # عرض الرسم على Streamlit
    st.pyplot(fig, transparent=True)
