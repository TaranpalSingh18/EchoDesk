from fastapi import APIRouter, HTTPException, status
from schema import SignupModel
from database import Session, Base, engine
from model import User
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import bcrypt
from sqlalchemy.exc import IntegrityError

auth_router = APIRouter(prefix="/auth")

@auth_router.post('/signup')
async def signup(payload: SignupModel):
    session = Session(bind=engine)
    try:
        existing_user_email = session.query(User).filter(User.email == payload.email).first()
        if existing_user_email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists"
            )
        
        # Check if user with username already exists
        existing_user_username = session.query(User).filter(User.username == payload.username).first()
        if existing_user_username:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this username already exists"
            )
        password_bytes = payload.password.get_secret_value().encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password_bytes, salt)
    
        new_user = User(
            username=payload.username,
            email=payload.email,
            password=hashed_password.decode('utf-8')
        )
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": "User created successfully",
                "username": payload.username,
                "email": payload.email
            }
        )
        
    except IntegrityError as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )
    finally:
        session.close()
