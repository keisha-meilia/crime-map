import jwt
import psycopg

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from ..database import get_conn
from ..schemas import LoginIn, RegisterIn, TokenOut, UserOut
from ..security import (
    create_token,
    decode_token,
    hash_password,
    verify_password,
)


router = APIRouter(prefix="/auth", tags=["auth"])
bearer = HTTPBearer()


def get_current_user(
    cred: HTTPAuthorizationCredentials = Depends(bearer),
) -> UserOut:
    try:
        payload = decode_token(cred.credentials)
        user_id = int(payload["sub"])

    except (jwt.PyJWTError, KeyError, ValueError):
        raise HTTPException(
            status_code=401,
            detail="Token tidak valid atau kedaluwarsa"
        )

    with get_conn() as conn:
        row = conn.execute(
            "SELECT id, nama, email FROM users WHERE id = %s",
            (user_id,)
        ).fetchone()

    if row is None:
        raise HTTPException(
            status_code=401,
            detail="Pengguna tidak ditemukan"
        )

    return UserOut(
        id=row[0],
        nama=row[1],
        email=row[2]
    )


@router.post("/register", response_model=TokenOut, status_code=201)
def register(data: RegisterIn):
    email = data.email.lower()
    nama = data.nama.strip()
    hashed = hash_password(data.password)

    try:
        with get_conn() as conn:
            row = conn.execute(
                "INSERT INTO users (nama, email, password_hash) "
                "VALUES (%s, %s, %s) RETURNING id",
                (nama, email, hashed),
            ).fetchone()

    except psycopg.errors.UniqueViolation:
        raise HTTPException(
            status_code=409,
            detail="Email sudah terdaftar"
        )

    user = UserOut(
        id=row[0],
        nama=nama,
        email=email
    )

    return TokenOut(
        access_token=create_token(user.id),
        user=user
    )


@router.post("/login", response_model=TokenOut)
def login(data: LoginIn):
    email = data.email.lower()

    with get_conn() as conn:
        row = conn.execute(
            "SELECT id, nama, email, password_hash FROM users WHERE email = %s",
            (email,),
        ).fetchone()

    if row is None or not verify_password(data.password, row[3]):
        raise HTTPException(
            status_code=401,
            detail="Email atau password salah"
        )

    user = UserOut(
        id=row[0],
        nama=row[1],
        email=row[2]
    )

    return TokenOut(
        access_token=create_token(user.id),
        user=user
    )


@router.get("/me", response_model=UserOut)
def me(user: UserOut = Depends(get_current_user)):
    return user