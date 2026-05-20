import smtplib
from email.message import EmailMessage
from abc import ABC, abstractmethod
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


class EmailServiceImpl:
    def __init__(self, email_address: str = EMAIL_ADDRESS, email_password: str = EMAIL_PASSWORD):
        self.email_address = email_address
        self.email_password = email_password

    def send_confirmation(self, destinatario: str, nome_cliente: str, data: str, horario: str) -> bool:
        msg = EmailMessage()
        msg['Subject'] = 'HairTime - Horário Confirmado! ✂️'
        msg['From'] = self.email_address
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

        return self._send_email(msg)

    def send_rescheduling(self, destinatario: str, nome_cliente: str, nova_data: str, novo_horario: str) -> bool:
        msg = EmailMessage()
        msg['Subject'] = 'HairTime - Horário Remarcado! 🔄'
        msg['From'] = self.email_address
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

        return self._send_email(msg)

    def send_test(self, destinatario: str) -> bool:
        msg = EmailMessage()
        msg['Subject'] = 'HairTime - Teste de Notificação 🎉'
        msg['From'] = self.email_address
        msg['To'] = destinatario
        msg.set_content('Olá! Se você está lendo isso, o serviço de mensageria do HairTime está funcionando perfeitamente! 🚀✂️\n\nEste é um e-mail automático, por favor não responda.')

        return self._send_email(msg)

    def _send_email(self, msg: EmailMessage) -> bool:
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(self.email_address, self.email_password)
                smtp.send_message(msg)
            return True
        except Exception as e:
            print(f"❌ Erro ao enviar e-mail: {e}")
            return False
