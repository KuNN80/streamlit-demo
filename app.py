import streamlit as st
import requests
import pandas as pd

# Streamlit 페이지 설정
st.set_page_config(page_title="Real Estate Listings Viewer", layout="wide")
st.title("Real Estate Listings from Pages 1 to 10")
st.markdown("This page fetches and displays real estate listings from pages 1 to 10 using the Naver Real Estate API.")

# 쿠키와 헤더 정의 (사용자 설정 필요)
cookies = {
    # 쿠키 값 입력
}
headers = {
    # 헤더 값 입력
}

# API 데이터를 가져오는 함수 (캐싱을 사용해 성능 향상)
@st.cache_data
def fetch_all_data():
    all_articles = []
    for page in range(1, 11):
        try:
            # API 요청 URL
            url = f'https://new.land.naver.com/api/articles/complex/111515?realEstateType=APT%3AABYG%3AJGC%3APRE&tradeType=A1&tag=%3A%3A%3A%3A%3A%3A%3A%3A&rentPriceMin=0&rentPriceMax=900000000&priceMin=0&priceMax=900000000&areaMin=0&areaMax=900000000&oldBuildYears&recentlyBuildYears&minHouseHoldCount=300&maxHouseHoldCount&showArticle=false&sameAddressGroup=true&minMaintenanceCost&maxMaintenanceCost&priceType=RETAIL&directions=&page={page}&complexNo=111515&buildingNos=&areaNos=&type=list&order=prc'
            
            response = requests.get(url, cookies=cookies, headers=headers)
            
            # 응답이 성공적인 경우 데이터 처리
            if response.status_code == 200:
                data = response.json()
                articles = data.get("articleList", [])
                all_articles.extend(articles)
            else:
                st.warning(f"Failed to retrieve data for page {page}. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")
        except ValueError:
            st.error(f"Non-JSON response for page {page}.")
    return all_articles

# 모든 페이지의 데이터 가져오기
data = fetch_all_data()

# 데이터가 있는 경우 DataFrame으로 변환
if data:
    df = pd.DataFrame(data)
    
    # 표시할 열 선택
    selected_columns = [
        "articleNo", "articleName", "realEstateTypeName", "tradeTypeName", "floorInfo",
        "dealOrWarrantPrc", "areaName", "direction", "articleConfirmYmd", 
        "articleFeatureDesc", "tagList", "buildingName", "sameAddrMaxPrc", 
        "sameAddrMinPrc", "realtorName"
    ]
    df_display = df[selected_columns]
    
    # Streamlit에서 데이터 표시
    st.write("### Real Estate Listings - Pages 1 to 10")
    st.dataframe(df_display)

else:
    st.write("No data available.")
