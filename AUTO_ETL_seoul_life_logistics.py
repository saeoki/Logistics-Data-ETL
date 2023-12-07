# 1. Google Cloud Storage API 연결
import os
from google.cloud import storage
from datetime import datetime
from io import StringIO
import requests
import pandas as pd
import calendar
from io import BytesIO
import time
import json

with open('config.json') as config_file:
    config = json.load(config_file)

googlo_cloud_api_key = config.get('GOOGLE_APPLICATION_CREDENTIALS')

if googlo_cloud_api_key is None:
    print("Google Cloud API 키를 찾을 수 없습니다.")
else:
    # 1-1) 환경변수 - Googlecloud_key 설정
    storage_client = storage.Client.from_service_account_json(
        googlo_cloud_api_key)
    buckets = list(storage_client.list_buckets())

    # 2. 현재 시간과 저장된 시간 확인
    nowdate = str(datetime.today().year) + \
        str(datetime.today().month)+str(datetime.today().day)
    lastmonth = str(datetime.today().year)+str(datetime.today().month-1)


def increment_month(input_month):
    year = int(input_month[:4])
    month = int(input_month[4:])
    if month == 12:
        year += 1
        next_month = str(year) + "01"
    else:
        next_month = str(year) + str(month + 1).zfill(2)
    return next_month


def makemonthcsv(folder_name, url, now_month, bucket, destination_blob_name):
    startidx = 1
    endidx = 999
    firsturl = url+str(startidx)+'/'+str(endidx)+"/"+now_month+"01"
    res = requests.get(firsturl)
    data = res.json()
    if folder_name == 'SEOUL_SEOUL':
        key = 'seoulGuGu'
        # 따로 추가 필요 없음
    elif folder_name == 'SEOUL_SIDO':
        key = 'seoulGuSido'
        new_column_name = 'REC_CTGG_NM'
        insert_idx = 7
    elif folder_name == 'SIDO_SEOUL':
        key = 'sidoSeoulgu'
        new_column_name = 'SEND_CTGG_NM'
        insert_idx = 3
    else:
        return None
    if 'RESULT' in data.keys():
        csv = None
        print(url+str(startidx)+'/'+str(endidx)+"/"+now_month+"01")
        print("이상")
        print(data['RESULT'])
        return None
    else:
        csv = pd.DataFrame(data[key]['row'])
        startidx = endidx+1
        endidx = startidx+999
        firsturl2 = url+str(startidx)+'/'+str(endidx)+"/"+now_month+"01"
        res2 = requests.get(firsturl2)
        data2 = res2.json()
        while 'RESULT' not in data2.keys():
            csv2 = pd.DataFrame(data2[key]['row'])
            csv = pd.concat([csv, csv2], ignore_index=True)

            startidx = endidx+1
            endidx = startidx+999
            firsturl2 = url+str(startidx)+'/'+str(endidx)+"/"+now_month+"01"
            res2 = requests.get(firsturl2)
            data2 = res2.json()

        first_day, last_day = calendar.monthrange(
            int(now_month[:4]), int(now_month[4:]))
        for day in range(2, last_day+1):
            time.sleep(0.5)
            startidx = 1
            endidx = 999
            nowurl2 = url+str(startidx)+'/'+str(endidx) + \
                "/"+now_month+str(day).zfill(2)
            res2 = requests.get(nowurl2)
            data2 = res2.json()

            while 'RESULT' not in data2.keys():
                csv2 = pd.DataFrame(data2[key]['row'])
                csv = pd.concat([csv, csv2], ignore_index=True)

                startidx = endidx+1
                endidx = startidx+999
                firsturl2 = url+str(startidx)+'/' + \
                    str(endidx)+"/"+now_month+str(day).zfill(2)
                res2 = requests.get(firsturl2)
                data2 = res2.json()

        # insert
        if folder_name in ['SEOUL_SIDO', 'SIDO_SEOUL']:
            null_values = [None] * len(csv)
            csv.insert(loc=insert_idx, column=new_column_name,
                       value=null_values)
            csv = csv[['DL_YMD', 'SEND_CTPV_NM', 'SEND_CTGG_NM', 'REC_CTPV_NM', 'REC_CTGG_NM',
                       'E_C_01', 'E_C_02', 'E_C_03', 'E_C_04', 'E_C_05', 'E_C_06', 'E_C_07', 'E_C_08', 'E_C_09', 'E_C_10', 'E_C_11']]
            conversion_rules = {'E_C_01': int, 'E_C_02': int, 'E_C_03': int, 'E_C_04': int, 'E_C_05': int,
                                'E_C_06': int, 'E_C_07': int, 'E_C_08': int, 'E_C_09': int, 'E_C_10': int, 'E_C_11': int}
            csv = csv.astype(conversion_rules)
            csv.rename(columns={'DL_YMD': 'delivery_date', 'SEND_CTPV_NM': 'sender_city', 'SEND_CTGG_NM': 'sender_district', 'REC_CTPV_NM': 'recipient_city', 'REC_CTGG_NM': 'recipient_district',
                                'E_C_01': 'category_furniture_and_interior', 'E_C_02': 'category_others',
                                'E_C_03': 'category_book_and_music', 'E_C_04': 'category_digital_and_appliances',
                                'E_C_05': 'category_living_and_health', 'E_C_06': 'category_sports_and_leisure',
                                'E_C_07': 'category_food', 'E_C_08': 'category_parenting',
                                'E_C_09': 'category_fashion_clothing', 'E_C_10': 'category_fashion_accessories',
                                'E_C_11': 'category_beauty_cosmetics'}, inplace=True)

    blob = bucket.blob(destination_blob_name)

    # CSV 데이터를 문자열로 변환
    csv_string = csv.to_csv(index=False, encoding='utf-8')  # UTF-8로 인코딩

    # 문자열을 BytesIO로 감싸서 업로드
    csv_bytes = BytesIO(csv_string.encode('utf-8'))  # UTF-8로 인코딩된 바이트로 변환
    blob.upload_from_file(csv_bytes, content_type='text/csv')
    print(f"CSV data uploaded to {destination_blob_name} in bucket")


def check(bucket_name, folder_name, url):
    folder_path = 'Seoul-Life-Logistics/'+folder_name+'/'
    # 버킷 객체 생성
    client = storage.Client()
    # 특정 버킷 가져오기
    bucket = storage_client.get_bucket(bucket_name)
    # 폴더 내 객체(파일)목록 가져오기
    blobs = bucket.list_blobs(prefix=folder_path)
    blob_list = []
    for blob in blobs:
        blob_list.append(blob.name)
    blob_list.sort()

    if blob_list[-1][-10:-4] < lastmonth and blob_list[-1][-10:-4] >= "202001":

        # 제일 최근파일 삭제(그 전에 모든 정보가 들어있지 않을 수도 있어서)
        now_month = blob_list[-1][-10:-4]
        destination_blob_name = folder_path+'DWC_KXLCLS_OD_DAY_' + \
            folder_dict[folder_name][1]+'_'+now_month+'.csv'
        del_blob = bucket.blob(destination_blob_name)
        try:
            del_blob.delete()
            print(f'Blob {destination_blob_name} deleted successfully.')
        except Exception as e:
            print(f'Error deleting blob {destination_blob_name}: {e}')

        while now_month <= lastmonth:
            destination_blob_name = folder_path+'DWC_KXLCLS_OD_DAY_' + \
                folder_dict[folder_name][1]+'_'+now_month+'.csv'
            result_csv = makemonthcsv(
                folder_name, url, now_month, bucket, destination_blob_name)
            now_month = increment_month(now_month)
    else:
        print("Nothing to change!")


# 2-1. (서울 공공데이터 포탈) 서울시 생활물류
with open('config.json') as config_file:
    config = json.load(config_file)

seoul_api_key = config.get('seoul_api_key')

if seoul_api_key is None:
    print("API 키를 찾을 수 없습니다.")
else:
    bucket_name = 'programmers-devcourse-project2'
    folder_list = ['SEOUL_SEOUL', 'SEOUL_SIDO', 'SIDO_SEOUL']
    folder_dict = {'SEOUL_SEOUL': ["http://openapi.seoul.go.kr:8088/"+seoul_api_key+"/json/seoulGuGu/", "SEOULGU_SEOULGU"],
                   'SEOUL_SIDO': ["http://openapi.seoul.go.kr:8088/"+seoul_api_key+"/json/seoulGuSido/", "SEOULGU_SIDO"],
                   'SIDO_SEOUL': ["http://openapi.seoul.go.kr:8088/"+seoul_api_key+"/json/sidoSeoulgu/", "SIDO_SEOULGU"]}
    for folder in folder_list:
        folder_path = 'Seoul-Life-Logistics/'+folder+'/'
        check(bucket_name, folder, folder_dict[folder][0])


# ##2-2. 우체국 전국 시도별 우편물류 데이터
