# [Programmers-devcourse]
### Project2 데이터 웨어하우스를 이용한 대시보드 구성
<br/>
<br/>
## 주제
### 물류 데이터로 확인하는 우리 동네 택배 현황
데이터 웨어하우스를 이용하여 ETL 프로세스를 구축하고 대시보드 구성해 보는 프로젝트
<br/>
<br/>
## 목표
물류 데이터를 활용하여 __`지역별 물류생활 대시보드`__ 를 생성하는것을 목표로 합니다.
<br/>
__ELT 프로세스__(데이터 수집, 전처리, 클라우드 스토리지에 저장, 데이터웨어하우스에 적재)를 경험하고, 
<br/>
데이터웨어하우스에 적재된 데이터를 활용하여 데이터 분석 및 __대시보드__를 생성합니다. 
<br/>
<br/>
## 기대효과
<br/>
<br/>

------------

## 사용 데이터
- `[서울시 생활물류 데이터](https://data.seoul.go.kr/dataList/OA-21866/S/1/datasetView.do)`
<br/>
- `[우편물류 데이터(시/도)](https://www.koreapost.go.kr/)`
<br/>
- `[우편물류 데이터(구/동)](https://kdx.kr/data/view/31129)`
<br/>
<br/>
## 프로젝트 구조
![image](https://github.com/Logistics-Devcourse/Data-ETL/assets/77157003/b4ec0647-5d8c-4744-bf37-bfcc24e1d15e)
<br/>
1. API, 크롤링을 통한 사용데이터 수집
2. 데이터 전처리 및 클라우드 스토리지 적재
3. Google storage에 저장된 파일을 Snowflake로 벌크 업데이트
4. 데이터 웨어하우스(Snowflake) 대시보드(Superset)에 연결
5. 대시보드 생성 및 데이터 분석
<br/>
<br/>
## 사용 기술
### 데이터 수집 및 전처리
- Python
- BeautifulSoup
- Pandas
<br/>
### Storage
- Google Storage
<br/>
### Data Warehouse
- Snowflake
<br/>
### 시각화
- Superset(preset.io)
<br/>
### 협업
- GitHub
- Mysql Workbench
- Visual Studio Code
<br/>
<br/>

-----------
## 역할
### PM
- 이서림 : GCS 및 Snowflake 환경설정
### 분석 테이블 설계
- 김동연
### ETL 프로세스
- 이서림 : [우편물류 데이터(구/동)](https://kdx.kr/data/view/31129) 데이터 수집 전처리 및 데이터 웨어하우스 적재
- 정세욱 : 지역별 인구 수 데이터 수집 전처리 및 데이터 웨어하우스 적재
- 최은서 : [서울시 생활물류 데이터](https://data.seoul.go.kr/dataList/OA-21866/S/1/datasetView.do) 데이터 스크립트 파일로 수집 자동화, [우편물류 데이터(시/도)](https://www.koreapost.go.kr/) 데이터 수집 전처리 및 데이터 웨어하우스 적재
### (공통)대시보드 작성 및 물류생활 리포트 작성

