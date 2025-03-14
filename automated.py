import MetaTrader5 as mt5
import time
from tqdm import tqdm
#REPLACE WITH YOUR OWN SIGNALS FILE
import pickle
import data


def PURCHASE(symbol, type, tp, sl, volume):

    price = mt5.symbol_info_tick(symbol)
    price = price.ask
    
    request = {
        'action':mt5.TRADE_ACTION_DEAL,
        'symbol':symbol,
        'volume':volume,
        'type':type,
        'price':price,
        'sl':sl,
        'tp':tp,
        'deviation':20,
        'magic': 12345678,
        'comment':'Python script open',
        'type_time':mt5.ORDER_TIME_GTC,
        'type_filling': mt5.ORDER_FILLING_IOC
    }

    result = mt5.order_send(request)
    return result

if __name__ == '__main__':
    username = None
    password = None
    server = None

    mt5.initialize()
    mt5.login(username, password, server)
    info = mt5.account_info()


    with open('tickers.pickle', 'wb') as file:
        tickers = pickle.load(file)

    start = time.time()
    while mt5.last_error() == 1:
        balance = info.balance()
        leverage = info.leverage()

        for ticker in tqdm(tickers):
            df = data.get_rates(ticker)

            signal, stop_loss, take_profit, volume = signals.signal1(df, balance, leverage, ticker)
            if signal != None:
                type = mt5.ORDER_TYPE_BUY if signal =='BUY' else mt5.ORDER_TYPE_SELL

                PURCHASE(symbol = ticker,
                           type = type,
                           tp = take_profit,
                           sl = stop_loss,
                           volume = volume
                        )
        
        time.sleep(60)
        time_live = start - time.time()

        print(f'Time live: {time_live}')
