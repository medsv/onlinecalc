import streamlit as st
import pandas as pd
def print_result(data):
    df = pd.DataFrame(data.items(), columns=['Параметр', 'Значение'])
    df['Значение'] = df['Значение'].apply(lambda x: str(x).replace('.', ','))
    st.dataframe(df, hide_index=True)    