from fastapi import APIRouter, Depends, HTTPException, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import crud, auth, models
from app.dependencies import get_db
from jose import jwt, JWTError, ExpiredSignatureError
import os

IS_DEV = os.getenv("ENV") == "dev"

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/token")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
    response: Response = None
):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token = auth.create_access_token(data={"sub": user.email})
    refresh_token = auth.create_refresh_token(data={"sub": user.email})

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=not IS_DEV,  
        samesite="lax" if IS_DEV else "none",
        max_age=60 * 60 * 24 * auth.REFRESH_TOKEN_EXPIRE_DAYS
    )

    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/refresh", response_model=dict)
def refresh_token(
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Missing refresh token")

    try:
        payload = jwt.decode(refresh_token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token")
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not user.hashed_password:
        raise HTTPException(status_code=401, detail="User not found or invalid")

    new_refresh_token = auth.create_refresh_token(data={"sub": user.email})

    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=not IS_DEV,
        samesite="lax" if IS_DEV else "none",
        max_age=60 * 60 * 24 * auth.REFRESH_TOKEN_EXPIRE_DAYS
    )

    new_access_token = auth.create_access_token(data={"sub": user.email})
    return {
        "access_token": new_access_token,
        "token_type": "bearer",
        "expires_in": auth.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }
@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(
        "refresh_token",
        httponly=True,
        secure=not IS_DEV,
        samesite="lax" if IS_DEV else "none",
    )
    response.status_code = 204
    return response  
