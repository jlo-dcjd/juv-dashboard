import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as ex
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import datetime

months = ['Jan.', 'Feb.', 'Mar.', 'Apr.',
               'May', 'Jun.', 'Jul.', 'Aug.',
               'Sep.', 'Oct.', 'Nov.', 'Dec.']

detentions = pd.read_csv('https://raw.githubusercontent.com/jlo-dcjd/juv-dashboard/main/apps/data/detentions_2016_2021.csv', index_col='Referral_Date')
detentions = detentions.round(2)

def det_df(change):
    df_perc = pd.DataFrame(index=list(range(1,13)))
    df_perc.index.names = ['Month']
    df_perc['2016'] = detentions[change].iloc[:12].values
    df_perc['2017'] = detentions[change].iloc[12:24].values
    df_perc['2018'] = detentions[change].iloc[24:36].values
    df_perc['2019'] = detentions[change].iloc[36:48].values
    df_perc['2020'] = detentions[change].iloc[48:60].values

    c2021 = pd.Series(detentions[change].iloc[60:].values)
    c2021.index += 1 
    df_perc['2021'] = c2021


    df_perc = df_perc.round(2)
    return df_perc

def app():
    st.title('Detention Boxplot per Year')
    change = st.selectbox('Select Detention Metric', detentions.columns) # select offense


    fig = go.Figure()

    fig.add_trace(go.Box(y=detentions[change][:12], name='2016', boxmean=True))
    fig.add_trace(go.Box(y=detentions[change][12:24], name='2017', boxmean=True))
    fig.add_trace(go.Box(y=detentions[change][24:36], name='2018', boxmean=True))
    fig.add_trace(go.Box(y=detentions[change][36:48], name='2019', boxmean=True))
    fig.add_trace(go.Box(y=detentions[change][48:60], name='2020', boxmean=True))
    fig.add_trace(go.Box(y=detentions[change][60:], name='2021', boxmean=True))


    fig.update_layout(title='{} - Boxplot Per Year'.format(change))

    st.plotly_chart(fig)

    st.subheader('{} Detention'.format(change))
    st.dataframe(det_df(change))
