from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://root:test@127.0.0.1:3309/test"

# sqlalchemy를 이용해서 데이터베이스 접속을 위해 engine 생성
engine = create_engine(DATABASE_URL, echo=True) # echo: sqlalchemy에 의해 쿼리가 대신 처리되는데 어떤 sql이 사용됐는지 사용되는 시점에 사용되는 sql을 출력해주는 옵션(실제론 사용하지 않지만 개발 환경에서 디버깅 할 때 확인용)
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine) # 데이터베이스와 통신을 하기 위해 SessionFactory라는 인스턴스 생성
# autocommit, autoFlush 수동
# bind=engine -> 전달한 데이터베이스 URL을 통해서 생성된 engine을 사용해서 Session 만들기 위해


# API 안에서 Session 개체를 이용해서 데이터베이스에 접근하기 위해 Generator 생성
# FastAPI가 session을 처리하는 과정
# 1. FastAPI에서 request가 들어왔을 때 
def get_db():
    session = SessionFactory()  # 2. session이 생성이 돼서 
    try:
        yield session   # 3. yield 문으로 return이 되고 사용이 되다가
    finally:
        session.close() # 4. 응답을 한 이후에 session을 close 해서 삭제

