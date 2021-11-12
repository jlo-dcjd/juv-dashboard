import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as ex
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import datetime

monthsfy = ['Oct.', 'Nov.', 'Dec.', 'Jan.', 'Feb.', 'Mar.', 'Apr.', 'May', 'Jun.', 'Jul.', 'Aug.','Sep.']

prog_en = (('Cognitive Response Group', 0), ('DIVERSION MALE COURT', 9), ('Drug Court Diversion Program', 18),
 ('E.S.T.E.E.M. Court', 27),
 ('Electronic Monitoring Post Adjudication', 36),
 ('Electronic Monitoring Preadjudication Program', 45),
 ('Family Violence Intervention Program', 54),
 ('Functional Family Therapy', 63),
 ('M.Y. G.I.R.L.S - Mentor Services', 72),
 ('MENTAL HEALTH COURT', 81),
 ('Psych - Anger Management Group', 90),
 ('Psych - Sex Offender Group Stars', 99),
 ('Special Needs Unit/Program', 108),
 ('Texas Initiative Programs - Detention Alternative Program', 117),
 ('Texas Initiative Programs - Intensive Case Management', 126),
 ('Texas Initiative Programs - Mentor Services', 135),
 ('YAP - Family Preservation', 144),
 ('YAP Detention Alternative Program', 153),
 ('YAP Intensive Case Management', 162),
 ('Youth Conversion - Intensive Case Management', 171),
 ('Youthful Offenders Court', 180))

def percentage_change(col1,col2):
    return ((col2 - col1) / col1)

def get_unique_numbers(numbers):
    list_of_unique_numbers = []
    unique_numbers = set(numbers)
    for number in unique_numbers:
        list_of_unique_numbers.append(number)
    return sorted(list_of_unique_numbers)


def pro_chart_picker(op):
    fig = make_subplots(rows=2, cols=1, shared_yaxes=True)

    fig.add_trace(
        go.Scatter(x=monthsfy, y=program.iloc[:12, op], name='FY 2020'),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(x=monthsfy, y=program.iloc[12:24, op], name='FY 2021'),
        row=1, col=1
    )

    fig.add_trace(
        go.Bar(x=monthsfy, y=np.round(percentage_change(program.iloc[:12, prg_df_index].values, program.iloc[12:24, prg_df_index].values), 2), name='% Change 2020 vs 2021'),
        row=2, col=1
    )
    fig.update_layout(title_text="{} - Youth Served".format(option))
    return st.plotly_chart(fig)


def pro_chart_exits(op):
    fig = make_subplots(rows=3, cols=1, shared_yaxes=True, subplot_titles=("Total & Successful Exits", "Total Exits FY20 vs FY21", "Percent Change FY20 vs FY21"))

    fig.add_trace(
        go.Scatter(x=program.index, y=program.iloc[:, op], name='Total Exits'),
        row=1, col=1
    )

    fig.add_trace(
        go.Bar(x=program.index, y=program.iloc[:, op+1], name='Succ. Exits',  marker = {'color' : 'green'}),
        row=1, col=1
    )

    fig.add_trace(
        go.Bar(x=program.index, y=program.iloc[:, op + 2], name='Unsucc. Exits',  marker = {'color' : 'red'}),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(x=monthsfy, y=program.iloc[:12, op], name='FY 2020'),
        row=2, col=1
    )

    fig.add_trace(
        go.Scatter(x=monthsfy, y=program.iloc[12:24, op], name='FY 2021'),
        row=2, col=1
    )

    fig.add_trace(
        go.Bar(x=monthsfy, y=np.round(percentage_change(program.iloc[:12, prg_df_index_te].values, program.iloc[12:24, prg_df_index_te].values), 2), name='% Change 20 vs 21'),
        row=3, col=1
    )
    fig.update_layout(title_text="{} - Exits".format(option))
    return st.plotly_chart(fig)




def pro_chart_avg(op):
    fig = make_subplots(rows=2, cols=1, shared_yaxes=True)


    fig.add_trace(
        go.Bar(x=program.index, y=program.iloc[:, op], name='ADP'),
        row=1, col=1
    )

    fig.add_trace(
        go.Bar(x=program.index, y=program.iloc[:, op + 1], name='ALOS'),
        row=2, col=1
    )

    fig.update_layout(title_text="{} - ADP & ALOS".format(option))
    return st.plotly_chart(fig)


program = pd.read_csv('https://raw.githubusercontent.com/jlo-dcjd/juv-dashboard/main/apps/data/program_population.csv', index_col=0)
pg_list = get_unique_numbers([x.split(',')[0] for x in program.columns]) # program list


def app():
    st.title('Monthly Program Population')

    option = st.selectbox('Select program', pg_list)

    # column index: 9=youth served 9+2=t. exits
    prg_df_index = [y[0] for y in prog_en].index(option) * 9
    prg_df_index_te = [y[0] for y in prog_en].index(option) * 9 + 2
    prg_df_index_avg = [y[0] for y in prog_en].index(option) * 9 + 7

    # charts
    pro_chart_picker(prg_df_index)
    pro_chart_exits(prg_df_index_te)
    pro_chart_avg(prg_df_index_avg)

    # add table with program variables
    def pr_table(index):
        df_start = 0 + index
        df_end = 9 + index
        return program.iloc[:, df_start:df_end]

    st.dataframe(pr_table(prg_df_index))

    youth_served = program.iloc[:,::9]
    youth_served = youth_served.replace('-', np.nan)
    youth_served = youth_served.astype('int64')




    fig = ex.line(youth_served, x=youth_served.index,
                  y=youth_served.columns[:7], title='Monthly Program Population (FY2020 - 21)')

    st.plotly_chart(fig)
