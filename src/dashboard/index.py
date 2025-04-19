import streamlit as st
import pandas as pd
import numpy as np

from functions import get_actual_month_total_value

st.title('Ant')

@st.cache_data
def load_data():
    import asyncio
    return asyncio.run(get_actual_month_total_value("expenses"))

metric1, metric2, metric3, metric4 = st.columns(4, gap="small",  vertical_alignment="top", border=True)

with metric1:
    st.metric('Remuneração Bruta', 3535.00, 1000)
    st.caption('(mensal)') 

with metric2:
    st.metric('Remuneração Líquida', 1500.35, 1000)
    st.caption('(mensal)') 

with metric3:
    st.metric('Benefícios', 1000.33, 1000)
    st.caption('(mensal)') 

with metric4:
    st.metric('Gastos Fixo', 159.99, 1000)
    st.caption('(mensal)')

st.divider()

type_filter = st.segmented_control('Select type', ['Expenses', 'Incomes'], default='Expenses')

chart_metric1, chart_metric2, chart_metric3, chart_metric4 = st.columns(4, gap="small")
with chart_metric1:
    st.metric('Ganhos Totais', 3535.00, 1000)
    st.caption('(mês atual)')

with chart_metric2:
    st.metric('Gastos Totais', load_data(), 1000)
    st.caption('(mês atual)')

