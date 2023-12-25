from typing import List

from fastapi import Depends
from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from database.orm import ToDo, User
from database.connection import get_db

class ToDoRepository:
    def __init__(self, session: Session = Depends(get_db)): # get_db가 Dendency Injection으로 적용이 되어 있고 FastAPI가 DI를 재귀호출해서 걸려있는 의존성 호출 
        self.session = session
        
    # 전체 조회
    def get_todos(self) -> List[ToDo]:  # get_todos 함수는 ToDo를 List에 담아서 리턴한다고 타이핑 적용
        return list(self.session.scalars(select(ToDo)))  # 전체 Todo를 조회해서 리턴

    # 단일 조회
    def get_todo_by_todo_id(self, todo_id: int) -> ToDo | None:    # session을 인자 아이디로 전달 받고 todo_id를 조회에 사용. todo_id 에 해당하는 Todo가 존재하지 않을 때는 None 리턴
        return self.session.scalar(select(ToDo).where(ToDo.id == todo_id))   # ToDo의 id와 전달받은 todo_id와 같은 지. 

    # 생성
    def create_todo(self, todo: ToDo) -> ToDo:   # 생성한 ORM 객체 todo를 전달 받음
        # SQLAlchemy를 통해서 데이터를 저장하는 방법
        self.session.add(instance=todo)   # session Object에 todo 인스턴스 추가
        self.session.commit()    # 이 시점에서 데이터베이스에 저장 (이 때 todo_id 값도 할당)
        self.session.refresh(instance=todo)   # todo 인스턴스를 한 번 더 데이터베이스로 읽어옴(todo_id 까지 읽어오기 위해)
        return todo # 다시 읽어 온 todo 리턴

    # 수정
    def update_todo(self, todo: ToDo) -> ToDo:
        self.session.add(instance=todo)   
        self.session.commit()  # db save
        self.session.refresh(instance=todo)  
        return todo

    # 삭제
    def delete_todo(self, todo_id: int) -> None:  # 삭제 후 None 리턴
        self.session.execute(delete(ToDo).where(ToDo.id == todo_id)) # ToDo 테이블에 todo_id 와 일치하는 id를 찾아서 삭제
        self.session.commit()


class UserRepository:
    def __init__(self, session: Session = Depends(get_db)): 
        self.session = session

    def get_user_by_username(self, username: str) -> User | None:  # scalar에서 조건에 만족하는 유저가 있으면 리턴하고 없으면 None 리턴
        return self.session.scalar(
            select(User).where(User.username == username)
        )

    def save_user(self, user: User) -> User:
        self.session.add(instance=user)   
        self.session.commit()  # db save
        self.session.refresh(instance=user)  
        return user

