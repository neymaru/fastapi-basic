import bcrypt

class UserService:
    encoding: str = "UTF-8"

    def hash_password(self, plain_password: str) -> str:    # 플레인 패스워드를 strng으로 받아서 해시된 형태의 string 반환
        hashed_password: bytes = bcrypt.hashpw(
            plain_password.encode(self.encoding), 
            salt=bcrypt.gensalt()
        )
        return hashed_password.decode(self.encoding)  # hashed_password를 decode 해서 return
