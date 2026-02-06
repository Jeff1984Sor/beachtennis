from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.core.deps import get_current_user
from app.schemas.branding import EmpresaConfigOut, EmpresaConfigUpdate
from app.services.branding_service import get_empresa_config, ensure_empresa_config, update_empresa_config
from app.services.media_service import save_upload, file_path
from app.models.media_file import MediaFile
from app.models.enums import OwnerType
from app.core.config import settings

router = APIRouter()


@router.get("/public/branding", response_model=EmpresaConfigOut)
async def public_branding(session: AsyncSession = Depends(get_session)) -> EmpresaConfigOut:
    config = await ensure_empresa_config(session)
    logo_url = None
    if config.logo_media_id:
        logo_url = f"{settings.public_base_url}/public/logo"
    return EmpresaConfigOut(
        id=config.id,
        nome_empresa=config.nome_empresa,
        tema=config.tema,
        fonte=config.fonte,
        logo_media_id=config.logo_media_id,
        logo_url=logo_url,
        created_at=config.created_at,
        updated_at=config.updated_at,
    )


@router.get("/public/logo")
async def public_logo(session: AsyncSession = Depends(get_session)):
    config = await ensure_empresa_config(session)
    if not config.logo_media_id:
        return {"detail": "logo nao configurado"}
    result = await session.execute(select(MediaFile).where(MediaFile.id == config.logo_media_id))
    media = result.scalar_one_or_none()
    if not media:
        return {"detail": "logo nao configurado"}
    path = file_path(media)
    if not path.exists():
        return {"detail": "logo nao configurado"}
    return FileResponse(path)


@router.get("/config/branding", response_model=EmpresaConfigOut)
async def get_branding(session: AsyncSession = Depends(get_session), user=Depends(get_current_user)) -> EmpresaConfigOut:
    config = await ensure_empresa_config(session)
    logo_url = None
    if config.logo_media_id:
        logo_url = f"{settings.public_base_url}/public/logo"
    return EmpresaConfigOut(
        id=config.id,
        nome_empresa=config.nome_empresa,
        tema=config.tema,
        fonte=config.fonte,
        logo_media_id=config.logo_media_id,
        logo_url=logo_url,
        created_at=config.created_at,
        updated_at=config.updated_at,
    )


@router.put("/config/branding", response_model=EmpresaConfigOut)
async def update_branding(
    payload: EmpresaConfigUpdate,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
) -> EmpresaConfigOut:
    config = await update_empresa_config(session, payload.model_dump(exclude_unset=True))
    logo_url = None
    if config.logo_media_id:
        logo_url = f"{settings.public_base_url}/public/logo"
    return EmpresaConfigOut(
        id=config.id,
        nome_empresa=config.nome_empresa,
        tema=config.tema,
        fonte=config.fonte,
        logo_media_id=config.logo_media_id,
        logo_url=logo_url,
        created_at=config.created_at,
        updated_at=config.updated_at,
    )


@router.post("/config/logo/upload", response_model=EmpresaConfigOut)
async def upload_logo(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
) -> EmpresaConfigOut:
    media = await save_upload(
        session,
        file,
        owner_type=OwnerType.empresa,
        owner_id=None,
        unidade_id=None,
        folder="branding",
        uploaded_by=str(user.id),
    )
    config = await update_empresa_config(session, {"logo_media_id": str(media.id)})
    logo_url = f"{settings.public_base_url}/public/logo"
    return EmpresaConfigOut(
        id=config.id,
        nome_empresa=config.nome_empresa,
        tema=config.tema,
        fonte=config.fonte,
        logo_media_id=config.logo_media_id,
        logo_url=logo_url,
        created_at=config.created_at,
        updated_at=config.updated_at,
    )
