#from sklearn.utils import indices_to_mask
import streamlit as st
import pandas as pd 
import requests
import investpy as py
from bs4 import BeautifulSoup
import plotly.express as px

from _moving_average_convergence_divergence import MovingAverageConvergenceDivergence
from _relative_strength_index import RelativeStrengthIndex
from _bollinger_bands import BollingerBands



def ticker_2_CodeValeur(ticker):
  ticker_2_CodeValeur = {"ADH" : "9000" , "AFM" : "12200" , "AFI" : "11700" , "GAZ" : "7100" , "AGM" : "6700" , "ADI" : "11200" , "ALM" : "6600" , "ARD" : "27" , "ATL" : "10300" , "ATW" : "8200" , "ATH" : "3200" , "NEJ" : "7000" , "BAL" : "3300" , "BOA" : "1100" , "BCP" : "8000" , "BCI" : "5100" , "CRS" : "8900" , "CDM" : "3600" , "CDA" : "3900" , "CIH" : "3100" , "CMA" : "4000" , "CMT" : "11000" , "COL" : "9200" , "CSR" : "4100" , "CTM" : "2200" , "DRI" : "8500" , "DLM" : "10800" , "DHO" : "10900" , "DIS" : "4200" , "DWY" : "9700" , "NKL" : "11300" , "EQD" : "2300" , "FBR" : "9300" , "HPS" : "9600" , "IBC" : "7600" , "IMO" : "12" , "INV" : "9500" , "JET" : "11600" , "LBV" : "11100" , "LHM" : "3800" , "LES" : "4800" , "LYD" : "8600" , "M2M" : "10000" , "MOX" : "7200" , "MAB" : "1600" , "MNG" : "7300" , "MLE" : "2500" , "IAM" : "8001" , "MDP" : "6500" , "MIC" : "10600" , "MUT" : "21" , "NEX" : "7400" , "OUL" : "5200" , "PRO" : "9900" , "REB" : "5300" , "RDS" : "12000" , "RISMA" : "8700" , "S2M" : "11800" , "SAH" : "11400" , "SLF" : "10700" , "SAM" : "6800" , "SMI" : "1500" , "SNA" : "10500" , "SNP" : "9400" , "MSA" : "12300" , "SID" : "1300" , "SOT" : "9800" , "SRM" : "2000" , "SBM" : "10400" , "STR" : "11500" , "TQM" : "11900" , "TIM" : "10100" , "TMA" : "12100" , "UMR" : "7500" , "WAA" : "6400" , "ZDJ" : "5800"}
  return ticker_2_CodeValeur[ticker]


def get_image(ticker):                                                           
  url = "https://www.casablanca-bourse.com/bourseweb/Societe-Cote.aspx?codeValeur="+str(ticker_2_CodeValeur(ticker))+"&cat=7"
  req = requests.get(url)
  soup = BeautifulSoup(req.text, "html.parser")
  logo_path = soup.find("input", {"id": "SocieteCotee1_imgLogo"})['src']
  logo_url = 'https://www.casablanca-bourse.com/bourseweb/' + logo_path
  return logo_url

apptitle = 'Projet hiba'

st.set_page_config(page_title=apptitle, page_icon=":chart_with_upwards_trend:")

# Title the app
st.title('Titre')

# @st.cache(ttl=3600, max_entries=10)   #-- Magic command to cache data

# @st.cache(ttl=3600, max_entries=10)   #-- Magic command to cache data


st.sidebar.markdown('<center><img src="https://www.lamarocainevie.com/bo/sites/default/files/2019-02/logo.png" width="300"  height="100" alt="Marocaine vie "></center>', unsafe_allow_html=True)

st.sidebar.markdown("## Selectioner le titre et la periode ")
st.markdown('Travail realisé par: ....')
st.markdown("Sous l'encadrement de Pr...")
st.markdown('__________________________________________________________')


dropdown = st.sidebar.selectbox("Choisir une action", pd.concat([pd.Series(["MASI"]), py.get_stocks(country='morocco').name]))
indicateur = st.sidebar.selectbox("Choisir un indicateur", ['MACD','RSI', 'BB'])


start = st.sidebar.date_input('Debut', value =pd.to_datetime('01-01-2020'))
end = st.sidebar.date_input('Fin', value = pd.to_datetime('today'))

start = start.strftime('%d/%m/%Y')
end = end.strftime('%d/%m/%Y')

stocks = py.get_stocks(country='morocco')
stocks.set_index("name", inplace = True)


if dropdown != "MASI":
  ticker =  stocks.loc[dropdown,'symbol']
  df=py.get_stock_historical_data(stock=ticker, country='morocco', from_date=start, to_date=end)
  url = get_image(ticker)
  url = str(url)
else :
  df=py.get_index_historical_data(index='Moroccan All Shares', country='morocco', from_date=start, to_date=end)
  df.Volume = df.Close*10000 
  url = "https://static.lematin.ma/cdn/images/icobourse/indices/masi.png"






st.markdown('<center><img src="'+url+'" alt="stock logo"></center>', unsafe_allow_html=True) # logo de l'action
st.markdown('__________________________________________________________')
if indicateur == 'MACD':
  c1, c2 = st.columns(2)
  with c1:
      ws = st.number_input('Ws', 9)
  with c2:
      wl = st.number_input('Wl', 26)

  macd = MovingAverageConvergenceDivergence(df)
  calcul_macd = macd._calculateTi(wl=wl,ws=ws)
  df['macd'] = calcul_macd.macd
  df['signal line'] = calcul_macd.signal_line
  data = [df['close'], df['macd'], df['signal line']]
  headers = ["close", "macd", 'signal line']
  
elif indicateur == 'RSI':
    rsi=RelativeStrengthIndex(df)
    period = st.number_input('Period', 9)
    calcul_rsi = rsi._calculateTi(period=period)
    df['rsi'] = calcul_rsi.rsi
    data = [df['close'], df['rsi']]
    headers = ["close", "rsi"]

elif indicateur == 'BB':
    BB=BollingerBands(df)
    c1, c2 = st.columns(2)
    with c1:
        period = st.number_input('Period', 12)
    with c2:
        std_nbr = st.number_input('Std Number', 4)
    calcul_bb = BB._calculateTi(period=period,std_number=std_nbr)
    df['middle_band'] = calcul_bb.middle_band	
    df['upper_band'] = calcul_bb.upper_band
    df['lower_band'] = calcul_bb.lower_band
    data = [df['middle_band'], df['upper_band'], df['lower_band']]
    headers = ["close", "middle_band", "upper_band", "lower_band"]



st.markdown('__________________________________________________________')
df3 = pd.concat(data, axis=1, keys=headers)
fig = px.line(df3)
st.plotly_chart(fig, use_container_width=False, sharing="streamlit")

