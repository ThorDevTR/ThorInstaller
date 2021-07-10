import heroku3
from time import time
import random
import requests
from git import Repo
from thor_installer import *
import os
from .string_yap import stral

def connect (api):
    heroku_conn = heroku3.from_key(api)
    try:
        heroku_conn.apps()
    except:
        hata("Heroku API Key yanlış!")
        exit(1)
    return heroku_conn

def createApp (connect):
    appname = "thor" + str(time() * 1000)[-4:].replace(".", "") + str(random.randint(0,500))
    try:
        ###########Docker için burayı değiştir#############BURADA########################
        connect.create_app(name=appname, stack_id_or_name='cedar', region_id_or_name="us")
    except requests.exceptions.HTTPError:
        hata("(!) Sanırım beşten fazla uygulamanız var. Yeni uygulama oluşturabilmek için bazılarını silmeniz gerekmekte.")
        exit(1)
    return appname

def hgit (connect, repo, appname):
    global api
    app = connect.apps()[appname]
    giturl = app.git_url.replace(
            "https://", "https://api:" + api + "@")

    if "heroku" in repo.remotes:
        remote = repo.remote("heroku")
        remote.set_url(giturl)
    else:
        remote = repo.create_remote("heroku", giturl)
    try:
        remote.push(refspec="HEAD:refs/heads/master", force=True)
    except Exception as e:
        hata("(!) Hata" + str(e))
    return app

if __name__ == "__main__":
    logo()
    api = soru("(?) Heroku API Keyinizi yazın: ")
    bilgi("(i) Heroku'ya giriş yapılıyor...")
    heroku = connect(api)
    basarili("(✓) Giriş başarılı!")

    # Telegram İşlemleri #
    onemli("(i) StringSession alınıyor...\n")
    stri = stral()
    basarili("(✓) StringSession alındı!")
    baslangic = time()

    # Heroku İşlemleri #
    bilgi("(i) Uygulama oluşturuluyor...")
    appname = createApp(heroku)
    basarili("(✓) Uygulama oluşturma başarılı!")
    onemli("(i) ThorUserBot indiriliyor...")

    if os.path.isdir("./thoruserbot/"):
        del_it('./thoruserbot/')
    repo = Repo.clone_from("https://github.com/ThorDevs/ThorUserBot", "./thoruserbot/", branch="main")
    basarili("(✓) ThorUserBot indirildi!")
    onemli("(i) Deploy işlemi başlatılıyor... (Bu İşlem Uzun Sürebilir)")
    app = hgit(heroku, repo, appname)
    config = app.config()

    onemli("(i) Veriler yazılıyor...")

    config['ENV'] = 'thor'
    config['API_ID'] = '4150176' #TODO: Bu değer otomatik alınsın.
    config['API_HASH'] = 'cc60c01e601ee9cd77fe5ec6a6129882' #TODO: Bu değer otomatik alınsın.
    config['STRING_SESSION'] = stri
    config['SESSION_ADI'] = 'ThorUserBot'
    config['HEROKU_APIKEY'] = api
    config['HEROKU_APPNAME'] = appname


    basarili("(✓) Veriler yazıldı!")
    bilgi('(i) Dyno açılıyor...')

    try:
        app.process_formation()["worker"].scale(1)
    except:
        hata("(!) Dosyalar yüklenirken bir hata oluştu. Lütfen tekrar deneyin.")
        exit(1)

    basarili("(✓) Dynolar açıldı!")
    basarili("(✓) Deploy işlemi başarılı!")
    tamamlandi(time() - baslangic)