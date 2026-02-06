from fastapi import APIRouter

from app.api.routes.auth import router as auth_router
from app.api.routes.utils import router as utils_router
from app.api.routes.branding import router as branding_router
from app.api.routes.media import router as media_router
from app.api.routes.alunos import router as alunos_router
from app.api.routes.unidades import router as unidades_router
from app.api.routes.planos import router as planos_router
from app.api.routes.profissionais import router as profissionais_router
from app.api.routes.contratos import router as contratos_router
from app.api.routes.comissoes import router as comissoes_router
from app.api.routes.dre import router as dre_router

router = APIRouter()
router.include_router(auth_router, tags=["auth"])
router.include_router(utils_router, tags=["utils"])
router.include_router(branding_router, tags=["branding"])
router.include_router(media_router, tags=["media"])
router.include_router(alunos_router, tags=["alunos"])
router.include_router(unidades_router, tags=["unidades"])
router.include_router(planos_router, tags=["planos"])
router.include_router(profissionais_router, tags=["profissionais"])
router.include_router(contratos_router, tags=["contratos"])
router.include_router(comissoes_router, tags=["comissoes"])
router.include_router(dre_router, tags=["dre"])