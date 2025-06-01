import streamlit as st
import plotly.express as px
import pandas as pd
from bs4 import BeautifulSoup
import requests

class saramin:
    def __init__(self):
        self.result_df = pd.DataFrame()
    def collector(self, keyword):
        url = 'https://www.saramin.co.kr/zf_user/search?search_area=main&search_done=y&search_optional_item=n&searchType=search'
        params = {'searchword' : keyword}
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(url, params = params, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        company = soup.find_all('strong', class_ = "corp_name")
        RecUrl = soup.find_all('div', class_ = "area_job")
        site = ['Saramin'] * len(RecUrl)
        company_lst = [c.text.strip() for c in company]
        recruit_lst = [r.find('h2', class_ = 'job_tit').text.replace("\n", " ") for r in RecUrl]
        detail_tmp = [d.find('div', class_ = 'job_condition') for d in RecUrl]
        detail_lst = [[c.text for c in d.find_all('span')] for d in detail_tmp]
        url_lst = ['https://www.saramin.co.kr' + u.find('a')['href'] for u in RecUrl]
        self.result_df = pd.DataFrame({'Site': site,
        'Col_Company': company_lst,
        'Col_Recruit': recruit_lst,
        'Col_Detali' : detail_lst,
        'Col_Url' : url_lst 
        })
        return self.result_df
    
class jobkorea:
    def __init__(self):
        self.result_df = pd.DataFrame()
    def collector(self, keyword):
        url = 'https://www.jobkorea.co.kr/Search/'
        params = {'stext' : keyword}
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(url, params = params, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        company = soup.find_all('span', class_ = "Typography_variant_size16__344nw26 Typography_weight_regular__344nw2d Typography_color_gray900__344nw2k styles_mr_space4__dk46ts22")
        recruit = soup.find_all('span', class_ = "Typography_variant_size18__344nw25 Typography_weight_medium__344nw2c Typography_color_gray900__344nw2k Typography_truncate__344nw2t")
        detail = soup.find_all('div', class_ = "Flex_display_flex__i0l0hl2 Flex_gap_space16__i0l0hlj Flex_direction_row__i0l0hl3")
        url_lst = soup.find_all('a', class_ = "Flex_display_flex__i0l0hl2 Flex_gap_space4__i0l0hly Flex_align_center__i0l0hl8 h7nnv12")
        site = ['jobkorea'] * len(url_lst)
        company_lst = [c.text.strip() for c in company]
        recruit_lst = [r.text.replace("\n", " ") for r in recruit]
        detail_lst = [[c.text for c in d.find_all('span')] for d in detail]
        url_lst = [u['href'] for u in url_lst]
        self.result_df = pd.DataFrame({'Site': site,
        'Col_Company': company_lst,
        'Col_Recruit': recruit_lst,
        'Col_Detali' : detail_lst,
        'Col_Url' : url_lst 
        })
        return self.result_df


if __name__ == "__main__":
    st.title('Title')
    with st.container(border = True):
        if st.button("Recruit Searching"):
            job_df = jobkorea().collector('데이터분석')
            saram_df = saramin().collector('데이터분석')
            result_df = pd.concat([job_df, saram_df], ignore_index= True)
            summary_df = result_df.groupby('Site').agg(
                Count = ('Site', 'count'),
                Ratio = ('Site', lambda x : round(len(x) / len(result_df) * 100, 2)
            )).reset_index()
            st.dataframe(result_df)
            st.dataframe(summary_df)

            fig = px.pie(summary_df,
                         names = 'Site',
                         values = 'Ratio',
                         title = 'Recruitment Ratio')
            
            st.plotly_chart(fig)

