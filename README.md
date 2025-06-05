(인게임 내 html 요소 배치 및 전체적인 UI 스타일 구성 등 프론트엔드 부분에 ChatGPT 사용)



# 🔔 할리갈리 온라인 🍓

## 🚀 프로젝트 개요
### 🐋 Docker Compose를 활용한 할리갈리 게임
- 웹소켓을 활용한 실시간 웹사이트 게임으로, 멀티플레이 가능

-  브라우저 세션을 통해 사용자 구별, 로그인 없이 닉네임만 입력해도 게임에 참여 가능
  
- Docker가 설치되어 있다면 명령어 몇번만 입력하여 배포 가능

- 게임 결과 저장 및 플레이어별 승리 횟수, 패배 횟수, 총 전적 DB에 자동 기록
  
- 통계 페이지(추가 예정)에서 전적 확인 가능

<br/>

## 🖥️ 화면 구성
|초기 화면|
|:---:|
|<img src="https://github.com/user-attachments/assets/fa46020d-1e72-42a7-b50d-d84ead0ccf2e" width="450"/>|
|닉네임을 입력하여 게임에 입장 가능|

|로비 화면|
|:---:|
|<img src="https://github.com/user-attachments/assets/442a859c-9336-4664-852f-08b511f265d4" width="450"/>|
|웹소켓을 활용하여 실시간 방 생성 및 게임 입장 확인|

|인게임|
|:---:|
|<img src="https://github.com/user-attachments/assets/652d7998-cbe7-487a-bc70-26ad39d3ae91" width="450"/>|
|웹소켓을 통해 같은 방 내 플레이어끼리 게임상황에 대해 실시간 통신|

<br />

## ⚙️ 기술 스택
### Backend
<div>
  <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"> 
  <img src="https://img.shields.io/badge/flask-000000?style=for-the-badge&logo=flask&logoColor=white">
  <img src="https://img.shields.io/badge/mysql-4479A1?style=for-the-badge&logo=mysql&logoColor=white">
</div>

### Frontend
<div>
  <img src="https://img.shields.io/badge/node.js-339933?style=for-the-badge&logo=Node.js&logoColor=white">
  <img src="https://img.shields.io/badge/vue.js-4FC08D?style=for-the-badge&logo=vue.js&logoColor=white"> 
  <img src="https://img.shields.io/badge/Nginx-009639?logo=nginx&logoColor=white&style=for-the-badge">
</div>

### Tools
<div>
  <img src="https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white"> 
  <img src="https://img.shields.io/badge/Git-%23F05032.svg?style=for-the-badge&logo=git&logoColor=white">
<img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white">
</div>

<br />

## 🤖 프로젝트 요구사항 (윈도우 기준)
- git 버전 2.40.0 이상
- Docker 버전 28.1.1 이상
- Docker Compose v2.35.1-desktop.1 이상
- 호스트 컴퓨터 80번, 5000번, 3306번 포트 사용 가능

<br />

### ❓ 호스트 컴퓨터에서 요구하는 포트를 이미 사용 중이라면?
docker-compose.yml의 다음 부분을 변경
```yml

version: '3'

services:
  mysql:
    image: mysql:8.0
    container_name: halligalli-mysql
    environment:
      - MYSQL_ROOT_PASSWORD=cloudComputing331
      - MYSQL_DATABASE=halligalli
      - MYSQL_USER=halligalli
      - MYSQL_PASSWORD=halligalli
    volumes:
      - mysql_data:/var/lib/mysql
      - ./mysql/init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "<비어있는 포트>:3306"

  halligalli-backend:
    build: ./backend
    image: halligalli-backend:5.0.0-compose
    environment:
      - DB_HOST=mysql
      - DB_PORT=3306
      - DB_NAME=halligalli
      - DB_USER=halligalli
      - DB_PASSWORD=halligalli
      - SECRET_KEY=cloudComputingIsSoBeneficialAndFun
    depends_on:
      - mysql
    command: sh -c "sleep 10 && python app.py"
    ports:
      - "<비어있는 포트>:5000"

  halligalli-frontend:
    build: ./frontend
    image: halligalli-frontend:5.0.0-compose
    environment:
      - BACKEND_HOST=halligalli-backend
      - BACKEND_PORT=5000
    depends_on:
      - halligalli-backend
    ports:
      - "<비어있는 포트>:80"

volumes:
  mysql_data:

```

<br />

## 📌 설치 및 실행 방법 (bash 기준)
1. **리포지토리 클론 후 루트 디렉토리 이동**

   ```bash
  
   git clone https://github.com/Meowning/HalliGalli.git
   cd HalliGalli

   ```

<br />


2. **Docker 이미지 빌드 및 서비스 시작**

   ```bash
   docker-compose up -d --build
   ```


- 로그를 확인하고 싶은 경우 루트 디렉토리에서 다음 입력 (로그 출력 종료를 원하는 경우 Ctrl + C)
  
   ```bash
     docker-compose logs -f
   ```
   
<br />


3. **서비스 접속**
- (기본 포트 사용 시) 웹 브라우저에서 ```http://localhost``` 접속

- (포트 변경 시) 웹 브라우저에서 ```http://localhost:<포트>``` 접속

- (같은 LAN에서 접속 시) 웹 브라우저에서 ```http://<호스트 컴퓨터의 내부 IP>(:포트)``` 접속

- 다른 네트워크에서의 외부 접속을 허용하고 싶은 경우 포트포워딩 등 추가 작업 필요

  (bash에서 ```ipconfig``` 입력 시, 내부 IPV4 주소 확인 가능)

<br />


4. **서비스 중지**
  - 서비스 중지 시 루트 디렉토리로 이동 후

   ```bash

   docker-compose down

   ```
