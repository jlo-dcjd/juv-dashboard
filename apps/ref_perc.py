import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as ex
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import datetime

months = ['Jan.', 'Feb.', 'Mar.', 'Apr.', 'May', 'Jun.', 'Jul.', 'Aug.', 'Sep.', 'Oct.', 'Nov.', 'Dec.']
monthsf = ['Oct.', 'Nov.', 'Dec.', 'Jan.', 'Feb.', 'Mar.', 'Apr.', 'May', 'Jun.', 'Jul.', 'Aug.', 'Sep.']
year_list = ['2018', '2019', '2020', '2021']

col_names = ['Pid', 'Sex', 'Race', 'Ref_Date', 'Paper_Date', 'Referral_Date', 'Stat', 'Category', 'Offense',
        'General_Category', 'OffenseDescription', 'Referral_Type']

refs = pd.read_csv('https://raw.githubusercontent.com/jlo-dcjd/juv-dashboard/main/apps/data/Referrals%202010-2021.csv', 
            names=col_names, skiprows=1, dtype='unicode')

refs['Referral_Date'] = pd.to_datetime(refs['Referral_Date'])

general_2010 = refs.groupby(pd.Grouper(key='Referral_Date', freq='M'))['General_Category'].value_counts().unstack().fillna(0)
general_2016 = general_2010.loc[datetime.date(year=2016,month=1,day=1): ].copy()
general_2016.drop(['Contempt'], axis=1, inplace=True) # remove other category

def percentage_change(col1,col2):
    return ((col2 - col1) / col1)
  
def ref_perc_df(change):
    df_perc = pd.DataFrame(index=list(range(1,13)))
    df_perc.index.names = ['Month']
    df_perc['2018'] = general_2016[change].iloc[24:36].values
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


def ref_perc_df_fy(change):
    df_perc = pd.DataFrame(index=list(range(1, 13)))
    df_perc.index.names = ['Month']
    df_perc['2018'] = general_2016[change].iloc[21:33].values
    df_perc['2019'] = general_2016[change].iloc[33:45].values
    df_perc['2020'] = general_2016[change].iloc[45:57].values

    c2021 = pd.Series(general_2016[change].iloc[57:69].values)
    c2021.index += 1
    df_perc['2021'] = c2021

    df_perc['pct_change_18vs20'] = percentage_change(df_perc['2018'], df_perc['2020'])
    df_perc['pct_change_19vs20'] = percentage_change(df_perc['2019'], df_perc['2020'])
    df_perc['pct_change_19vs21'] = percentage_change(df_perc['2019'], df_perc['2021'])
    df_perc['pct_change_20vs21'] = percentage_change(df_perc['2020'], df_perc['2021'])
    df_perc = df_perc.round(2)
    return df_perc


def app():
    st.title('Referral Offense % Change')


    change = st.selectbox('Select Offense', general_2016.columns) # select offense
    year1 = st.selectbox('Select Year 1', year_list, index=1)
    year2 = st.selectbox('Select Year 2', year_list, index=2)

    # ------------------ CY -------------------
    fig = make_subplots(rows=2, cols=1, shared_yaxes=True)
    fig.add_trace(
        go.Scatter(x=months, y=ref_perc_df(change)['2018'], name='2018'),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=months, y=ref_perc_df(change)['2019'], name='2019'),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=months, y=ref_perc_df(change)['2020'], name='2020'),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=months, y=ref_perc_df(change)['2021'], name='2021'),
        row=1, col=1
    )

    # Bar Chart
    fig.add_trace(
        go.Bar(x=months, y=percentage_change(ref_perc_df(change)[year1], ref_perc_df(change)[year2]), name='% Change {} vs {}'.format(year1, year2)),
        row=2, col=1
    )


    fig.update_layout(height=700, title_text="{} Referrals Since January 2018".format(change))
    fig.update_yaxes(tick0=0, dtick=25, row=1, col=1)

    fig.layout.yaxis2.tickformat='%'
    fig.update_yaxes(tick0=0, dtick=.15, row=2, col=1)
    # -----------------------------------------------------------------

    # ------------------ FY -------------------
    fig2 = make_subplots(rows=2, cols=1, shared_yaxes=True)
    fig2.add_trace(
        go.Scatter(x=monthsf, y=ref_perc_df_fy(change)['2018'], name='2018'),
        row=1, col=1
    )
    fig2.add_trace(
        go.Scatter(x=monthsf, y=ref_perc_df_fy(change)['2019'], name='2019'),
        row=1, col=1
    )
    fig2.add_trace(
        go.Scatter(x=monthsf, y=ref_perc_df_fy(change)['2020'], name='2020'),
        row=1, col=1
    )
    fig2.add_trace(
        go.Scatter(x=monthsf, y=ref_perc_df_fy(change)['2021'], name='2021'),
        row=1, col=1
    )

    fig2.add_trace(
        go.Bar(x=monthsf, y=percentage_change(ref_perc_df_fy(change)[year1], ref_perc_df_fy(change)[year2]),
               name='% Change {} vs {}'.format(year1, year2)),
        row=2, col=1
    )

    fig2.update_layout(height=700, title_text="{} Referrals Since October 2017".format(change))
    fig2.update_yaxes(tick0=0, dtick=25, row=1, col=1)

    fig2.layout.yaxis2.tickformat = '%'
    fig2.update_yaxes(tick0=0, dtick=.15, row=2, col=1)
    # ---------------------------------

    # Radio Button
    status = st.radio("Select Type: ", ('Calendar Year', 'Fiscal Year'))
    if (status == 'Calendar Year'):
        st.success("Calendar Year")
        st.plotly_chart(fig)
        st.subheader('{} Referrals'.format(change))
        st.dataframe(ref_perc_df(change))
    else:
        st.success("Fiscal Year")
        st.plotly_chart(fig2)
        st.subheader('{} Referrals'.format(change))
        st.dataframe(ref_perc_df_fy(change))

