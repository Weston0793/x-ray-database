import streamlit as st

def main():
    st.title("Üdvözöljük az Orvosi Röntgenkép Adatbázisban!")

    st.markdown("""
    ### Az alkalmazás célja
    Az alkalmazás célja, hogy segítse az orvosi röntgenképek kezelését, feltöltését, keresését és állapotuk nyomon követését. A rendszer pontos és részletes adatokat gyűjt a röntgenképekről, hogy elősegítse az orvosi kutatást, oktatást valamint legfőképpen a traumatológiai diagnosztikai munkát, ezáltal javítva a betegek ellátását

    ### Funkciók
    - **Kép feltöltése**: Új röntgenkép(ek)et tölthet fel az adatbázisba.
    - **Képek keresése**: Kereshet az adatbázisban található röntgenképek között különböző kritériumok alapján.
    - **Státusz**: Megtekintheti a feltöltött röntgenképek állapotát és statisztikáit.
    - **Elérhetőség**: Kapcsolatba léphet a fejlesztőkkel.

    ### Használati útmutató

    #### 1. Kép feltöltése
    - Kérjük a feltöltésre szánt képekről bizonyosodjon meg hogy anonimizálva vannak! A képeken nem szerepelhet semmilyen betegazonosító!
    - Válassza a bal oldalsáv "Navigáció" menüjéből a "Kép feltöltése" pontot.
    - Húzza a "Drag and drop file here" mezőbe a képet vagy válassza ki a "Browse files" gombbal s töltse fel a röntgenkép(ek)et (Max 15 MB/file).
    - **Több kép feltöltése**: Ha egyszerre több képet szeretne feltölteni, pipálja ki a "Több kép feltöltése" lehetőséget. Figyelem: az összes kép ugyanazokat a címkéket kapja! (kivéve a betegazonosítót)
    - Kérem, adja meg a kötelező adatokat: korcsoport, röntgen nézet, normál vagy elváltozás típusa, melyik oldal (ha végtagról van szó), és a sérült régiók (fő régió, régió).
    - A részletesebb adatmegadás (alrégiók, komplikációk, társuló állapotok, osztályozások) nagyban segíti a kutatást és diagnosztikát.
    - **Több régió jelölése**: Ha több sérült régiót szeretne megadni, pipálja ki a "Több régió jelölése" opciót. Fontos: új régió hozzáadására csak mentés után van lehetőség, jelenlegi technikai korlátok miatt. Ha mentés nélkül több új régiót hozzáad, hibaüzenet fog keletkezni!
    - A választható súlyossági kategóriák folyamatosan bővülnek. A hosszú csöves csontoknál már elérhető a teljes AO klasszifikáció (a boka kívételével).
    - Kattintson a "Feltöltés" gombra a kíválasztott adatok újra összegzéséhez, majd a "Megerősítés és Feltöltés" gombbal véglegesítheti a feltöltést.
    - Kérjük várja meg a zöld "Sikeres feltöltés" feliratot mielött új képet tölt fel. Több kép feltöltésénél egyszerre, többet kell várni.

    #### 2. Képek keresése
    - Válassza a "Képek keresése" menüpontot a bal oldalsáv "Navigáció" menüjéből.
    - Adja meg a keresési feltételeket (minimum: típus, nézet, főrégió).
    - Kattintson a "Keresés" gombra. A találatok listája megtekinthető és letölthető. 
    - Várjon egy pár másodpercet amíg a szerver összeállítja a "Letöltés" gomb megnyomása után a .zip filet, majd kattintson a "Megerősítés s Letöltés" gombra ha le kívánja tölteni a képeket és a hozzájuk tartozó címkéket. 

    #### 3. Státusz
    - Válassza a "Státusz" menüpontot a bal oldalsáv "Navigáció" menüjéből.
    - Tekintse meg a feltöltött röntgenképek statisztikáit és a projekt aktuális fázisának állapotát.
    - Az adatok alapján nyomon követheti a projekt előrehaladását és a hiányzó elemeket.
    - Az első fázis lezárási kirétirumai: az összes különböző csontot tartalmazó régióból, legalább két nézetből, normál és törött röntgenképeket gyüjts felnőttektől, kombinációnként legalább 50 darabot.
    - A második fázis a különböző alrégiók feltöltése lesz előreláhatólag.
    - Fontos: egyelőre a státusz a gyermekkori röntgeneket is számba veszi!

    #### 4. Elérhetőség
    - Válassza az "Elérhetőség" menüpontot a bal oldalsáv "Navigáció" menüjéből.
    - Ha bármilyen észrevétele van a honlappal kapcsolatban, segítségre van szüksége vagy kérdése van, lépjen nyugodtan kapcsolatba a fejlesztőkkel.

    ### Fontos Információk
    - **Adatbiztonság**: Az összes feltöltött adat biztonságos és titkosított környezetben kerül tárolásra.
    - **Frissítések és Karbantartás**: Az alkalmazás rendszeresen frissül, hogy biztosítsa a legújabb és egyre kényelmesebb funkciók és várják az ide látogatókat.

    Köszönjük, hogy használja az alkalmazásunkat!
    """)

if __name__ == "__main__":
    main()
