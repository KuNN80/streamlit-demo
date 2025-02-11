{\rtf1\ansi\ansicpg1252\cocoartf2820
\cocoatextscaling1\cocoaplatform1{\fonttbl\f0\fnil\fcharset0 .SFUI-Semibold;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\pard\tx560\tx1120\tx1680\tx2240\tx2800\tx3360\tx3920\tx4480\tx5040\tx5600\tx6160\tx6720\pardirnatural\partightenfactor0

\f0\b\fs24 \cf0 #Naver \uc0\u48512 \u46041 \u49328  \u53076 \u46300 \
import streamlit as st\
import requests\
import pandas as pd\
\
# Streamlit \uc0\u54168 \u51060 \u51648  \u49444 \u51221 \
st.set_page_config(page_title="Real Estate Listings Viewer", layout="wide")\
st.title("Real Estate Listings from Pages 1 to 10")\
st.markdown("This page fetches and displays real estate listings from pages 1 to 10 using the Naver Real Estate API.")\
\
# \uc0\u53216 \u53412 \u50752  \u54756 \u45908  \u51221 \u51032  (\u49324 \u50857 \u51088  \u49444 \u51221  \u54596 \u50836 )\
cookies = \{\
    # \uc0\u53216 \u53412  \u44050  \u51077 \u47141 \
\}\
headers = \{\
    # \uc0\u54756 \u45908  \u44050  \u51077 \u47141 \
\}\
\
# API \uc0\u45936 \u51060 \u53552 \u47484  \u44032 \u51256 \u50724 \u45716  \u54632 \u49688  (\u52880 \u49905 \u51012  \u49324 \u50857 \u54644  \u49457 \u45733  \u54693 \u49345 )\
@st.cache_data\
def fetch_all_data():\
    all_articles = []\
    for page in range(1, 11):\
        try:\
            # API \uc0\u50836 \u52397  URL\
            url = f'https://new.land.naver.com/api/articles/complex/111515?realEstateType=APT%3AABYG%3AJGC%3APRE&tradeType=A1&tag=%3A%3A%3A%3A%3A%3A%3A%3A&rentPriceMin=0&rentPriceMax=900000000&priceMin=0&priceMax=900000000&areaMin=0&areaMax=900000000&oldBuildYears&recentlyBuildYears&minHouseHoldCount=300&maxHouseHoldCount&showArticle=false&sameAddressGroup=true&minMaintenanceCost&maxMaintenanceCost&priceType=RETAIL&directions=&page=\{page\}&complexNo=111515&buildingNos=&areaNos=&type=list&order=prc'\
            \
            response = requests.get(url, cookies=cookies, headers=headers)\
            \
            # \uc0\u51025 \u45813 \u51060  \u49457 \u44277 \u51201 \u51064  \u44221 \u50864  \u45936 \u51060 \u53552  \u52376 \u47532 \
            if response.status_code == 200:\
                data = response.json()\
                articles = data.get("articleList", [])\
                all_articles.extend(articles)\
            else:\
                st.warning(f"Failed to retrieve data for page \{page\}. Status code: \{response.status_code\}")\
        except requests.exceptions.RequestException as e:\
            st.error(f"An error occurred: \{e\}")\
        except ValueError:\
            st.error(f"Non-JSON response for page \{page\}.")\
    return all_articles\
\
# \uc0\u47784 \u46304  \u54168 \u51060 \u51648 \u51032  \u45936 \u51060 \u53552  \u44032 \u51256 \u50724 \u44592 \
data = fetch_all_data()\
\
# \uc0\u45936 \u51060 \u53552 \u44032  \u51080 \u45716  \u44221 \u50864  DataFrame\u51004 \u47196  \u48320 \u54872 \
if data:\
    df = pd.DataFrame(data)\
    \
    # \uc0\u54364 \u49884 \u54624  \u50676  \u49440 \u53469 \
    selected_columns = [\
        "articleNo", "articleName", "realEstateTypeName", "tradeTypeName", "floorInfo",\
        "dealOrWarrantPrc", "areaName", "direction", "articleConfirmYmd", \
        "articleFeatureDesc", "tagList", "buildingName", "sameAddrMaxPrc", \
        "sameAddrMinPrc", "realtorName"\
    ]\
    df_display = df[selected_columns]\
    \
    # Streamlit\uc0\u50640 \u49436  \u45936 \u51060 \u53552  \u54364 \u49884 \
    st.write("### Real Estate Listings - Pages 1 to 10")\
    st.dataframe(df_display)\
\
else:\
    st.write("No data available.")}