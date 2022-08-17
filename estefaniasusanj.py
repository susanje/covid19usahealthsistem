import pandas as pd
import re
import streamlit as st
import datetime as dt
import plotly.figure_factory as ff
import plotly.graph_objects as go
import plotly.express as px
import chart_studio.plotly as py 
import plotly.offline as po 
import plotly.graph_objs as pg 



df1= pd.read_csv('C:/Users/User/Downloads/COVID-19_Reported_Patient_Impact_and_Hospital_Capacity_by_State_Timeseries.csv', sep= ',')
#Titulo
st.header("COVID-19-USA")
#subtitulo
st.subheader("Top 10 mayor ocupaciòn hospitalaria")
#Ordeno el dataframe por fecha
df1.sort_values(by='date', ascending=True)
#Borro columnas innecesarias
df1.drop(df1.filter(regex= 'coverage|numerator|denominator|suspected|reported').columns, axis= 1, inplace= True)
#Uso de cama por Estados
#Traigo las columnas de mi interes
respuesta_1= df1[['state','date','inpatient_beds_used_covid', 'total_adult_patients_hospitalized_confirmed_covid','total_pediatric_patients_hospitalized_confirmed_covid']]
#Paso a date la fecha y hago una columna mes
respuesta_1["date"]= pd.to_datetime(respuesta_1['date'])
respuesta_1["Month"]= respuesta_1['date'].dt.month 
respuesta_1["Year"]= respuesta_1['date'].dt.year
# Filtro info entre dos fechas 
respuesta_1= respuesta_1.loc[(respuesta_1['date']>= '2020-01-01')&(respuesta_1['date']<='2021-12-31')]  
#Hago limpieza y normalizacion de los datos
respuesta_1.dropna()

respuesta_1['total_adult_patients_hospitalized_confirmed_covid'] = respuesta_1['total_adult_patients_hospitalized_confirmed_covid'].astype(float, errors= 'raise')
respuesta_1['total_pediatric_patients_hospitalized_confirmed_covid'] = respuesta_1['total_pediatric_patients_hospitalized_confirmed_covid'].astype(float, errors= 'raise')
respuesta_1['total_adult_patients_hospitalized_confirmed_covid'] = respuesta_1['total_adult_patients_hospitalized_confirmed_covid'].fillna(0)
respuesta_1['total_pediatric_patients_hospitalized_confirmed_covid'] = respuesta_1['total_pediatric_patients_hospitalized_confirmed_covid'].fillna(0)
#Sumo las dos columnas de mi interes
respuesta_1['Total_camas_covid']=round((respuesta_1['total_pediatric_patients_hospitalized_confirmed_covid']+respuesta_1['total_adult_patients_hospitalized_confirmed_covid']),2)
#Hago un Groupby por estado sumando la columna 'Total_beds' 
MaxEstado= respuesta_1.groupby("state")['Total_camas_covid'].sum()
MaxEstado=(MaxEstado.to_frame())
#Ordeno por maximos
MaxEstado= MaxEstado.sort_values(by='Total_camas_covid',ascending=False).head(10)
#Paso esto en streamlilt
st.table(MaxEstado.style.highlight_max(axis=0))
#Grafico esto en streamlilt

fig = px.bar(        
        df1,
        x = respuesta_1['state'],
        y = respuesta_1['Total_camas_covid'],
        title = "Uso de camas Covid por Estado ",
        color=respuesta_1['state'],
         opacity = 0.8
             )
st.plotly_chart(fig)  
#Subtitulo
st.subheader("Ocupacion camas terapia Covid filtrado por Estado")
#Cantidad de camas UCI por estado
respuesta_3= df1[['state','date','staffed_icu_adult_patients_confirmed_covid', 'staffed_icu_pediatric_patients_confirmed_covid']]
#Corto entre dos fechas
respuesta_3.sort_values(by='date', ascending=True)
#Normalizo y hago limpieza
respuesta_3['staffed_icu_adult_patients_confirmed_covid'] = respuesta_3['staffed_icu_adult_patients_confirmed_covid'].astype(float, errors= 'raise')
respuesta_3['staffed_icu_pediatric_patients_confirmed_covid'] = respuesta_3['staffed_icu_pediatric_patients_confirmed_covid'].astype(float, errors= 'raise')
respuesta_3['staffed_icu_adult_patients_confirmed_covid'] = respuesta_3['staffed_icu_adult_patients_confirmed_covid'].fillna(0)
respuesta_3['staffed_icu_pediatric_patients_confirmed_covid'] = respuesta_3['staffed_icu_pediatric_patients_confirmed_covid'].fillna(0)
respuesta_3.dropna()
#Sumo camas pediatricas y adultos 
respuesta_3['Total_camas_icu']=round((pd.Series(respuesta_3['staffed_icu_pediatric_patients_confirmed_covid']+respuesta_3['staffed_icu_adult_patients_confirmed_covid'])),2)
#Hago un agrupamiento por Estado sumando Total_camas_uci
Max_Estado= respuesta_3.groupby("state")['Total_camas_icu'].sum()
Max_Estado=(Max_Estado.to_frame())
Max_Estado= Max_Estado.sort_values(by='Total_camas_icu',ascending=False).head(40)
#Grafico esto en streamlilt
st.table(Max_Estado)
#Grafico esto en streamlilt

fig1 = px.bar(        
        df1,
        x = respuesta_3['state'],
        y = respuesta_3['Total_camas_icu'],
        title = "Cantidad de Camas terapia por Estado",
        color=respuesta_3['state'],
        opacity = 0.5  ,
    )
  
st.plotly_chart(fig1) 
#Subtitulo
st.subheader("Cantidad de camas ocupadas por Covid durante la pandemia(sospechosos y confirmados)")
#Ordeno por fecha
respuesta_1.sort_values(by='date', ascending=True)
#Normalizo y limpio la columna a usar

Max_Fecha= respuesta_1.groupby("date")['Total_camas_covid'].sum()
Max_Fecha=(Max_Fecha.to_frame())
Max_Fecha= (Max_Fecha.sort_values(by='Total_camas_covid',ascending=False)).head(30)

#Grafico esto en streamlilt
st.table(Max_Fecha)
#Grafico esto en streamlilt

fig2 = px.bar(        
        df1,
        x = respuesta_1['date'],
        y = respuesta_1['Total_camas_covid'],
        title = "Ocupacion hospitalaria Covid por Fecha",
        
    )
st.plotly_chart(fig2)
#Normalizo y limpio la columna a usar


Max_Fecha1= respuesta_1.groupby("state")['Total_camas_covid'].sum()
Max_Fecha1=(Max_Fecha1.to_frame())
Max_Fecha1= Max_Fecha1.sort_values(by='Total_camas_covid',ascending=False)
#Grafico esto en streamlilt
st.table(Max_Fecha1)
#Grafico mapa esto en streamlilt
df= pd.read_csv('C:/Users/User/Downloads/COVID-19_Reported_Patient_Impact_and_Hospital_Capacity_by_State_Timeseries.csv', sep= ',')

df['new_date'] = pd.to_datetime(df['date'])
df['Year-Week'] = df['new_date'].dt.strftime('%Y-%U')
df = df.sort_values(by=['state', 'new_date'])
df_week = df.groupby(['state', 'Year-Week']).first().reset_index()
us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}
df_week['state_code'] = df_week['state'].map(us_state_abbrev)
df_week = df_week.sort_values(by=['Year-Week'])
fig3 = px.choropleth(df_week, locations='state', color='total_adult_patients_hospitalized_confirmed_covid',
                           color_continuous_scale=px.colors.sequential.OrRd,
                           hover_name = 'state',
                           locationmode = 'USA-states',
                           animation_frame="Year-Week",
                          )
fig3.update_layout(
    title_text = 'Semanas hospitalizacion adultos USA ', 
    geo_scope='usa',  
)
fig3.show()
st.plotly_chart(fig3)
df_week = df_week.sort_values(by=['Year-Week'])
fig4 = px.choropleth(df_week, locations='state', color='total_pediatric_patients_hospitalized_confirmed_covid',
                           color_continuous_scale=px.colors.sequential.OrRd,
                           hover_name = 'state',
                           locationmode = 'USA-states',
                           animation_frame="Year-Week",
                          )
fig4.update_layout(
    title_text = 'Semanas hospitalizacion niños USA ', 
    geo_scope='usa',  
)
fig4.show()
st.plotly_chart(fig4)




