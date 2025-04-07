import ssl
from aiosmtpd.controller import Controller

class CustomHandler:
    async def handle_DATA(self, server, session, envelope):
        print("\n--- Nowa wiadomość ---")
        print(f"Od: {envelope.mail_from}")
        print(f"Do: {envelope.rcpt_tos}")
        print("Treść:")
        print(envelope.content.decode("utf-8", errors="replace"))
        print("----------------------\n")
        return "250 Wiadomość odebrana"

# Konfiguracja SSL
ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.load_cert_chain("cert.pem", "key.pem")

# Uruchom serwer na porcie 587 z obsługą STARTTLS
controller = Controller(
    CustomHandler(),
    hostname="localhost",
    port=587,
    tls_context=ssl_context,
)

if __name__ == "__main__":
    controller.start()
    print("Serwer SMTP działa na localhost:587 (STARTTLS włączone)...")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        controller.stop()