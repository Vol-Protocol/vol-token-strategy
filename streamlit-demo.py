
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_option('deprecation.showPyplotGlobalUse', False)
st.title('Vol Protocol Use Case Study')
st.write('Use of ETHVOL30 as % of portfolio and buying the improve LP returns in UNISWAPV2 WETH-DAI POOL')
st.write("ETHVOL30 token can significantly improve portfolio returns by hedging vol exposure ")
percentInV = st.sidebar.slider('Percent Portfolio in Volility Token', 0, 100, 20)
st.write(percentInV, '% Portfolio in ETHVOL30 and rest of the ',100-percentInV,'% in ETH vs 100% in ETHVOL30/ETH' )

df = pd.read_csv('eth-usd-price-with-volitility.csv')

initialEqity = 100

# percentInV = 20
percentInEth = 100 - percentInV

# print(df) 

timeStart = 1609545600
df = df[df['time'] >= timeStart]


# st.sidebar()

timeEnd = 1621468800
df = df[df['time'] <= timeEnd]
df.reset_index(inplace = True)


df['portfolio_ETH'] = df['close']/(df['close'][0]/initialEqity)

df['portfolio_HV'] = df['HV']/(df['HV'][0]/initialEqity)

df['eth_value'] = df['close']/(df['close'][0]/(percentInEth*0.01*initialEqity))
df['ethvol_value'] = df['HV']/(df['HV'][0]/(percentInV*0.01*initialEqity))
df['portfolio_value'] = df['ethvol_value']+df['eth_value']

print(df) 

plt.plot(df['time'], df['portfolio_ETH'], color='red', linewidth=2, label="portfolio_ETH")
plt.plot(df['time'], df['portfolio_HV'], color='olive', linewidth=2, label="portfolio_HV")
plt.plot(df['time'], df['portfolio_value'], linestyle = 'dotted', label="portfolio_value")

plt.legend()
# show graph
plt.show()

st.pyplot()
ticker =df['portfolio_ETH']
Roll_Max = ticker.cummax()
Daily_Drawdown = ticker/Roll_Max - 1.0
Max_DD = Daily_Drawdown.cummin()
print(Roll_Max)
print(Daily_Drawdown)
print(Max_DD)

def get_return(df_param,param):
  return 100*(df_param.iloc[0][param]/df_param.iloc[len(df_param)-1][param])


Sharpe_Ratio = df['close'].pct_change(periods=1).mean() / df['close'].pct_change(periods=1).std()
st.write('Sharpe_Ratio ETH ONLY: ',(364**0.5)*(Sharpe_Ratio),' Return: ',get_return(df,'close'))

Sharpe_Ratio = df['HV'].pct_change(periods=1).mean() / df['HV'].pct_change(periods=1).std()
st.write('Sharpe_Ratio ETHVOL30: ',(364**0.5)*(Sharpe_Ratio),' Return: ',get_return(df,'HV'))

Sharpe_Ratio = df['portfolio_value'].pct_change(periods=1).mean() / df['portfolio_value'].pct_change(periods=1).std()
st.write(f'Sharpe_Ratio {percentInV}% ETHVOL30 with ETH: ',(364**0.5)*(Sharpe_Ratio),' Return: ',get_return(df,'portfolio_value'))

df2 = pd.read_csv('ittb-il-weth-dai.csv')
df2 = df2[df2['TIME (America/New York)'].str.contains('00:00:00')]
df2 = df2.rename({'TIME (America/New York)': 'time'}, axis='columns')
df2['time'] = pd.to_datetime(df2['time'])
df2['time'] = df2['time'].values.astype(np.int64) // 10 ** 9
df2.reset_index(inplace = True)

 
df2['DAI-ETH Pool Value'] =  df2['DAI-ETH Pool Value']*initialEqity
df2['DAI-ETH HODL Value'] =  df2['DAI-ETH HODL Value']*initialEqity
df2['DAI-ETH Pool Value w V percent share'] = df2['DAI-ETH Pool Value']*(1-(percentInV/100))
df2['DAI-ETH HODL Value w V percent share'] = df2['DAI-ETH HODL Value']*(1-(percentInV/100))
df2['Value Pool w V'] = df2['DAI-ETH Pool Value w V percent share']+ df['ethvol_value']
df2['Value HODL w V'] = df2['DAI-ETH HODL Value w V percent share']+ df['ethvol_value']
df2 = df2[df2['Value Pool w V']>0]
plt.plot(df2['time'], df2['DAI-ETH Pool Value'], color='olive', linestyle = 'dotted', label="Pool Value")
plt.plot(df2['time'], df2['DAI-ETH HODL Value'], color='red', linestyle = 'dotted', label="HODL Value")
plt.plot(df2['time'], df2['Value Pool w V'], color='olive', label="DAI-ETH Pool Value /w V")
plt.plot(df2['time'], df2['Value HODL w V'], color='red', label="DAI-ETH HODL Value /w V")

plt.legend()
# show graph
plt.show()
st.pyplot()


Sharpe_Ratio = df2['DAI-ETH Pool Value'].pct_change(periods=1).mean() / df2['DAI-ETH Pool Value'].pct_change(periods=1).std()
st.write('Sharpe_Ratio DAI-ETH Pool : ',(364**0.5)*(Sharpe_Ratio),' Returns: ',get_return(df2,'DAI-ETH Pool Value'))

Sharpe_Ratio = df2['DAI-ETH HODL Value'].pct_change(periods=1).mean() / df2['DAI-ETH HODL Value'].pct_change(periods=1).std()
st.write('Sharpe_Ratio DAI-ETH HODL Value: ',(364**0.5)*(Sharpe_Ratio),' Returns: ',get_return(df2,'DAI-ETH HODL Value'))

Sharpe_Ratio = df2['Value Pool w V'].pct_change(periods=1).mean() / df2['Value Pool w V'].pct_change(periods=1).std()
st.write(f'Sharpe_Ratio {percentInV}% ETHVOL30 with Value Pool w V: ',(364**0.5)*(Sharpe_Ratio),' Returns: ',get_return(df2,'Value Pool w V'))

Sharpe_Ratio = df2['Value HODL w V'].pct_change(periods=1).mean() / df2['Value HODL w V'].pct_change(periods=1).std()
st.write(f'Sharpe_Ratio {percentInV}% ETHVOL30 with Value HODL w V: ',(364**0.5)*(Sharpe_Ratio),' Returns: ',get_return(df2,'Value HODL w V'))