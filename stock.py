import streamlit as st
from datetime import datetime, timedelta
from pykrx import stock
import pandas as pd
import os
from pytz import timezone

filePath, fileName = os.path.split(__file__)
# yf.pdr_override()
# now = datetime.now()
# end_day = datetime(now.year, now.month, now.day)
# start_day = end_day - timedelta(days = 365)

# kospi_df = stock.get_index_fundamental(start_day.strftime('%Y%m%d'), end_day.strftime('%Y%m%d'), "1001") # 코스피

# st.metric('코스피 지수', value = kospi_df.iloc[-1, 0], delta = str(kospi_df.iloc[-1, 1]) + '%')

# tab1, tab2 = st.tabs(["지수 현황", "등락 폭 비교"])
# with tab1:
#     st.line_chart(kospi_df['종가'], use_container_width = True)
# with tab2:
#     pass

# 안녕헬로

df = pd.read_csv(os.path.join(filePath, 'data', '상장법인목록.csv'))
print(df)
name = st.text_input('종목명을 입력해주세요😊')
if name:
    try:
        code = df.loc[df['cooperation'] == name].iloc[0,0]
        # df['cooperation']df
        print(code)

        now = datetime.today()
        end_day = datetime(now.year, now.month, now.day)
        start_day = end_day - timedelta(days = 365)
        df = stock.get_market_ohlcv(start_day.strftime('%Y%m%d'), end_day.strftime('%Y%m%d'), code)
        st.metric(name, value = df.iloc[-1, 3], delta = str(df.iloc[-1, 6]) + '%')
        st.line_chart(df['종가'])
    except:
        st.write('❗정확한 종목명을 입력해주세요')