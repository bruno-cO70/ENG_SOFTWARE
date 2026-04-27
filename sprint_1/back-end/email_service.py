import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv

# Carrega as variáveis seguras do .env
load_dotenv()
EMAIL_ADDRESS = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def enviar_email_teste(destinatario: str):
    msg = EmailMessage()
    msg['Subject'] = 'HairTime - Teste de Notificação 🎉'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = destinatario
    msg.set_content('Olá! Se você está lendo isso, o serviço de mensageria do HairTime está funcionando perfeitamente! 🚀✂️\n\nEste é um e-mail automático, por favor não responda.')

    try:
        # Conecta ao servidor do Gmail usando conexão segura (SSL)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        return True
    except Exception as e:
        print(f"❌ Erro ao enviar e-mail: {e}")
        return False

def enviar_email_confirmacao(destinatario: str, nome_cliente: str, data: str, horario: str):
    msg = EmailMessage()
    msg['Subject'] = 'HairTime - Horário Confirmado! ✂️'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = destinatario
    
    corpo_email = f"""
    Olá, {nome_cliente}!
    
    Seu agendamento no HairTime foi confirmado com sucesso.
    
    📅 Data: {data}
    ⏰ Horário: {horario}
    
    Agradecemos a preferência e te esperamos na hora marcada!
    
    Atenciosamente,
    Equipe HairTime
    """
    msg.set_content(corpo_email)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        return True
    except Exception as e:
        print(f"❌ Erro ao enviar e-mail de confirmação: {e}")
        return False

def enviar_email_remarcacao(destinatario: str, nome_cliente: str, nova_data: str, novo_horario: str):
    msg = EmailMessage()
    msg['Subject'] = 'HairTime - Horário Remarcado! 🔄'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = destinatario
    
    corpo_email = f"""
    Olá, {nome_cliente}!
    
    Seu agendamento no HairTime foi REMARCADO com sucesso.
    
    📅 Nova Data: {nova_data}
    ⏰ Novo Horário: {novo_horario}
    
    Atualize sua agenda e te esperamos na nova data marcada!
    
    Atenciosamente,
    Equipe HairTime
    """
    msg.set_content(corpo_email)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        return True
    except Exception as e:
        print(f"❌ Erro ao enviar e-mail de remarcação: {e}")
        return False