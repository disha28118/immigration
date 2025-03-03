#streamlit run dashboard.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

#global variables
years=list(map(str,range(1980,2014)))

#loading data
@st.cache_data
def load_data():
    df=pd.read_excel('Canada.xlsx',sheet_name=1,skiprows=20,skipfooter=2)
    cols_to_rename={
    'OdName':'Country',
    'AreaName':"Continent",
    'REG':'Region',
    'DEV':'Status'
    }
    df=df.rename(columns=cols_to_rename)
    cols_to_drop=['AREA','Type','Coverage']
    df=df.drop(columns=cols_to_drop)
    df=df.set_index('Country')
    df.columns=[str(name).lower() for name in df.columns.tolist()]
    df['total']=df[years].sum(axis=1)
    df=df.sort_values(by='total',ascending=False)
    return df

#configure the layout
st.set_page_config(
    layout='wide',
    page_title='Immigration Data Analysis',
    page_icon='@',
)

#loading the data
with st.spinner('Loading data...'):
    df=load_data()
    st.sidebar.success('Data Loaded Successfully!!!')

#creating the ui interface
c1,c2,c3=st.columns([2,1,1])
c1.title('Immigration Analysis')
c2.header('Summary of Data')
total_rows=df.shape[0]
total_immig=df.total.sum()
max_immig=df.total.max()
max_immig_country=df.total.idxmax()
c2.metric('Total Countries',total_rows)
c2.metric('Total years',len(years))
c2.metric('Total immigration',f"{total_immig/1000000:.2f}M")
c2.metric('Maximum immigration',f"{max_immig/1000000:.2f}M",f"{max_immig_country}")

c3.header('Top 10 countries')
top_10=df.head(10)['total']
c3.dataframe(top_10,use_container_width=True)
fig=px.bar(top_10,x=top_10.index,y='total')
c3.plotly_chart(fig,use_container_width=True)
#country wise visualization
countries=df.index.tolist()
country=c1.selectbox('Select a country',countries)
immig=df.loc[country,years]
fig=px.line(immig,x=immig.index,y=immig.values,title='Immigration trend')
c1.plotly_chart(fig,use_container_width=True)
fig2=px.histogram(immig,x=immig.values,nbins=10,marginal='box')
c1.plotly_chart(fig2,use_container_width=True)
max_immig_for_country=immig.max()
max_year=immig.idxmax()
c2.metric(f'Max Immigration for {country}',f"{max_immig_for_country/1000:.2f}K",f"{max_year}")

st.header("Continent Wise Analysis")
c1,c2,c3=st.columns(3)
continents=df['continent'].unique().tolist()
cdf=df.groupby('continent')[years].sum()
cdf['total']=cdf.sum(axis=1)
c1.dataframe(cdf,use_container_width=True)
figContinent=px.bar(cdf,x=cdf.index,y='total',title='Continent Wise Immigration')
c2.plotly_chart(figContinent,use_container_width=True)
mapContinent=px.choropleth(df,locations=df.index,locationmode='country names',color='total',title='World map',width=1000,height=700,template='plotly_dark',)
c3.plotly_chart(mapContinent,use_container_width=True)