import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Some Page Layout settings
st.set_page_config(layout='wide')

# Import Data
df = pd.read_csv('startup_funding.csv')

# Data Cleaning
df['Investors Name'] = df['Investors Name'].fillna("Undisclosed")

# Remove Remarks column
df.drop('Remarks',axis=1,inplace=True)

# Rename Columns
df.rename(columns={"InvestmentnType":"round", "City  Location":"city", "Startup Name":"startup",
                   "Date dd/mm/yyyy":"date", "Industry Vertical" : "vertical",
                   "Investors Name":"investors", "SubVertical" : "subvertical", "Amount in USD":"amount"},
          inplace=True)

# Set column Sr No as Index
df.set_index('Sr No', inplace=True)

# Fill Na with 0
df.amount.fillna('0',inplace=True)
df.amount = df.amount.str.replace(',','')
df.loc[df['amount'].isin(['unknown','undisclosed','Undisclosed']),'amount'] = '0'

# Take only those where amount column is digit as there are some '+' values coming
df = df[df.amount.str.isdigit()]
df.amount = df.amount.astype('float')

# Function to convert dollar to inr
def usd_to_inr(x):
    return round(x*(80)/(10000000),2)

df.amount = df.amount.apply(usd_to_inr)

# Convert date to date type
df.date.replace('05/072018','05/07/2018',inplace=True) # Some typo in date column
df.date = pd.to_datetime(df.date,errors='coerce') # Ignore those values that are not converting

# Remove null values based on few columns
df = df.dropna(subset=['date','startup','vertical','city','investors','round','amount'])

# Add year column
df['year'] = df.date.dt.year
df['month'] = df.date.dt.month

def load_investor_details(investor):
    st.title(investor)
    # Load recent 5 startup details by this investor
    st.subheader("Top 5 investments")
    last_5 = df[df['investors'].str.contains(selected_investor)][
                 ['date', 'startup', 'vertical', 'city', 'round', 'amount']].head(5)
    st.dataframe(last_5)

    # Biggest Investments
    st.subheader("Biggest Investments")
    big_5 = df[df['investors'].str.contains(selected_investor)].groupby('startup')['amount'].sum().sort_values(ascending = False).head()
    st.dataframe(big_5)

    # Plot Bar Chart
    col1, col2 = st.columns(2)
    with col1:
      fig, x = plt.subplots()
      x.bar( big_5.index, big_5.values)
      st.pyplot(fig)

    # Sector Pie Chart
    sector = df[df['investors'].str.contains(selected_investor)].groupby(['vertical'])['amount'].sum()
    with col2:
      st.subheader("Sectors Invested in")
      fig, x = plt.subplots()
      x.pie(sector.values, labels = sector.index, autopct='%1.1f%%')
      st.pyplot(fig)

    # Stage Pie Chart
    col3, col4 = st.columns(2)
    stage = df[df['investors'].str.contains(selected_investor)].groupby(['round'])['amount'].sum()
    with col3:
      st.subheader("Stages Invested in")
      fig, x = plt.subplots()
      x.pie(stage,labels= stage.index, autopct='%1.1f%%')
      st.pyplot(fig)

    # City
    city = df[df['investors'].str.contains(selected_investor)].groupby(['city'])['amount'].sum()
    with col4:
        st.subheader("City Invested in")
        fig, x = plt.subplots()
        x.pie(city, labels=city.index, autopct='%1.1f%%')
        st.pyplot(fig)

    # Investment year on year
    yoy_investment = df[df['investors'].str.contains(selected_investor)].groupby(['year'])['amount'].sum()
    st.subheader("Investment year on year Line Chart")
    fig, x = plt.subplots()
    #a.plot(yoy_investment.index, yoy_investment.values)
    st.line_chart(yoy_investment)
    #st.pyplot(fig)


# Overall Analysis Function:-
def load_overall_analysis():
    st.title("Overall Analysis")
    col1, col2, col3, col4 = st.columns(4)
    total = round(df['amount'].sum())
    with col1:
      st.metric("Total" ,str(total)+" Cr")

    max = round(df.groupby('startup')['amount'].max().sort_values(ascending=False)[0])
    with col2:
      st.metric("Maximum Amount Invested ", str(max) + " Cr")

    avg = round(df.groupby('startup')['amount'].sum().mean())
    with col3:
      st.metric("Average", str(avg) + " Cr")

    count = df['startup'].nunique()
    with col4:
        st.metric("Count", count)

    st.header('MOM Graph')
    selected_type = st.selectbox('Select Type',['Count','Amount'])
    if selected_type =='Count':
        temp_count = df.groupby(['year', 'month'])['startup'].count().reset_index()
        temp_count['x_axis'] = temp_count['year'].astype('str') + "_" + temp_count['month'].astype('str')
        fig, x = plt.subplots()
        x.plot(temp_count['x_axis'], temp_count['startup'])
    elif selected_type =='Amount':
        temp_amount = df.groupby(['year', 'month'])['amount'].sum().reset_index()
        temp_amount['x_axis'] = temp_amount['year'].astype('str') + "_" + temp_amount['month'].astype('str')
        fig, x = plt.subplots()
        x.plot(temp_amount['x_axis'], temp_amount['amount'])

    st.pyplot(fig)

# Add Sidebar
st.sidebar.title("Startup Funding Analysis")

option = st.sidebar.selectbox("Choose Type of Analysis", ['Overall', 'Investors', 'startups'])

if option == 'Overall':
    #btn0 = st.sidebar.button("Show Overall Analysis")
    #if btn0:
    load_overall_analysis()

elif option == 'startups':
    st.sidebar.selectbox("Choose Startup", sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button("Find StartUp Details")
    st.title("Startup Analysis")
elif option == 'Investors':
    selected_investor = st.sidebar.selectbox("Choose Investor", sorted(set(df['investors'].str.split(",").sum())))
    btn2 = st.sidebar.button("Find Investor Details")

    if btn2:
        load_investor_details(selected_investor)

