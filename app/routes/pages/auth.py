"""
Routes pour l'authentification (inscription, connexion, reset password)
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["auth"])
templates = Jinja2Templates(directory="templates")


@router.get("/inscription", response_class=HTMLResponse)
async def inscription(request: Request):
    """Page d'inscription"""
    return templates.TemplateResponse("auth/inscription.html", {"request": request})


@router.get("/connexion", response_class=HTMLResponse)
async def connexion(request: Request):
    """Page de connexion"""
    return templates.TemplateResponse("auth/connexion.html", {"request": request})


@router.get("/reset-password", response_class=HTMLResponse)
async def reset_password(request: Request):
    """Page de demande de réinitialisation du mot de passe"""
    return templates.TemplateResponse("auth/reset-password.html", {"request": request})


@router.get("/new-password", response_class=HTMLResponse)
async def new_password(request: Request):
    """Page de création d'un nouveau mot de passe"""
    return templates.TemplateResponse("auth/new-password.html", {"request": request})
