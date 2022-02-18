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

    refs = pd.read_csv('https://raw.githubusercontent.com/jlo-dcjd/juv-dashboard/main/apps/data/Referrals%202010-2021.csv', dtype='unicode', names=col_names, skiprows=1)
    refs['Referral_Date'] = pd.to_datetime(refs['Referral_Date'])
    
    general_2010 = refs.groupby(pd.Grouper(key='Referral_Date', freq='M'))['General_Category'].value_counts().unstack().fillna(0)
    general_2016 = general_2010.loc[datetime.date(year=2016,month=1,day=1): ].copy()
    general_2016.drop(['Contempt'], axis=1, inplace=True) # remove other category


    fig = ex.line(refs_2016, x=refs_2016.index, y=refs_2016.columns, title='Monthly Referrals 2016-2022')
    fig2 = ex.bar(refs['General_Category'].value_counts(), x=refs['General_Category'].value_counts().index, y=refs['General_Category'].value_counts().values, 
        title='Referral Offenses 2016-2021')
    
    fig3 = ex.line(general_2016, x=general_2016.index, y=general_2016.columns, title='Referral Offenses 2016-2022')


    st.plotly_chart(fig)
    st.plotly_chart(fig3)
    st.plotly_chart(fig2)


