import streamlit as st
import pandas as pd

import matplotlib.pyplot as plt

import seaborn as sns



st.set_page_config(layout="wide",page_title="Startup Analysis")

df = pd.read_csv("startup_cleaned(2).csv")

df["date"] = pd.to_datetime(df["date"],errors="coerce")

df["month"] = df["date"].dt.month

df["year"] = df["date"].dt.year

def load_overall_analysis():
    st.title("Overall Analysis")

    #total invested amount
    total = (round(df["amount"].sum()))

    #max amount infused in a startup
    max_funding = df.groupby("startup")["amount"].max().sort_values(ascending=False).head(1).values[0]

    #avg ticket size

    avg_funding = df.groupby("startup")["amount"].sum().mean()

    #total funded startups

    num_startups = df["startup"].nunique()


    col1,col2,col3,col4 = st.columns(4)

    with col1:
        st.metric("Total",str(total) +"Cr")

    with col2:
        st.metric("Max",str(max_funding)+"Cr")

    with col3:
        st.metric("Avg",str(round(avg_funding)) + "Cr")

    with col4:
        st.metric("Funded Startups",num_startups)

    st.header("MOM graph")

    selected_option = st.selectbox("Select Type",["Toatal","Count"])
    if selected_option == "Total":
        temp_df = df.groupby(["year", "month"])["amount"].sum().reset_index()

    else:
        temp_df = df.groupby(["year", "month"])["amount"].count().reset_index()

    temp_df["x-axis"] = temp_df["month"].astype("str") + "-" + temp_df["year"].astype("str")

    fig5, ax5 = plt.subplots()
    ax5.bar(temp_df["x-axis"], temp_df["amount"])
    st.pyplot(fig5)

    #sector Analysis

    st.header("Sector Analysis")
    sector_analysis = df.groupby("vertical")["amount"].sum().reset_index()
    fig6, ax6 = plt.subplots()
    ax6.pie(sector_analysis["amount"], labels=sector_analysis["vertical"], autopct='%1.1f%%')
    ax6.set_title('Investment by Sector')
    st.pyplot(fig6)

    #types of funding



    st.header("Type of Funding")
    funding_type = df["round"].value_counts()
    fig7, ax7 = plt.subplots(figsize=(10, 6))  # plot ki size badhadi
    ax7.bar(funding_type.index, funding_type.values)
    ax7.set_title('Type of Funding')
    ax7.set_xlabel('Type of Funding')
    ax7.set_ylabel('Count')
    ax7.tick_params(axis='x', labelrotation=90)  # type of funding ki rotation badhadi
    st.pyplot(fig7)

    #city wise funding



    st.header("City-wise Funding")
    city_funding = df.groupby("city")["amount"].sum().reset_index()
    fig8, ax8 = plt.subplots(figsize=(12, 6))  # plot ki size badhadi
    ax8.bar(city_funding["city"], city_funding["amount"])
    ax8.set_title('City-wise Funding')
    ax8.set_xlabel('City')
    ax8.set_ylabel('Funding Amount')
    ax8.tick_params(axis='x', labelrotation=90)  # city names ki rotation badhadi
    st.pyplot(fig8)

    #top startup overall funding
    st.header("Top Startups Overall")
    top_startups = df.groupby("startup")["amount"].sum().reset_index()
    top_startups = top_startups.sort_values(by="amount", ascending=False).head(10)

    fig9, ax9 = plt.subplots(figsize=(10, 6))
    ax9.bar(top_startups["startup"], top_startups["amount"])
    ax9.set_title('Top Startups Overall')
    ax9.set_xlabel('Startup')
    ax9.set_ylabel('Funding Amount')
    ax9.tick_params(axis='x', labelrotation=90)
    st.pyplot(fig9)

    #top startup yearly
    st.header("Top Startups Yearly")
    top_startups_yearly = df.groupby(["year", "startup"])["amount"].sum().reset_index()
    top_startups_yearly = top_startups_yearly.sort_values(by=["year", "amount"], ascending=[True, False])

    fig10, ax10 = plt.subplots(figsize=(15, 8))
    for year in top_startups_yearly["year"].unique():
        year_data = top_startups_yearly[top_startups_yearly["year"] == year]
        ax10.plot(year_data["startup"], year_data["amount"], label=year)

    #top investors
    st.header("Top Investors")
    top_investors = df.groupby("investors")["amount"].sum().reset_index()
    top_investors = top_investors.sort_values(by="amount", ascending=False).head(10)

    fig11, ax11 = plt.subplots(figsize=(10, 6))
    ax11.bar(top_investors["investors"], top_investors["amount"])
    ax11.set_title('Top Investors')
    ax11.set_xlabel('Investors')
    ax11.set_ylabel('Funding Amount')
    ax11.tick_params(axis='x', labelrotation=90, labelsize=10)
    plt.tight_layout()
    st.pyplot(fig11)


    ax10.set_ylim(0, max(top_startups_yearly["amount"]) * 1.1)

    ax10.set_title('Top Startups Yearly')
    ax10.set_xlabel('Startup')
    ax10.set_ylabel('Funding Amount')
    ax10.legend()
    ax10.tick_params(axis='x', labelrotation=90, labelsize=10)
    plt.tight_layout()  # layout ko adjust kiya
    st.pyplot(fig10)

    #funding Heatmap
    st.header("Funding Heatmap")
    funding_pivot = df.pivot_table(index="vertical", columns="city", values="amount", aggfunc="sum")
    funding_heatmap = sns.heatmap(funding_pivot, annot=True, cmap="Blues", fmt=".2f", linewidths=0.5, linecolor="white")

    fig12 = funding_heatmap.get_figure()
    fig12.set_size_inches(12, 8)
    plt.rcParams.update({'font.size': 12})  # font size badhaya
    st.pyplot(fig12)

def load_startups_details(startup):
    st.title(startup)
    #load the recent five investors
    recent_startups = df.groupby("startup")["date"].max().sort_values(ascending=False).head(5)
    st.title("Recent Startups")
    st.dataframe(recent_startups)

    #founders
    st.subheader("Founders")
    founders_df = df["startup"].value_counts()
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(founders_df.index, founders_df.values, color='skyblue')
    ax.set_xlabel("Founders")
    ax.set_ylabel("Count")
    ax.set_title("Founders Distribution")
    ax.tick_params(axis='x', rotation=90)
    st.pyplot(fig)

    # Industry ko show karein
    st.subheader("Industry")
    industry_df = df["vertical"].value_counts()
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(industry_df.index, industry_df.values, color='skyblue')
    ax.set_xlabel("Industry")
    ax.set_ylabel("Count")
    ax.set_title("Industry Distribution")
    ax.tick_params(axis='x', rotation=90)
    st.pyplot(fig)

    # Subindustry ko show karein
    st.subheader("Subindustry")
    subindustry_df = df["subvertical"].value_counts()
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.pie(subindustry_df.values, labels=subindustry_df.index, autopct='%1.1f%%', textprops={'fontsize': 12})
    ax.set_title("Subindustry Distribution")
    st.pyplot(fig)

    #stages

    st.subheader("Stage")
    stage_df = df["amount"].value_counts()
    st.dataframe(stage_df)


    # # Investors ko pie chart mein show karein
    # st.subheader("Investors")
    # investors_df = df["investors"].value_counts()
    # fig, ax = plt.subplots()
    # ax.pie(investors_df.values, labels=investors_df.index, autopct='%1.1f%%')
    # ax.set_title("Investors Distribution")
    # st.pyplot(fig)

    # Investors ko bar chart mein show karein
    st.subheader("Investors Distribution")
    investors_df = df["investors"].value_counts()
    # fig, ax = plt.subplots(figsize=(10, 6))
    # ax.bar(investors_df.index, investors_df.values, color='skyblue')
    # ax.set_xlabel("Investors")
    # ax.set_ylabel("Count")
    # ax.set_title("Investors Distribution")
    # ax.tick_params(axis='x', rotation=90)
    # st.pyplot(fig)
    fig10, ax10 = plt.subplots()
    ax10.plot(investors_df.index, investors_df.values)
    st.pyplot(fig10)

    # Date-wise investment ko show karein
    st.subheader("Date-wise Investment")
    date_investment_df = df.groupby("date")["amount"].sum().reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(date_investment_df["date"], date_investment_df["amount"], marker='o')
    ax.set_xlabel("Date")
    ax.set_ylabel("Investment Amount")
    ax.set_title("Date-wise Investment")
    ax.tick_params(axis='x', rotation=90)
    st.pyplot(fig)






def load_investor_details(investor):
    st.title(investor)
    #load the recent five investors
    last5_df = df[df["investors"].str.contains(investor)].head()[["date", "startup", "vertical", "city", "round", "amount"]]
    st.subheader("Most Recent Investments")
    st.dataframe(last5_df)

    col1,col2 = st.columns(2)
    with col1:
        #biggest investments
        big_series = df[df["investors"].str.contains(investor)].groupby("startup")["amount"].sum().sort_values(ascending=False).head()
        st.subheader("Biggest Investment")
        fig, ax = plt.subplots()
        ax.bar(big_series.index,big_series.values)
        st.pyplot(fig)

    with col2:
        verical_series = df[df["investors"].str.contains(investor)].groupby("vertical")["amount"].sum()
        st.subheader("Sector Invested In")

        fig1, ax1 = plt.subplots()
        ax1.pie(verical_series,labels=verical_series.index)
        st.pyplot(fig1)

    col1,col2 = st.columns(2)

    with col1:
        stages_series = df[df["investors"].str.contains("IDG Ventures")].groupby("round")["amount"].sum()

        fig2, ax2 = plt.subplots()
        ax2.pie(stages_series, labels=stages_series.index)
        st.pyplot(fig2)

    with col2:
        city_series = df[df["investors"].str.contains(investor)].groupby("city")["amount"].sum()

        fig3, ax3 = plt.subplots()
        ax3.pie(city_series, labels=city_series.index)
        st.pyplot(fig3)

    df["year"] = df["date"].dt.year
    year_series = df[df["investors"].str.contains(investor)].groupby("year")["amount"].sum()
    st.subheader("YoY Investments")
    fig4, ax4 = plt.subplots()
    ax4.plot(year_series.index, year_series.values)
    st.pyplot(fig4)



st.sidebar.title("Startup Funding Alaysis")

option = st.sidebar.selectbox("select one",["Overall Analysis","Startup","Investors"])

if option == "Overall Analysis":

    load_overall_analysis()


# elif option == "Startup":
#     selected_startup = st.sidebar.selectbox("Select StartUp",sorted(df["startup"].unique().tolist()))
#     btn1 = st.sidebar.button("Find Startup Details")
#     if btn1:
#         load_startup_analysis(selected_startup)

elif option == "Startup":
    startup_name = st.sidebar.selectbox("Select StartUp", sorted(df["startup"].unique().tolist()))
    if st.sidebar.button("Find startup Details"):
        load_startups_details(startup_name)




else:
    selected_investor = st.sidebar.selectbox("Select StartUp",sorted(set(df["investors"].str.split(',').sum())))
    btn2 = st.sidebar.button("Find Investors Details")
    if btn2:
        load_investor_details(selected_investor)











