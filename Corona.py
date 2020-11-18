from datetime import date, timedelta
from urllib.request import urlopen
import pandas as pd
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.animation as animation
########################################################################################
# 한글사용
import matplotlib.font_manager as fm
font_location = 'C:/Windows/Fonts/Malgun.ttf'
font_family = fm.FontProperties(fname=font_location).get_name()
plt.rc('font', family=font_family)
########################################################################################
# API 링크관련
strd = '20200319'  # 시작일
endd = '20201116'  # 종료일
curl = 'http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19NatInfStateJson?serviceKey='  # api 사이트링크
key = 'IrmQujn6Ay6i4waFVlIeKdTtmnjiTGbhFjHkpUCYlRTG9LdT6qIrJlR81NiiGkfRJN%2FWkulBX%2F2zhbzkpBHsaQ%3D%3D'  # 인증키
request = f'&pageNo=1&numOfRows=10&startCreateDt={strd}&endCreateDt={endd}'  # 불러올값설정
print(curl + key + request)
########################################################################################
# API 값 읽어오기
cpa = urlopen(curl + key + request).read()
tree = ET.fromstring(cpa)
findt = tree.findall('./body/items/item')
########################################################################################
# 값 저장할 리스트들
Std_day = []  # api 날짜저장
Nation_name = []  # api 나라이름저장
Nat_def_cut = []  # api 확진자수저장
Area_name = []  # api 대륙이름저장
NNSlist = []  # api 받아온값들 저장된 리스트들 통합용리스트
datelist = []  # 애니메이션에 사용될 날짜들 저장될 리스트
########################################################################################
# API에서 읽어온값 리스트에 추가
for item in findt:
    Nation_name.append(item.find('nationNm').text)
    Nat_def_cut.append(item.find('natDefCnt').text)
    Std_day.append(item.find('createDt').text)
    Area_name.append(item.find('areaNmEn').text)
# print(Nation_name)
# print(Nat_def_cut)
# print(Std_day)
# print(set(Area_name))
########################################################################################
# Std_day 값 가공
for i in range(len(Std_day)):
    Std_day[i] = Std_day[i][:10]  # 필요한만큼 잘라내기
    Std_day[i] = Std_day[i].split('-')  # -문자 기준으로 잘라내기(결과물예시 : '2020','10','14)
    Std_day[i] = ''.join(Std_day[i])  # 위에서 잘라낸문자열을 합치기(결과물예시 : 20201014
# print(Std_day)
########################################################################################
# 확진자수가 문자열로 되있어서 int로 형변환(안해주면 나중에 int 필요한위치에 사용못함)
Nat_def_cut = list(map(int, Nat_def_cut))
Std_day = list(map(int, Std_day))
# print(Nat_def_cut)
########################################################################################
# 리스트에 추가된값 리스트하나로 묶어버리기(데이터프레임 제작을위해)
NNSlist = list(zip(Nation_name, Area_name, Nat_def_cut, Std_day))
# for i in NNSlist123:
#     print(i)
########################################################################################
# 리스트를 DataFrame으로 변환
df_list = pd.DataFrame(NNSlist, columns=['나라명', '그룹', '누적 확진자 수', '일자'])
#print(df_list)
########################################################################################
# 날짜변수 생성
d1 = date(2020, 3, 19)  # 시작일
d2 = date.today()  # 종료일(오늘)
delta = d2 - d1
# print(d1, d2, delta)
for i in range(delta.days + 1):
    d = d1 + timedelta(days=i)
    d = d.strftime('20%y%m%d')  # 문자열로변경
    datelist.append(d)  # 리스트에 추가
datelist = list(map(int, datelist))  # int 형변환
# print(datelist)
########################################################################################
# 색깔설정
# 참고사이트 : https://towardsdatascience.com/bar-chart-race-in-python-with-matplotlib-8e687a5c8a41
colors = dict(zip(
    ['Europe', 'Asia', 'Africa', 'Middle Ease', 'MiddleEase',
     'Middle East', 'Oceania', '大洋洲', 'Others', 'America', None],
    ['peru', 'maroon', 'olive', 'teal', 'royalblue',
     'slateblue', 'violet', 'orange', '#forestgreen', 'salmon', 'aqua']
))
group_lk = df_list.set_index('나라명')['그룹'].to_dict()
########################################################################################
# 화면설정
fig, ax = plt.subplots(figsize=(15, 8))
########################################################################################
# 바차트 제작에 쓰일 함수
def draw_barchart(day):
    dff = df_list[df_list['일자'].eq(day)].sort_values(by='누적 확진자 수', ascending=True).tail(10)
    ax.clear()
    ax.barh(dff['나라명'], dff['누적 확진자 수'], color=[colors[group_lk[x]] for x in dff['나라명']])
    dx = dff['누적 확진자 수'].max() / 200
    for i, (value, name) in enumerate(zip(dff['누적 확진자 수'], dff['나라명'])):
        ax.text(value - dx, i, name, size=14, weight=600, ha='right', va='bottom')
        ax.text(value - dx, i - .25, group_lk[name], size=10, color='#444444', ha='right', va='baseline')
        ax.text(value + dx, i, f'{value:,.0f}', size=14, ha='left', va='center')
    # ... polished styles
    ax.text(1, 0.4, day, transform=ax.transAxes, color='#777777', size=46, ha='right', weight=800)
    ax.text(0, 1.06, 'Population (thousands)', transform=ax.transAxes, size=12, color='#777777')
    ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    ax.xaxis.set_ticks_position('top')
    ax.tick_params(axis='x', colors='#777777', labelsize=12)
    ax.set_yticks([])
    ax.margins(0, 0.01)
    ax.grid(which='major', axis='x', linestyle='-')
    ax.set_axisbelow(True)
    ax.text(0, 1.12, '전세계 코로나 확진자수 현황',
            transform=ax.transAxes, size=24, weight=600, ha='left')
    ax.text(1, 0, 'by @pratapvardhan; credit @jburnmurdoch', transform=ax.transAxes, ha='right',
            color='#777777', bbox=dict(facecolor='white', alpha=0.8, edgecolor='white'))
    plt.box(False)
########################################################################################
# 바차트 제작
animator = animation.FuncAnimation(fig, draw_barchart, frames=datelist)
plt.show()
########################################################################################