import smtplib
from email.mime.text import MIMEText

nadawca = input("Podaj adres nadawcy: ")
odbiorcy = input("Podaj adres(y) odbiorców (oddziel przecinkami): ").split(',')
temat = input("Podaj temat wiadomości: ")
tresc = input("Podaj treść wiadomości: ")

msg = MIMEText(tresc)
msg['Subject'] = temat
msg['From'] = nadawca
msg['To'] = ', '.join(odbiorcy)

try:
    with smtplib.SMTP('localhost', 587) as serwer:
        serwer.starttls()
        serwer.ehlo()

        serwer.sendmail(nadawca, odbiorcy, msg.as_string())
        print("Wiadomość została pomyślnie wysłana!")

except Exception as e:
    print(f"Błąd podczas wysyłania wiadomości: {str(e)}")