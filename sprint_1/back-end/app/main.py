from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import database
import models
from app.routers import auth_router, servico_router, agendamento_router, cliente_router, profissional_router, relatorio_router
from app.services.email_service_impl import EmailServiceImpl

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="HairTime API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(servico_router.router)
app.include_router(agendamento_router.router)
app.include_router(cliente_router.router)
app.include_router(profissional_router.router)
app.include_router(relatorio_router.router)


@app.post("/api/teste-email")
def testar_envio_de_email(email_destino: str):
    email_service = EmailServiceImpl()
    sucesso = email_service.send_test(email_destino)

    if sucesso:
        return {"message": f"E-mail enviado com sucesso para {email_destino}!"}

    raise HTTPException(status_code=500, detail="Falha ao enviar e-mail. Verifique os logs do terminal.")
