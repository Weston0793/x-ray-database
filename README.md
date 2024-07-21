# Orvosi Röntgenkép Adatbázis

Üdvözöljük az Orvosi Röntgenkép Adatbázis alkalmazásban. Ez az alkalmazás lehetővé teszi orvosi röntgenképek feltöltését, keresését és állapotának nyomon követését. Az alkalmazás célja a röntgenképek gyűjtésének, elemzésének és kezelésének elősegítése, ezáltal támogatva az egészségügyi szakembereket és kutatókat a diagnosztikai és kutatási munkájukban.

Alternatívaként megnézheti az alkalmazás hostolt verzióját itt: [Orvosi Röntgenkép Adatbázis](https://x-ray-database.streamlit.app/).

## Funkciók

### Feltöltés oldal
- **Kép feltöltése és címkézése:** Lehetővé teszi a felhasználók számára röntgenképek feltöltését különböző címkékkel, beleértve a beteg azonosítóját, típusát, nézetét, fő régióját, alrégióját, életkorát és megjegyzéseit.
- **Megerősítési lépés:** A végleges feltöltés előtt a felhasználók áttekinthetik a megadott információkat és megerősíthetik a beküldést.

### Keresés oldal
- **Képek keresése:** Átfogó keresési funkciót biztosít, amely lehetővé teszi képek keresését címkék, típus, nézet, fő régió, alrégió, életkor és társult állapotok alapján.
- **Oldalakra bontott eredmények:** A keresési eredményeket oldalakra bontva jeleníti meg, 10 képet oldalanként, és lehetővé teszi az oldalak közötti könnyű navigációt.
- **Letöltési lehetőség:** A felhasználók letölthetik az összes keresési kritériumnak megfelelő képet egy ZIP fájlban.

### Státusz oldal
- **Státusz követése:** Nyomon követi a képek gyűjtésének előrehaladását és szervezetten jeleníti meg.
- **Előrehaladási sávok:** Megmutatja az egyes fő régiók és alrégiók teljesítési százalékát, numerikus értékekkel és előrehaladási sávokkal a jobb vizualizáció érdekében.
- **Általános előrehaladás:** Megjeleníti az egyes fázisok gyűjtési céljainak teljes előrehaladását.

## Kezdés

### Előfeltételek

- Python 3.7 vagy magasabb
- Streamlit
- Firebase fiók

### Telepítés

1. Klónozza a repozitóriumot:
    ```bash
    git clone https://github.com/Weston0793/x-ray-database.git
    cd x-ray-database
    ```

2. Telepítse a szükséges csomagokat:
    ```bash
    pip install -r requirements.txt
    ```

3. Állítsa be a Firebase-t:
    - Hozzon létre egy Firebase projektet.
    - Állítsa be a Firestore-t és a Firebase Storage-t.
    - Szerezze be a `serviceAccount.json` fájlt, és adja hozzá tartalmát a Streamlit titkokhoz.

4. Adja hozzá a Firebase konfigurációját a `secrets.toml` fájlhoz:
    ```toml
    [firebase]
    type = "service_account"
    project_id = "your_project_id"
    private_key_id = "your_private_key_id"
    private_key = "your_private_key"
    client_email = "your_client_email"
    client_id = "your_client_id"
    auth_uri = "https://accounts.google.com/o/oauth2/auth"
    token_uri = "https://oauth2.googleapis.com/token"
    auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
    client_x509_cert_url = "your_client_x509_cert_url"
    ```

5. Indítsa el az alkalmazást:
    ```bash
    streamlit run app.py
    ```

## Szerzők

- Aba Lőrincz<sup class='superscript'>1,2,3,*</sup>
- Hermann Nudelman<sup class='superscript'>1,3</sup>
- András Kedves<sup class='superscript'>2</sup>
- Gergő Józsa<sup class='superscript'>1,3</sup>

## Kapcsolódó intézmények

1. Thermofiziológia Tanszék, Transzlációs Medicina Intézet, Általános Orvostudományi Kar, Pécsi Tudományegyetem, Szigeti út 12, H7624 Pécs, Magyarország; aba.lorincz@gmail.com (AL)
2. Automatizálási Tanszék, Műszaki és Informatikai Kar, Pécsi Tudományegyetem, Boszorkány út 2, H7624 Pécs, Magyarország
3. Sebészeti, Traumatológiai, Urológiai és Fül-Orr-Gégészeti Osztály, Gyermekgyógyászati Klinika, Klinikai Központ, Pécsi Tudományegyetem, József Attila utca 7, H7623 Pécs, Magyarország

## Kód

A projekt forráskódja elérhető a GitHubon: [GitHub Repository](https://github.com/Weston0793/x-ray-database/)


