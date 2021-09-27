import streamlit as st
import pandas as pd 
import plotly.express as ex
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import datetime


def app():
    refs_2016 = pd.read_csv('https://raw.githubusercontent.com/jlo-dcjd/juv-dashboard/main/apps/data/Referrals_2016_2021.csv',
     index_col='Referral_Date')

    col_names = ['Pid', 'Sex', 'Race', 'Ref_Date', 'Paper_Date', 'Referral_Date', 'Stat', 'Category', 'Offense',
            'General_Category', 'OffenseDescription', 'Referral_Type']

    refs = pd.read_csv('https://raw.githubusercontent.com/jlo-dcjd/juv-dashboard/main/apps/data/Referrals%202010-2021.csv', names=col_names, skiprows=1)
    refs['Referral_Date'] = pd.to_datetime(refs['Referral_Date'])


    fig = ex.line(refs_2016, x=refs_2016.index, y=refs_2016.columns, title='Monthly Referrals 2016-2021')
    fig2 = ex.bar(refs['General_Category'].value_counts(), x=refs['General_Category'].value_counts().index, y=refs['General_Category'].value_counts().values, 
        title='Referral Offenses 2016-2021')


    st.plotly_chart(fig)
    st.plotly_chart(fig2)


