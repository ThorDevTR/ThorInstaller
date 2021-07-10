from pyrogram import Client
from thor_installer import *
from pyrogram.errors import (
    SessionPasswordNeeded, FloodWait,
    PhoneNumberInvalid, ApiIdInvalid,
    PhoneCodeInvalid, PhoneCodeExpired
)
import sys, time

def stral():
    # Original code https://github.com/AbirHasan2005/TG-String-Session/blob/main/genStr.py
    phone = input("\033[96m \nLütfen telefon numaranızı ülke kodu ile birlikte giriniz: ")
    print("\033[00m")
    client = Client(':memory:',api_id="4150176",api_hash="cc60c01e601ee9cd77fe5ec6a6129882",app_version='ThorUserBot',device_model='Thor',system_version='1.0',lang_code='tr',phone_number=phone)
    try:
        client.connect()
    except ConnectionError:
        client.disconnect()
        client.connect()
    try:
        code = client.send_code(phone)
        time.sleep(1)
    except FloodWait as e:
        hata(f"(!) FloodWait Tespit edildi! Lütfen {e.x} saniye sonra tekrar deneyin.")
        sys.exit()
    except PhoneNumberInvalid:
        hata("(!) Geçersiz Bir Numara Girdiniz Örnekte Gibi Giriniz. Örnek: +90xxxxxxxxxx")
        sys.exit()
    otp_code = soru("(?) Lütfen Telegram'dan gelen kodu yazın: ")
    try:
        client.sign_in(phone, code.phone_code_hash, phone_code=' '.join(str(' '.join(str(otp_code)))))
    except PhoneCodeInvalid:
        hata("(!) Kod yanlış. Lütfen tekrar deneyin.")
        sys.exit()
    except PhoneCodeExpired:
        hata("(!) Kodun süresi geçmiş. Lütfen tekrar deneyin.")
        sys.exit()
    except SessionPasswordNeeded:
        bilgi("(i) İki aşamalı doğrulama tespit edildi.")
        two_step_code = soru("(?) Şifrenizi yazınız: ")
        try:
            client.check_password(two_step_code)
        except Exception as e:
            hata(f"(!) Bilinmeyen Hata: {str(e)}")
            sys.exit()
    except Exception as e:
        hata(f"(!) Bilinmeyen Hata: {str(e)}")
        sys.exit()
    sess = client.export_session_string()
    client.disconnect()
    return sess