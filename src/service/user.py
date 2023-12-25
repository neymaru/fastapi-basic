import bcrypt
from datetime import datetime, timedelta
from jose import jwt

class UserService:
    encoding: str = "UTF-8"
    secret_key: str = "dedf6de5fab49a4befdf55aea5df0b070c328add76f0429f0852058d031cdd87"
    jwt_algorithm: str = "HS256"    # 웹토큰 생성에 사용되는 알고리즘

    def hash_password(self, plain_password: str) -> str:    # 플레인 패스워드를 strng으로 받아서 해시된 형태의 string 반환
        hashed_password: bytes = bcrypt.hashpw(
            plain_password.encode(self.encoding), 
            salt=bcrypt.gensalt()
        )
        return hashed_password.decode(self.encoding)  # hashed_password를 decode 해서 return
    
    def verify_password(
        self, plain_password: str, hashed_password: str
    ) -> bool:
        return bcrypt.checkpw(
            plain_password.encode(self.encoding),
            hashed_password.encode(self.encoding)
        )
    
    def create_jwt(self, username: str) -> str:
        return jwt.encode(
            {
                "sub": username,    # 원래는 unique한 id
                "exp": datetime.now() + timedelta(days=1),  # 현재 요청한 시간에서 하루 까지 유효
            }, 
            self.secret_key, 
            algorithm=self.jwt_algorithm,
        )
    
    def decode_jwt(self, access_token: str) -> str:
        payload: dict = jwt.decode(
            access_token, self.secret_key, algorithms=[self.jwt_algorithm]
        )

        return payload["sub"]   # payload의 sub값(username)만 사용
