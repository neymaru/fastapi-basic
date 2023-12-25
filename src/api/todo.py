from typing import List
from fastapi import Body, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from database.connection import get_db
from database.orm import ToDo, User
from database.repository import ToDoRepository, UserRepository
from schema.response import ToDoListSchema, ToDoSchema
from schema.request import CreateToDoRequest
from security import get_access_token
from service.user import UserService

router = APIRouter(prefix="/todos")

# ---------- 조회 ------------
## 전체 조회
@router.get("", status_code=200)
def get_todos_handler(
    access_token: str = Depends(get_access_token), # api가 호출 될 때마다 get_access_token이라는 dependency가 먼저 호출
    order: str | None = None,
    user_service: UserService = Depends(),
    user_repo: UserRepository =  Depends(),
) -> ToDoListSchema: 
    
    username: str = user_service.decode_jwt(access_token=access_token)  # 앞으로 이 username을 통해서 user 조회

    user: User | None = user_repo.get_user_by_username(username=username)
    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")
    
    todos: List[ToDo] = user.todos
    if order and order == "DESC":   # order 값이 있고 oder 값이 "DESC" 이라면
        return ToDoListSchema(
            todos=[ToDoSchema.from_orm(todo) for todo in todos[::-1]] 
        )
    return ToDoListSchema(
        todos=[ToDoSchema.from_orm(todo) for todo in todos] 
        # todos를 순회하면서 todo 하나를 from_orm에 전달해주고 ToDoSchema가 계속 생성 되면서 todos에 리스트 형태로 담기게 된다.
        # 즉 앞서 가져왔던 todos 데이터를 ToDoSchema로 바꿔서 리턴한다.
    )

## 단일 조회
@router.get("/{todo_id}", status_code=200)
def get_todo_handler(
    todo_id: int,
    todo_repo: ToDoRepository = Depends(), 
    ) -> ToDoSchema:
    todo: ToDo | None = todo_id.get_todo_by_todo_id(todo_id=todo_id)
    if todo:
        return ToDoSchema.from_orm(todo)
    raise HTTPException(status_code=404, detail="Todo Not Found")   # 잘못된 todo_id로 조회한 경우, 404에러 발생, 메시지

# ---------- 생성 ------------- 
# todo 아이템들이 갖는 형태와 동일한 스키마로 request 클래스 만들기
@router.post("", status_code=201)
def create_todo_handler(
    request: CreateToDoRequest, # request에 CreateToDoRequest를 입력하면 FastAPI가 알아서 create_todo_handler에 넣어서 처리
    todo_repo: ToDoRepository = Depends(), 
    ) -> ToDoSchema:    
    # ORM 객체를 생성하는 부분
    todo: ToDo = ToDo.create(request=request)   # ToDo 클래스의 create 메서드에 request를 전달해서 todo에 리턴 값 저장 / id=None
    # 레퍼지토리 코드를 추가 해서 데이터베이스에 데이터를 저장하는 부분을 호출
    todo: ToDo = todo_repo.create_todo(todo=todo)    # session을 통해서 todo가 데이터베이스에 저장 되고 refresh 된 todo(id 할당)가 변수에 할당
    return ToDoSchema.from_orm(todo)    # 최신 todo가 응답으로 반환

# ---------- 수정 -------------
@router.patch("/{todo_id}", status_code=200)
def update_todo_handler(
    todo_id: int,
    is_done: bool = Body(..., embed=True),  # FastAPI에서 하나의 컬럼값은 request body를 읽어서 사용할 수 있게 됨
    todo_repo: ToDoRepository = Depends(), 
):
    todo: ToDo | None = todo_repo.get_todo_by_todo_id(todo_id=todo_id)
    if todo:
        # update
        # if is_done is True:
        #     todo.done()
        # else:
        #     todo.undone()
        todo.done() if is_done else todo.undone()   # 삼항연산자
        # repository 함수로 데이터베이스에 데이터 업데이트
        todo. ToDo = todo_repo.update_todo(todo=todo)
        return ToDoSchema.from_orm(todo)
    raise HTTPException(status_code=404, detail="Todo Not Found")

# ---------- 삭제 ------------
@router.delete("/{todo_id}", status_code=204)    # delete는 기본적으로 상태코드 204(아무것도 리턴하지 않을 때)
def delete_todo_handler(
    todo_id: int,
    todo_repo: ToDoRepository = Depends(), 
):
    todo: ToDo | None = todo_repo.get_todo_by_todo_id(todo_id=todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="ToDo Not Found")
    # delete
    todo_repo.delete_todo(todo_id=todo_id)
    # 204 같은 경우는 응답으로 반환하는 데이터가 없기 때문에 return문을 안적어도 됨