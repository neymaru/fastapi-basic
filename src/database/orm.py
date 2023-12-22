from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import declarative_base

from schema.request import CreateToDoRequest

# Base 클래스 생성
Base = declarative_base()   

# Base 클래스를 상속받아서 데이터베이스 테이블을 특정 클래스로 모델링
class ToDo(Base):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True, index=True)
    contents = Column(String(256), nullable=False)
    is_done = Column(Boolean, nullable=False)

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