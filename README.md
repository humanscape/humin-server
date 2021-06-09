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
1. Test
   - 새로 구현한 API 가 있다면 test 를 통해 **반드시** 확인합니다.
   ```
   $ coverage run manage.py test
   ```
   - Exception Case 에 대한 핸들링

2. Export requirements.txt 
   - 새로 설치한 package 가 있다면, requirements 를 새로 export 합니다.
      ```
      $ pip freeze > requirements.txt
      ```
      
### Test Coverage
```
Name                                 Stmts   Miss  Cover
--------------------------------------------------------
batch_tasks/__init__.py                  0      0   100%
batch_tasks/migrations/__init__.py       0      0   100%
batch_tasks/tests.py                     1      0   100%
batch_tasks/views.py                    58     45    22%
events/__init__.py                       0      0   100%
events/admin.py                          1      0   100%
events/apps.py                           4      0   100%
events/migrations/__init__.py            0      0   100%
events/models.py                        12      0   100%
events/serializers.py                   27      6    78%
events/tests.py                          1      0   100%
events/views.py                         16      9    44%
manage.py                               12      2    83%
reservationroom/__init__.py              0      0   100%
reservationroom/settings.py             25      0   100%
reservationroom/urls.py                  6      0   100%
users/__init__.py                        0      0   100%
users/admin.py                           1      0   100%
users/apps.py                            4      0   100%
users/migrations/__init__.py             0      0   100%
users/models.py                          5      0   100%
users/serializers.py                     6      0   100%
users/tests.py                           1      0   100%
users/views.py                          25     17    32%
--------------------------------------------------------
TOTAL                                  205     79    61%
```

## 서버 배포

해당 가이드는 Centos8버전을 기준으로 제작되었습니다.

1. install packages
```
$ yum install epel-release yum-utils
$ yum install python3
$ yum install git
$ yum install gcc
$ yum install nginx
$ yum install certbot 
$ yum install python3-certbot-nginx
$ dnf install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-8-x86_64/pgdg-redhat-repo-latest.noarch.rpm
$ dnf -qy module disable postgresql
$ dnf install -y postgresql12-server
$ /usr/pgsql-12/bin/postgresql-12-setup initdb
$ systemctl enable postgresql-12
$ systemctl start postgresql-12
```

2. database 설정

humin에서 사용할 database와 접속할 user를 생성합니다.

```
$ su postgres
$ psql -U postgres
# create user humansacpe password 'PASSWORD';
# create database humin owner humanscape;
```

생성한 user로 접속하기 위해 설정파일을 수정합니다.
```
$ vi /var/lib/pgsql/12/data/pg_hba.conf
```

설정파일의 "host all 127.0.0.1/32 ident" 부분을 "md5"로 수정합니다.
```
host    all             all             127.0.0.1/32            md5
```

서비스를 재시작합니다.
```
$ systemctl restart postgresql-12
```

3. repo clone
```
$ git clone https://github.com/humanscape/humin-server.git
```

4. python3 가상환경 생성 및 활성화
```
$ python3 -m venv .venv
$ source .venv/bin/activate
```

5. python3 라이브러리 설치
```
$ pip install -r requirements.txt
```

6. env파일 설정

프로젝트의 env/.env파일을 생성하고, 아래와 같은 정보를 입력합니다.

(대괄호 속 내용은 사용자의 설정에 맞춰 입력합니다.)
```
# .env
DJANGO_DATABASE_ENGINE=django.db.backends.postgresql
DJANGO_DATABASE_USER=humanscape
DJANGO_DATABASE_PASSWORD={DB_PASSWORD}
DJANGO_DATABASE_HOST=127.0.0.1
DJANGO_DATABASE_PORT=5432
DJANGO_DATABASE_NAME=humim
DJANGO_SECRET_KEY={RANDOM_STRING}
```

google api token파일을 프로젝트의 env/token.json 파일로 저장합니다.

7. migrate

프로젝트 경로에서 migrate를 실행합니다.
```
$ python manage.py migrate
```

8. data insert

humin 구동에 필요한 데이터 users_user, events_room의 데이터를 import합니다.

9. Nginx 설정

Nginx에 SSL 설정을 추가합니다.

Diffie-Hellman Key 생성
```
$ openssl dhparam -out /etc/nginx/conf.d/ssl-dhparams.pem 4096
```

ssl key 변경

/etc/letsencrypt에서 해당 명령어를 실행합니다.
```
$ mv ssl-dhparams.pem  ssl-dhparams.pem.letsencrypt
$ cp -rp /etc/nginx/conf.d/ssl-dhparams.pem /etc/letsencrypt/
```

/etc/nginx/nginx.conf 파일 수정

```conf

#user  nobody;
worker_processes  1;

#error_log  logs/error.log;
#error_log  logs/error.log  notice;
#error_log  logs/error.log  info;

#pid        logs/nginx.pid;


events {
    worker_connections  1024;
}


http {
        upstream django {
                server unix:/run/uwsgi/humin.sock;
        }
    include       mime.types;
    default_type  application/octet-stream;

    #log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
    #                  '$status $body_bytes_sent "$http_referer" '
    #                  '"$http_user_agent" "$http_x_forwarded_for"';

    #access_log  logs/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    #keepalive_timeout  0;
    keepalive_timeout  65;

    #gzip  on;

    include /etc/nginx/conf.d/*.conf;

    server {
        server_name  humin.humanscape.io;

        #charset koi8-r;

        #access_log  logs/host.access.log  main;

        location / {
            root   html;
            index  index.html index.htm;
        }

        location /api {
                uwsgi_pass django;
                include /etc/nginx/uwsgi_params;
        }

        #error_page  404              /404.html;

        # redirect server error pages to the static page /50x.html
        #
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }

    listen 443 ssl http2; # managed by Certbot
    add_header Strict-Transport-Security "max-age=63072000; includeSubdomains; preload";
    ssl_certificate /etc/letsencrypt/live/humin.humanscape.io/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/humin.humanscape.io/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

   }
}
```

/etc/letsencrypt/options-ssl-nginx.conf 파일 수정
```conf
# This file contains important security parameters. If you modify this file
# manually, Certbot will be unable to automatically provide future security
# updates. Instead, Certbot will print and log an error message with a path to
# the up-to-date file that you will need to refer to when manually updating
# this file.

ssl_session_cache shared:le_nginx_SSL:10m;
ssl_session_timeout 1440m;
ssl_session_tickets off;

ssl_protocols TLSv1.2 TLSv1.3;

ssl_stapling on;
ssl_stapling_verify on;
ssl_prefer_server_ciphers on;
ssl_ciphers "ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES256-SHA384:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA:ECDHE-RSA-AES256-SHA:DHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA:DHE-RSA-AES256-SHA256:DHE-RSA-AES256-SHA:ECDHE-ECDSA-DES-CBC3-SHA:ECDHE-RSA-DES-CBC3-SHA:EDH-RSA-DES-CBC3-SHA:AES128-GCM-SHA256:AES256-GCM-SHA384:AES128-SHA256:AES256-SHA256:AES128-SHA:AES256-SHA:DES-CBC3-SHA:!DSS";


# ssl_prefer_server_ciphers off;

# ssl_ciphers "ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384";
```


10. Nginx 연동

nginx와 연동하기 위한 humin.ini파일을 /etc/uwsgi/sites 경로에 생성합니다.

(대괄호 속 내용은 사용자의 설정에 맞춰 입력합니다.)
uwsgi
```conf
[uwsgi]
chdir = {PROJECT_PWD}
module = reservationroom.wsgi
home = {PROJECT_PWD}/.venv

master = true
processes = 10
logto = /var/log/uwsgi/@(exec://date +%%Y-%%m-%%d).log
log-reopen = true

socket = /run/uwsgi/humin.sock
chmod-socket = 666
vacuum = true
```

/etc/systemd/system/uwsgi.service 파일을 아래와 같이 생성합니다.
```conf
[Unit]
Description=uWSGI service

[Service]
ExecStartPre=/bin/mkdir -p /run/uwsgi
ExecStartPre=/bin/chown root:nginx /run/uwsgi
ExecStart={PROJECT_PWD}/.venv/bin/uwsgi --emperor /etc/uwsgi/sites
Restart=always
Type=notify
NotifyAccess=all

[Install]
WantedBy=multi-user.target
```