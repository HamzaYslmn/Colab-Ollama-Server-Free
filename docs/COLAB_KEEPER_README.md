# Colab Keeper — Kısa Kurulum ve Kullanım

Bu küçük araç Colab oturumlarını otomatik açıp aralıklı olarak `Run all` tetiklemeye çalışır. Amaç: ücretsiz Colab oturumları sıfırlandığında sık tekrar kurulum yapmak zorunda kalmamanıza yardımcı olmak.

Önemli notlar
- Otomatik giriş ve tarayıcı otomasyonu Google/Colab kullanım koşullarına aykırı olabilir; kendi hesabınız ve riskiniz altında kullanın.
- Bu çözüm garantili değildir — Colab arayüzü değişirse küçük ayarlar gerekebilir.

Hazırlık

1. Python 3.10+ ortamında gereksinimleri yükleyin:

```powershell
python -m pip install -r requirements.txt
```

2. Profil dizini ayarlayın (tek seferlik):

- Windows örnek: `C:\colab_profile` gibi bir klasör kullanabilirsiniz.
- `colab_keeper/config.py` içindeki `CHROME_USER_DATA_DIR` değerini düzenleyin veya çevre değişkeni `CHROME_USER_DATA_DIR` atayın.

3. Chrome profiliyle manuel giriş yapın (bir kez):

- Yöntem A (kolay): terminal ile kısa bir sürücü başlatma komutu çalıştırıp Google hesabınızla giriş yapın:

```powershell
python -c "from colab_keeper.driver_manager import get_driver; get_driver(user_data_dir=r'C:\colab_profile', headless=False)"
```

- Yöntem B: Chrome'u `--user-data-dir` parametresi ile elle açın, oturum açın ve Colab'e giriş yapın:

```powershell
"C:\Program Files\Google\Chrome\Application\chrome.exe" --user-data-dir="C:\colab_profile"
```

4. `COLAB_NOTEBOOK_URL` olarak çalıştırmak istediğiniz Colab notebook linkini `colab_keeper/config.py` içinde ayarlayın (veya çevre değişkeni olarak verin).

Çalıştırma

```powershell
python scripts/run_keeper.py
```

Bu script her `INTERVAL_HOURS` saatte bir yeni bir tarayıcı penceresi açıp `NOTEBOOK_URL`'i yüklemeye ve mümkünse `Run all` kısayolunu tetiklemeye çalışır. Oturum açık kalması için periyodik küçük etkileşimler gönderir.

Otomatik kopyalama (12 saatlik döngü)

- `ENABLE_AUTO_COPY` aktifse bot her `COLAB_COPY_INTERVAL_HOURS` saatte bir (varsayılan 12) yeni bir Colab kopyası oluşturup çalıştırmaya çalışır. Bu, Colab'in 12 saate kadar açık kalma sınırlarına karşı yeni bir sayfa açarak kesintiyi azaltmak içindir.
- Kopyalama işlemi: kaynak `COLAB_NOTEBOOK_URL` GitHub/URL üzerinde açılır → "Save a copy in Drive" öğesi tıklanmaya çalışılır → yeni kopya açılır ve `Run all` tetiklenir.
- Arayüz değişiklikleri nedeniyle bu adım her zaman sorunsuz çalışmayabilir; düğme seçimleri gerektiğinde `colab_keeper/colab_controller.py` içinde güncellenmelidir.

Servis/Arka plan çalışma

- Windows için Task Scheduler veya `nssm`/PowerShell kullanarak script'i arka planda çalıştırabilirsiniz.

Geliştirme fikirleri
- Google Drive API ile notebook'u kopyalayıp her döngüde yeni bir kopya açma (isteğe bağlı).
- Colab UI değişikliklerine karşı daha sağlam selector'lar eklenmesi.
