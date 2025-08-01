from fastapi import APIRouter, HTTPException, status, Depends
from schema import SignupModel, Settings, LoginModel
from database import Session, Base, engine
from model import User
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import bcrypt
from sqlalchemy.exc import IntegrityError
from fastapi_jwt_auth import AuthJWT

auth_router = APIRouter(prefix="/auth", tags=['authentication routes'])

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
        password_bytes = payload.password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password_bytes, salt)
    
        new_user = User(
            username=payload.username,
            email=payload.email,
            password=hashed_password.decode('utf-8')
        )
        session.add(new_user)
        session.commit()
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


@auth_router.post('/login')
async def Login(payload: LoginModel, Authorize: AuthJWT=Depends()):
    session = Session(bind=engine)
    try:
        user = session.query(User).filter(User.email == payload.email).first()
        if user is None:
            raise HTTPException(status_code=400, detail="No such user found, Signup to create one!")
        
        # Check if password matches the hashed password
        password_bytes = payload.password.encode('utf-8')
        if not bcrypt.checkpw(password_bytes, user.password.encode('utf-8')):
            raise HTTPException(status_code=400, detail="Invalid password!")
        
        create_access_token=Authorize.create_access_token(subject=user.email)
        refresh_access_token = Authorize.create_refresh_token(subject=user.email)

        response = {
            "access_tokens": create_access_token,
            "refresh_tokens": refresh_access_token
        }
        return JSONResponse(status_code=status.HTTP_200_OK, content=response)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )
    finally:
        session.close()


