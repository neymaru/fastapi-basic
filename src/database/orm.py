from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

from schema.request import CreateToDoRequest

# Base 클래스 생성
Base = declarative_base()   

# Base 클래스를 상속받아서 데이터베이스 테이블을 특정 클래스로 모델링
class ToDo(Base):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True, index=True)
    contents = Column(String(256), nullable=False)
    is_done = Column(Boolean, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"))

    # 파이썬의 __repr__이라는 메소드를 오버라이딩 해서 어떤 ToDo 객체가 출력 되는지 확인용
    def __repr__(self):
        return f"ToDo(id={self.id}, contents={self.contents} is_done={self.is_done})"
    
    # ORM 객체로 먼저 변환
    @classmethod
    def create(cls, request: CreateToDoRequest) -> "ToDo":    # request를 그대로 전달 받아서 여기에 맞는 데이터 매핑
        return cls(
            contents=request.contents,
            is_done=request.is_done,
        )
    
    # 인스턴스 메소드를 정의해서 데이터를 업데이트 하는 부분을 관리하는 이유는 유지보수가 편하기 때문
    def done(self) -> "ToDo":
        self.if_done = True
        return self
    
    def undone(self) -> "ToDo":
        self.if_done = False
        return self

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(256), nullable=False)
    password = Column(String(256), nullable=False)
    todos = relationship("ToDo", lazy="joined")    # 어떤 클래스와 연결을 할 지
    # todos 속성은 실제로 컬럼이 생성되는 건 아니고 가상의 relationship
    # User가 조회되는 시점에 todos를 함께 JOIN 해와서 User.todos 로 todo 데이터를 사용 가능

    @classmethod
    def create(cls, username: str, hashed_password: str) -> "User":
        return cls(
            username=username,
            password=hashed_password,
        )
    