from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

def get_access_token(
        # header에서 HTTPBearer 형태로 오는 엑세스 토큰이 있나 먼저 검증 하고
        auth_header: HTTPAuthorizationCredentials | None = Depends( 
            HTTPBearer(auto_error=False)
        ),
) -> str:
    if auth_header is None: # 없으면 401 에러 발생
        raise HTTPException(
            status_code=401,    
            detail="Not Authorized", 
        )
    # 헤더가 정상적으로 요청이 오면 그 안에 있는 credentials에서 access_token 리턴
    return auth_header.credentials