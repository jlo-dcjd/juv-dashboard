import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as ex
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import datetime

# CY 18 - Jan 2018 - Dec 2018
# FY 18 - Oct 2017 - Sep 2018

months = ['Jan.', 'Feb.', 'Mar.', 'Apr.','May', 'Jun.', 'Jul.', 'Aug.', 'Sep.', 'Oct.', 'Nov.', 'Dec.']
monthsf = ['Oct.', 'Nov.', 'Dec.', 'Jan.', 'Feb.', 'Mar.', 'Apr.', 'May', 'Jun.', 'Jul.', 'Aug.', 'Sep.']
year_list = ['2018', '2019', '2020', '2021']

detentions = pd.read_csv(r'C:\Users\Juan.Lomeli\OneDrive - Dallas County\Documents\streamlit-app\multipage-app\apps\data\detentions_2016_2021.csv', index_col='Date')
detentions = detentions.round(2)

def percentage_change(col1,col2):
    return ((col2 - col1) / col1)

def det_perc_df(change):
    df_perc = pd.DataFrame(index=list(range(1,13)))
    df_perc.index.names = ['Month']
    df_perc['2018'] = detentions[change].iloc[36:48].values
    df_perc['2019'] = detentions[change].iloc[48:60].values
    df_perc['2020'] = detentions[change].iloc[60:72].values

    c2021 = pd.Series(detentions[change].iloc[72:84].values)
    c2021.index += 1 
    df_perc['2021'] = c2021
    
    df_perc['pct_change_18vs20'] = percentage_change(df_perc['2018'], df_perc['2020'])    
    df_perc['pct_change_19vs20'] = percentage_change(df_perc['2019'], df_perc['2020'])
    df_perc['pct_change_19vs21'] = percentage_change(df_perc['2019'], df_perc['2021'])
    df_perc['pct_change_20vs21'] = percentage_change(df_perc['2020'], df_perc['2021'])
    df_perc = df_perc.round(2)
    return df_perc

def det_perc_df_fy(change):
    df_perc = pd.DataFrame(index=list(range(1,13)))
    df_perc.index.names = ['Month']
    df_perc['2018'] = detentions[change].iloc[33:45].values
    df_perc['2019'] = detentions[change].iloc[45:57].values
    df_perc['2020'] = detentions[change].iloc[57:69].values

    c2021 = pd.Series(detentions[change].iloc[69:81].values)
    c2021.index += 1 
    df_perc['2021'] = c2021
    
    df_perc['pct_change_18vs20'] = percentage_change(df_perc['2018'], df_perc['2020'])    
    df_perc['pct_change_19vs20'] = percentage_change(df_perc['2019'], df_perc['2020'])
    df_perc['pct_change_19vs21'] = percentage_change(df_perc['2019'], df_perc['2021'])
    df_perc['pct_change_20vs21'] = percentage_change(df_perc['2020'], df_perc['2021'])
    df_perc = df_perc.round(2)
    return df_perc

def app():
    st.title('Detention % Change')

    change = st.selectbox('Select Detention Metric', detentions.columns) # select offense
    year1 = st.selectbox('Select Year 1', year_list, index=1) 
    year2 = st.selectbox('Select Year 2', year_list, index=2) 
    # ------------------ CY -------------------
    fig = make_subplots(rows=2, cols=1, shared_yaxes=True)
    fig.add_trace(
        go.Scatter(x=months, y=det_perc_df(change)['2018'], name='{} 2018'.format(change)),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=months, y=det_perc_df(change)['2019'], name='{} 2019'.format(change)),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=months, y=det_perc_df(change)['2020'], name='{} 2020'.format(change)),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=months, y=det_perc_df(change)['2021'], name='{} 2021'.format(change)),
        row=1, col=1
    )


    fig.add_trace(
        go.Bar(x=months, y=percentage_change(det_perc_df(change)[year1], det_perc_df(change)[year2]), name='% Change {} vs {}'.format(year1, year2)),
        row=2, col=1
    )
    # fig.add_trace(
    #     go.Bar(x=months, y=det_perc_df(change)['pct_change_19vs20'], name='% Change 2019 vs 2020'),
    #     row=3, col=1
    # )
    # fig.add_trace(
    #     go.Bar(x=months, y=det_perc_df(change)['pct_change_19vs21'], name='% Change 2019 vs 2021'),
    #     row=4, col=1
    # )
    # fig.add_trace(
    #     go.Bar(x=months, y=det_perc_df(change)['pct_change_20vs21'], name='% Change 2020 vs 2021'),
    #     row=5, col=1
    # )

    fig.update_layout(height=700, title_text="Detention {} Since Jan. 2018".format(change))
    fig.update_yaxes(tick0=0, dtick=30, row=1, col=1)

    fig.layout.yaxis2.tickformat='%'
    fig.update_yaxes(tick0=0, dtick=.10, row=2, col=1)

    # fig.layout.yaxis3.tickformat='%'
    # fig.update_yaxes(tick0=0, dtick=.25, row=3, col=1)

    # fig.layout.yaxis4.tickformat='%'
    # fig.update_yaxes(tick0=0, dtick=.25, row=4, col=1)


    # ------------------ FY -------------------
    fig2 = make_subplots(rows=2, cols=1, shared_yaxes=True)
    fig2.add_trace(
        go.Scatter(x=monthsf, y=det_perc_df_fy(change)['2018'], name='{} 2018'.format(change)),
        row=1, col=1
    )
    fig2.add_trace(
        go.Scatter(x=monthsf, y=det_perc_df_fy(change)['2019'], name='{} 2019'.format(change)),
        row=1, col=1
    )
    fig2.add_trace(
        go.Scatter(x=monthsf, y=det_perc_df_fy(change)['2020'], name='{} 2020'.format(change)),
        row=1, col=1
    )
    fig2.add_trace(
        go.Scatter(x=monthsf, y=det_perc_df_fy(change)['2021'], name='{} 2021'.format(change)),
        row=1, col=1
    )


    fig2.add_trace(
        go.Bar(x=monthsf, y=percentage_change(det_perc_df_fy(change)[year1], det_perc_df_fy(change)[year2]), name='% Change {} vs {}'.format(year1, year2)),
        row=2, col=1
    )
    # fig2.add_trace(
    #     go.Bar(x=monthsf, y=det_perc_df_fy(change)['pct_change_19vs20'], name='% Change 2019 vs 2020'),
    #     row=3, col=1
    # )
    # fig2.add_trace(
    #     go.Bar(x=monthsf, y=det_perc_df_fy(change)['pct_change_19vs21'], name='% Change 2019 vs 2021'),
    #     row=4, col=1
    # )
    # fig2.add_trace(
    #     go.Bar(x=monthsf, y=det_perc_df_fy(change)['pct_change_20vs21'], name='% Change 2020 vs 2021'),
    #     row=5, col=1
    # )

    fig2.update_layout(height=700, title_text="Detention {} Since Oct. 2017".format(change))
    fig2.update_yaxes(tick0=0, dtick=30, row=1, col=1)

    fig2.layout.yaxis2.tickformat='%'
    fig2.update_yaxes(tick0=0, dtick=.10, row=2, col=1)

    # fig2.layout.yaxis3.tickformat='%'
    # fig2.update_yaxes(tick0=0, dtick=.25, row=3, col=1)

    # fig2.layout.yaxis4.tickformat='%'
    # fig2.update_yaxes(tick0=0, dtick=.25, row=4, col=1)

    # Radio Button
    status = st.radio("Select Type: ", ('Calendar Year', 'Fiscal Year'))
    if (status == 'Calendar Year'):
        st.success("Calendar Year")
        st.plotly_chart(fig)
        st.subheader('{} Detention'.format(change))
        st.dataframe(det_perc_df(change))
    else:
        st.success("Fiscal Year")
        st.plotly_chart(fig2)
        st.subheader('{} Referrals'.format(change))
        st.dataframe(det_perc_df_fy(change))



