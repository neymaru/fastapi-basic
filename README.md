# FastAPI 프로젝트 기본 구성

### 포함 내용
프로젝트 구조화<br/>
CRUD<br/>
HTTP Status Code<br/>
Error 처리<br/>
Docker MySQL 컨테이너 실행<br/>
Database Connection<br/>
ORM(sqlalchemy)<br/>
FastAPI Router<br/>
Dependency Injection(의존성 주입)<br/>
Repository Patter(레포지토리 패턴)<br/>
<br/>
  
### 패키지 설치
````
pip install -r requirements.txt
````
### Docker - MySQL 컨테이너 실행
(예시) 
````
docker run -p 3309:3306 -e MYSQL_ROOT_PASSWORD=test -e MYSQL_DATABASE=test -d -v test:/db --name test mysql:8.0<br/>
````


### Docker 컨테이너 확인
````
docker ps
````

### Docker volume 확인
````
docker volume ls
````

### Docker 컨테이너 접속
````
docker exec -it test bash
````

### MySQL 접속(root 유저 사용)
````
mysql -u root -p
````

### FastAPI Swagger UI
http://localhost:8000/docs
![image](https://github.com/neymaru/fastapi-basic/assets/106804514/ad8225cb-fbd6-4d01-9f24-722ba49bcbbe)






