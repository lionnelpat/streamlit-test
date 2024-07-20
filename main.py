import  streamlit as st
import pandas as pd
import plotly.express as px
import plotly.subplots as sp
from streamlit_option_menu import option_menu
from streamlit_extras.metric_cards import style_metric_cards

#set page
st.set_page_config(page_title="CESAG Business Analytics Dashboard", page_icon="🌎", layout="wide")
st.subheader("📈 Business Analytics Dashboard ")

#get data from mysql
df=pd.read_csv('data/customers.csv')

department=st.sidebar.multiselect(
    "Filter Department",
     options=df["Department"].unique(),
     default=df["Department"].unique(),
)

country=st.sidebar.multiselect(
    "Filter Country",
     options=df["Country"].unique(),
     default=df["Country"].unique(),
)

businessunit=st.sidebar.multiselect(
    "Filter Business",
     options=df["BusinessUnit"].unique(),
     default=df["BusinessUnit"].unique(),
)

df_selection=df.query(
    "Department==@department & Country==@country & BusinessUnit ==@businessunit"
)

#create divs
div1, div2=st.columns(2)


#mysql table
def table():
  with st.expander("Tabular"):
  #st.dataframe(df_selection,use_container_width=True)
   shwdata = st.multiselect('Filter :', df.columns, default=["EEID","FullName","JobTitle","Department","BusinessUnit","Gender","Ethnicity","Age","HireDate","AnnualSalary","Bonus","Country","City","id"])
   st.dataframe(df_selection[shwdata],use_container_width=True)

#bar chart
def barchart():
  theme_plotly = None # None or streamlit
  with div2:
    fig = px.bar(df_selection, y='AnnualSalary', x='Department', text_auto='.2s',title="Controlled text sizes, positions and angles")
    fig.update_traces(textfont_size=18, textangle=0, textposition="outside", cliponaxis=False)
    st.plotly_chart(fig, use_container_width=True, theme="streamlit")

def pie():
 with div1:
  theme_plotly = None # None or streamlit
  fig = px.pie(df_selection, values='AnnualSalary', names='Department', title='Customers by Country')
  fig.update_layout(legend_title="Country", legend_y=0.9)
  fig.update_traces(textinfo='percent+label', textposition='inside')
  st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

#top analytics
def metrics():

    col1, col2, col3 = st.columns(3)

    col1.metric(label="Total Customers", value=df_selection.Gender.count(), delta="All customers")

    col2.metric(label="Total Annual Salary", value= f"{df_selection.AnnualSalary.sum():,.0f}",delta=df.AnnualSalary.median())

    col3.metric(label="Annual Salary", value= f"{ df_selection.AnnualSalary.max()-df.AnnualSalary.min():,.0f}",delta="Annual Salary Range")

    style_metric_cards(background_color="#121270",border_left_color="#f20045",box_shadow="3px")

#option menu

with st.sidebar:
        selected=option_menu(
        menu_title="Main Menu",
         #menu_title=None,
        options=["Home","Table"],
        icons=["house","book"],
        menu_icon="cast", #option
        default_index=0, #option
        orientation="vertical",



        )


if selected=="Home":
    metrics()
    table()

if selected=="Table":
    st.write("Welcome to Business Analytics Dashboard")
    pie()
    barchart()


