from typing import List
from pydantic import BaseModel

# ToDoSchema가 SQLAlchemy의 orm 객체를 전달 받아서 정의한 형태에 맘ㅈ게 데이터를 변환하고 최종적으로 리턴
# 굳이 response를 한 번 더 분리하고 정의하는 이유는?
# -> 지금은 구조가 단순하지만 컬럼 간의 연산이 있거나 혹은 이 객체를 중첩된 구조로 변환 한다거나, 
#    특정 값을 제외하고 리턴할 경우와 같은 유지 케이스가 있을 수 있기 때문에
#    객체를 분리 해높으면 훨씬 유연하게 코드를 변경할 수 있다.
class ToDoSchema(BaseModel):
    id: int
    contents: str
    is_done: bool

    # pydantic에서 SQLAlchemy를 바로 읽어줄 수 있도록 하기위한 옵션
    class Config:
        orm_mode = True # pydantic에 정의한 orm_mode 사용 가능 -> ToDoSchema에 SQLAlchemy orm 객체를 던져주면 pydantic이 잘 해석해서 ToDoSchema 속성들에 맞게 변경해줌

# 실제로는 ListToDoResponse을 응답에 활용
class ToDoListSchema(BaseModel):
    todos: List[ToDoSchema] # todos 라는 키로 todo 전체 데이터를 리스트 형태로 담아서 리턴