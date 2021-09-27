import streamlit as st
from multiapp import MultiApp
from apps import home, roc, ref_perc, det_perc, det_boxplot # import your app modules here


app = MultiApp()

st.markdown("""
# Juvenile Dashboards


""")

# Add all your application here
app.add_app("Home", home.app)
app.add_app("Referral Offense Correlation", roc.app)
app.add_app("Referral Offense % Change", ref_perc.app)
app.add_app("Detention % Change", det_perc.app)
app.add_app("Detention Boxplot per Year", det_boxplot.app)


# The main app
app.run()
