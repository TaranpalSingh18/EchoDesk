from fastapi import APIRouter, Depends
from model import SessionDatabase
from schema import SessionModel
from fastapi_jwt_auth import AuthJWT
from fastapi.exceptions import HTTPException
from database import Session,engine
from fastapi.responses import JSONResponse

session_router = APIRouter(prefix="/session", tags=["Used for working with sessions"])
session = Session(bind=engine)

@session_router.get('/')
async def authorization(Authorize: AuthJWT=Depends()):
    try:
        AuthJWT.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=400, detail="Unauthorised Access")


@session_router.get('/all')
async def get_all_sessions(meeting_url:str,Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=400, detail="Unauthorised Access")
    
    lists=[]

    user = session.query(SessionDatabase).filter(SessionDatabase.meeting_url==meeting_url).all()
    if not user:
        raise HTTPException(status_code=404, detail="No Meeting Links Found! Create One")
    else:
        lists.append(user)
    
    return JSONResponse(lists)

@session_router.post('/create')
async def create_session(payload: SessionModel, Authorize: AuthJWT=Depends()):

    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=400, detail="Unauthorised Access")
    
    default_session = session.query(SessionDatabase).filter(payload.meeting_url == SessionDatabase.meeting_url).first()

    if default_session is not None:
        raise HTTPException(status_code=404, detail="Session Already Found")
    
    else:
        new_session = SessionModel(
            session_id=payload.session_id,
            meeting_url=payload.meeting_url,
            start_time=payload.start_time,
            status=payload.status
        )
        session.add(new_session)
        session.commit()

        return {"message":"Session Created Successfully"}





    


    
    