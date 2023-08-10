import pandas as pd
import time
import requests
import telegram
from datetime import datetime
import calendar 


def get_rsi():

    chat_id='-100768549567' # Chat Channel begin with -100
    bot = telegram.Bot(token='Telegram Token')

    for i in range(0,20):
        symbol='BTCUSDT'
        tick_interval = '5'
    
        now = datetime.utcnow()
        unixtime = calendar.timegm(now.utctimetuple())
        since = unixtime
        start=str(since-60*60*10)    
    
        url = 'https://api.bybit.com/public/linear/kline?symbol='+symbol+'&interval='+tick_interval+'&from='+str(start)
        
        
        data = requests.get(url).json()
        D = pd.DataFrame(data['result'])
        
        period=21
        df=D
        df['close'] = df['close'].astype(float)
        df2=df['close'].to_numpy()
        
        df2 = pd.DataFrame(df2, columns = ['close'])
        delta = df2.diff()
        
        up, down = delta.copy(), delta.copy()
        up[up < 0] = 0
        down[down > 0] = 0
        
        _gain = up.ewm(com=(period - 1), min_periods=period).mean()
        _loss = down.abs().ewm(com=(period - 1), min_periods=period).mean()
        
        RS = _gain / _loss
        
        
        rsi=100 - (100 / (1 + RS))  
        rsi=rsi['close'].iloc[-1]
        rsi=round(rsi,1)
        
        if rsi<30:
            text='Bybit '+symbol+' RSI: '+str(rsi)
        
            print(text)
            bot.sendMessage(chat_id=chat_id, text=text)
        print('RSI: ',rsi)   
        time.sleep(10)

if __name__ == "__main__":
    print(get_rsi())