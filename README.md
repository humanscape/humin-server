# Humin Server

## 기본 정보

### 주요 버전 관리

- Python 3.8.5
- PostgreSQL 12
- Django 3.2

## 시작하기

### 설치 (최초 실행)

개발환경을 동일하게 하기 위해서 [Python 3.8.5](https://www.python.org/downloads/release/python-385/) 를 설치해줍니다. 
Mac 기본 Python3 버전이 3.8.5 라면 진행할 필요없습니다.

1. 가상환경 생성 및 활성화
   
   In-project 가상환경 생성을 위해 다음과 같은 명령어를 실행합니다. 이 때 가상환경의 이름은 .venv 로 고정됩니다.
   ```
   $ python -m venv .venv
   ```
   - 나중에 다른 terminal 에서 접속하여 가상환경 활성화를 진행해야 할 때도 동일하게 위 명령어를 입력합니다.
   - 가상환경을 비활성화 할 때는 `deactivate` 명령어를 입력합니다.

2. requirements 설치
   로컬 세팅에 필요한 패키지들을 설치합니다.
    ```
    $ pip install -r requirements.txt
    ```

4. database 설치

   - [postgreSQL12](https://postgresapp.com/) 를 설치합니다.
   - [pgAdmin4](https://www.pgadmin.org/) 를 설치합니다.

### PR 올리기 전 확인 사항
1. Swagger Test
   - 새로 구현한 API 가 있다면 Swagger 를 통해 **반드시** 확인합니다.
   - 적어도 다음 사항들은 확인해주세요.
      - test code 통과 여부
      - Exception Case 에 대한 핸들링

2. Export requirements.txt 
   - 새로 설치한 package 가 있다면, requirements 를 새로 export 합니다.
      ```
      $ pip freeze > requirements.txt
