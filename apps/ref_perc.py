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

col_names = ['Pid', 'Sex', 'Race', 'Ref_Date', 'Paper_Date', 'Referral_Date', 'Stat', 'Category', 'Offense',
        'General_Category', 'OffenseDescription', 'Referral_Type']

refs = pd.read_csv('https://raw.githubusercontent.com/jlo-dcjd/juv-dashboard/main/apps/data/Referrals%202010-2021.csv', 
            names=col_names, skiprows=1)

refs['Referral_Date'] = pd.to_datetime(refs['Referral_Date'])

general_2010 = refs.groupby(pd.Grouper(key='Referral_Date', freq='M'))['General_Category'].value_counts().unstack().fillna(0)
general_2016 = general_2010.loc[datetime.date(year=2016,month=1,day=1): ].copy()
general_2016.drop(['Contempt'], axis=1, inplace=True) # remove other category

def percentage_change(col1,col2):
    return ((col2 - col1) / col1)

def ref_perc_df(change):
    df_perc = pd.DataFrame(index=list(range(1,13)))
    df_perc.index.names = ['Month']
    df_perc['2019'] = general_2016[change].iloc[36:48].values
    df_perc['2020'] = general_2016[change].iloc[48:60].values

    c2021 = pd.Series(general_2016[change].iloc[60:72].values)
    c2021.index += 1 
    df_perc['2021'] = c2021

    df_perc['pct_change_19vs20'] = percentage_change(df_perc['2019'], df_perc['2020'])
    df_perc['pct_change_19vs21'] = percentage_change(df_perc['2019'], df_perc['2021'])
    df_perc['pct_change_20vs21'] = percentage_change(df_perc['2020'], df_perc['2021'])
    df_perc = df_perc.round(2)
    return df_perc


def app():
    st.title('Referral Offense % Change')



    change = st.selectbox('Select Offense', general_2016.columns) # select offense

    fig = make_subplots(rows=4, cols=1, shared_yaxes=True)

    fig.add_trace(
        go.Scatter(x=months, y=ref_perc_df(change)['2019'], name='{} Referrals 2019'.format(change)),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=months, y=ref_perc_df(change)['2020'], name='{} Referrals 2020'.format(change)),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=months, y=ref_perc_df(change)['2021'], name='{} Referrals 2021'.format(change)),
        row=1, col=1
    )


    fig.add_trace(
        go.Bar(x=months, y=ref_perc_df(change)['pct_change_19vs20'], name='% Change 2019 vs 2020'),
        row=2, col=1
    )

    fig.add_trace(
        go.Bar(x=months, y=ref_perc_df(change)['pct_change_19vs21'], name='% Change 2019 vs 2021'),
        row=3, col=1
    )

    fig.add_trace(
        go.Bar(x=months, y=ref_perc_df(change)['pct_change_20vs21'], name='% Change 2020 vs 2021'),
        row=4, col=1
    )

    fig.update_layout( title_text="Monthly {} Referrals Since Jan. 2019".format(change))
    fig.update_yaxes(tick0=0, row=1, col=1, dtick=20)

    fig.layout.yaxis2.tickformat='%'
    fig.update_yaxes(tick0=0, dtick=.2, row=2, col=1)

    fig.layout.yaxis3.tickformat='%'
    fig.update_yaxes(tick0=0, dtick=.2, row=3, col=1)

    fig.layout.yaxis4.tickformat='%'

    st.plotly_chart(fig)

    # ------------------------------------
    st.subheader('{} Referrals'.format(change))
    st.dataframe(ref_perc_df(change))

