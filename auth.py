from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from security import hash_password, verify_password, create_token

router = APIRouter(tags=["auth"])

# Usuario fijo SOLO para clase (sin BD)
FAKE_USER = {
    "username": "admin",
    "password_hash": hash_password("ChuckNorris2026")
}

@router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends()):
    if form.username != FAKE_USER["username"]:
        raise HTTPException(status_code=401, detail="Usuario incorrecto")

    if not verify_password(form.password, FAKE_USER["password_hash"]):
        raise HTTPException(status_code=401, detail="Password incorrecto")

    token = create_token(form.username)
    return {"access_token": token, "token_type": "bearer"}