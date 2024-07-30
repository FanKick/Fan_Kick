# 베이스 이미지를 Python 3.10.13으로 설정합니다.
FROM python:3.10.12-slim

# 작업 디렉토리를 설정합니다.
WORKDIR /app

# 로컬의 requirements.txt 파일을 컨테이너의 /app 디렉토리로 복사합니다.
COPY requirements.txt /app/

# requirements.txt에 정의된 패키지를 설치합니다.
RUN pip install --no-cache-dir -r requirements.txt

# 로컬의 프로젝트 파일을 컨테이너의 /app 디렉토리로 복사합니다.
COPY . /app/

# Django 애플리케이션의 진입점을 설정합니다.
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]

# 8000 포트를 열어줍니다.
EXPOSE 8000
