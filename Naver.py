import html
import requests
from bs4 import BeautifulSoup
import numpy as np
import matplotlib.pyplot as plt

# 아래의 함수는 지역ID 를 파라미터로 전달하면, 해당 Html을 반환해주는 함수이다.
def Get_Url(Select_Number, Add_Number):
    return requests.get('https://land.naver.com/article/articleList.nhn?rletTypeCd=A01&tradeTypeCd=all&rletNo=' + str(int(Select_Number) + int(Add_Number)) + '&page=1')

# 프로그램 시작 부 인사 ////////////////////////////////////////////////////////////////////////
print('네이버 부동산 검색 프로그램에 오신걸 환영합니다')
print('==========================================')
print("본인이 원하는 지역을 아래의 리스트에서 선택해주시기 바랍니다.\n")

# 변수선언 (크롤링 결과 담기) //////////////////////////////////////////////////////////////////
DB_List =[]
DB_Name = []
DB_Discription = []
DB_Price = []
DB_Result = []

s="";
cntList = 0
Total_Price =0
#////////////////////////////////////////////////////////////////////////////////////////////

# 네이버 부동산에서 ID No가 1부터 9까지인 지역만 초기 리스트로 보여줌
for i in range(1,10):
    html = Get_Url(i,0)   #부동산 링크를 Requests를 이용하여 html Gethering
    soup = BeautifulSoup(html.text.encode("utf-8"),'html.parser')   # Beautifulsoup를 사용해서 위에서 받은 html을 DOM화 함
    all_divs = soup.find_all("title")   # 지역을 찾기위하여 title 부분을 따옴

    print(str(i) + "행을 크롤링 하는중입니다.\n")
    for i2 in all_divs:
        DB_List.append( str(i2).strip())

for i in DB_List:

    s = str(i).replace(chr(32),"")  # Replace 를 이용하여 필요없는 문자 (개행, 공백 등등 ) 삭제
    s = s.replace(chr(10), "")
    s = s.replace(chr(9), "")
    s = s[s.find('<title>')+7:s.find('</title>')]
    s= s[0:s.find(',매물')]   # 매물 키워드 전까지만 s 변수에 담기

    cntList =cntList + 1
    print(str(cntList) + ' : ' + s) #사용자가 지역을 보고 선택을 할수 있도록 리스팅 하는 과정

print("\n")
Select_Number = input("번호 입력 엔터 → 선택한 지역의 매물 통계 / N → 종료\n")    # input을 사용하여 사용자와 인터랙션을 할수 있도록 함.

if (Select_Number != "N"):  # N가 아닌 숫자를 입력했다면, 입력한 숫자의 지역번호에 대한 매물을 모두 나오게함

    Loop_Number = int(input("위에서 입력한 번호부터, 지금 입력하는 수만큼 다른 지역도 반복합니다 →\n"))

    for i3 in range(0,Loop_Number): # 위에서 선택한 지역부터 ~ 입력한 번호까지 최대, 최저, 평균가를 통계냄
        html = Get_Url(Select_Number,i3)    # Html Request
        soup = BeautifulSoup(html.text.encode("utf-8"),'html.parser')

        Title = soup.select_one("title")
        str_Temp = Title.text.replace(chr(32),"").replace(chr(10),"").replace(chr(9),"")
        str_Temp = str_Temp[0:str_Temp.find(',매물')]

        print( '\n' + str(i3+1) + ' : 검색 지역은 ====> ' + str_Temp)

        for tr in soup.select('tr'):    # tr 태그를 모두 선택
            s= tr.select_one('span[class=txt]') # tr태그에서 span -> class = txt 인 것들을 모두 추출 -> 집 설명
            s1 =tr.select_one('strong[title]') # strong[title]인 것들을 모두 추출 -> 가격

            if s != None:   # 만약 반환값이 있다면, 리스트에 Apeend (집 설명)
                DB_Discription.append((s.text))

            if s1 != None:  # 만약 반환값이 있다면, 리스트에 Append (집 가격)
                str_Temp = s1.text;

                if str_Temp.find("/")>0:
                    DB_Price.append(int(str_Temp[:str_Temp.find('/')-1].replace(",","")))   # 리스트에 데이터 담기
                else:
                    DB_Price.append(int(str_Temp.replace(",","")))

        if len(DB_Price) > 0 :  # 가격 리스트의 크기가 0 초과면 (즉 있다면,)
            # 크롤링한 결과물에 대한 전체 통계 ========================================================
            print("평균가 (" + str(int(np.mean(DB_Price))) + ") | 최저값 (" + str(np.min(DB_Price)) + ") | 최대값 (" +   str(np.max(DB_Price)) + ")")

        else:
            print("매물이 존재하지 않습니다.")

        while len(DB_Price) > 0: DB_Price.pop()
        while len(DB_Discription) > 0: DB_Discription.pop()

    # 위에서 지역별 통계를 보여주고, 해당 지역의 번호를 클릭하면 / 해당 지역에 어떤 매물이 있는지 디테일 하게 리스팅
    Last_Number = input("\n번호 입력 엔터 → 선택한 지역의 Detail한 매물 리스팅 / N → 종료\n")   # 숫자 입력시, 리스팅 / 그게 아니라면, 프로그램 종료
    if (Last_Number!="N"):

        html = Get_Url(Select_Number,Last_Number)
        soup = BeautifulSoup(html.text.encode("utf-8"),'html.parser')

        Title = soup.select_one("title")
        str_Temp = Title.text.replace(chr(32),"").replace(chr(10),"").replace(chr(9),"")
        str_Temp = str_Temp[0:str_Temp.find(',매물')]

        print( '\n' + '세부 리스팅 될 검색 지역은 ====> ' + str_Temp)

        for tr in soup.select('tr'):    # tr 태그를 모두 선택
            s= tr.select_one('span[class=txt]') # tr태그에서 span -> class = txt 인 것들을 모두 추출 -> 집 설명
            s1 =tr.select_one('strong[title]') # strong[title]인 것들을 모두 추출 -> 가격

            if s != None:   # 만약 반환값이 없다면, 리스트에 넣지않음
                DB_Discription.append((s.text))

            if s1 != None:
                str_Temp = s1.text;

                if str_Temp.find("/")>0:
                    DB_Price.append(int(str_Temp[:str_Temp.find('/')-1].replace(",","")))   # 리스트에 데이터 담기
                else:
                    DB_Price.append(int(str_Temp.replace(",","")))

        for i in range(len(DB_Price)):  # 리스트에 담은 만큼, 사용자가 볼수 있도록 ( 집설명 : 가격 ) 리스팅
            print(str(i+1) + " : " + DB_Discription[i] + " ===== 가격 : " + str(DB_Price[i]))

        # 선택한 아이디의 막대 그래프 보여주기
        plt.title("Average Price of Search Item",fontsize=12,color='k')
        plt.bar(range(len(DB_Price)), DB_Price)
        plt.show()

    else:
        print("프로그램을 종료하겠습니다.")
else:
    print("프로그램을 종료하겠습니다.")