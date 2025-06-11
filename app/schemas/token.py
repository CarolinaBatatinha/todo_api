from datetime import datetime
from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class TokenBase(BaseModel):
    # Esquema base para tokens
    token_type: str = Field(default='bearer', example='bearer')

class TokenCreate(TokenBase):
    # Esquema para criação de token (resposta de login)
    access_token: str = Field(
        ...,
        example='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyQGV4YW1wbGUuY29tIiwiZXhwIjoxNjMyNTkwODAwfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'
    )
    refresh_token: Optional[str] = Field(
        None,
        example='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyQGV4YW1wbGUuY29tIiwiZXhwIjoxNjMyNTkwODAwfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'
    )

class TokenPayload(BaseModel):
    # Esquema para o payload do token JWT
    sub: Optional[EmailStr] = Field(None, example='user@example.com')
    exp: Optional[datetime] = Field(None, example=1632590800)
    iat: Optional[datetime] = Field(None, example=1632587200)
    jti: Optional[str] = Field(None, example='7f6a127d-8a3c-4a5e-b2d1-3e5f6a127d8a')

class Token(TokenBase):
    # Esquema para resposta de token
    access_token: str
    expires_in: Optional[int] = Field(None, example=3600)

class RefreshTokenRequest(BaseModel):
    # Esquema para requisição de refresh token
    refresh_token: str = Field(
        ...,
        example='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyQGV4YW1wbGUuY29tIiwiZXhwIjoxNjMyNTkwODAwfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'
    )

class TokenData(BaseModel):
    # Esquema para dados do token decodificado
    email: Optional[EmailStr] = None
    user_id: Optional[int] = None

# Alias para compatibilidade com o OAuth2
TokenResponse = TokenCreate
