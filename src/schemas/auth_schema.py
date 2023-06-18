from pydantic import BaseModel

# for jwt return


class AuthWithToken(BaseModel):
    access_token: str
    token_type: str

# for jwt payload


class AuthPayload(BaseModel):
    sub: str
    exp: int
