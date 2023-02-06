import streamlit as st
from datetime import datetime, timedelta
from pykrx import stock
import pandas as pd
import os
from pytz import timezone


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

def stock_price(stock_name, code, start_day, end_day):
    '''
    검색 종목 주식의 날짜별 고가, 저가, 종가와 실시간 가격을 시각화합니다.
    '''
    try:
        df = stock.get_market_ohlcv(start_day.strftime('%Y%m%d'), end_day.strftime('%Y%m%d'), code)
        st.metric(stock_name, value = df.iloc[-1, 3], delta = str(df.iloc[-1, 6]) + '%')
        st.line_chart(df[['고가','저가','종가']], use_container_width= True)
    except Exception as E:
        st.write('stock_price 함수 오류')
        st.write(E)



def main():
    
    # 경로 세팅
    filePath, fileName = os.path.split(__file__)
    
    # 페이지 세팅
    st.set_page_config(page_title = "대국민 주식 분석 프로젝트", layout='wide', initial_sidebar_state='collapsed',)
    
    # 날짜
    now = datetime.today()
    end_day = datetime(now.year, now.month, now.day)
    start_day = end_day - timedelta(days = 365)

    # 사이드바 정보
    with st.sidebar:
        # 코스피 정보
        kospi_df = stock.get_index_fundamental(start_day.strftime('%Y%m%d'), end_day.strftime('%Y%m%d'), "1001") # 코스피
        st.metric('코스피 지수', value = kospi_df.iloc[-1, 0], delta = str(kospi_df.iloc[-1, 1]) + '%')
        st.line_chart(kospi_df['종가'], use_container_width = True)
        
    # 필요 데이터 불러오기
    base_df = pd.read_csv(os.path.join(filePath, 'data', '상장법인목록.csv'))
    
    # 입력 받은 종목명 저장
    stock_name = st.text_input('정확한 종목명을 입력해주세요😊', '삼성전자')
    
    if stock_name in tuple(base_df['cooperation']):
        # 종목명으로 티커 찾기
        code = base_df.loc[base_df['cooperation'] == stock_name].iloc[0,0]
        
        # 화면 분할
        col1, col2 = st.columns(2)
        with col1:
            # 시각화
            stock_price(stock_name, code, start_day, end_day)
            
    elif stock_name not in tuple(base_df['cooperation']):
        st.write('❗정확한 종목명을 입력하세요❗')

if __name__ == "__main__":
    main()