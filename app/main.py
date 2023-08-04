# TEE PELI TÄHÄN
import pygame
import itertools
import random


class Seina:
    def __init__(self, x: int, y: int, skaala: int):
        self.x = x
        self.y = y
        self.skaala = skaala

    def vasen_laita(self):
        return self.x

    def oikea_laita(self):
        return self.x + self.skaala

    def ylareuna(self):
        return self.y

    def alareuna(self):
        return self.y + self.skaala


class Kartta:
    def __init__(self):
        self.kartta = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                       [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1],
                       [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1],
                       [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1],
                       [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1],
                       [0, 0, 1, 0, 1, 1, 0, 1, 2, 1, 0, 0, 0, 0, 0, 0, 0],
                       [1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
                       [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1],
                       [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1],
                       [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1],
                       [1, 0, 0, 0, 0, 0, 1, 0, 3, 0, 0, 0, 0, 0, 0, 0, 1],
                       [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

        self.korkeus = len(self.kartta)
        self.leveys = len(self.kartta[0])
        self.skaala = 50
        self.kuvakoko = self.skaala - 1

        self.kielletyt_koordinaatit()

    def kielletyt_koordinaatit(self):
        skaala = self.skaala
        seinat = []
        SEINA = 1
        for y, x in itertools.product(range(self.korkeus), range(self.leveys)):
            ruutu = self.kartta[y][x]
            if ruutu == SEINA:
                seina = Seina(x * skaala, y * skaala, skaala)
                seinat.append(seina)
        self.seinat = seinat


def oliot_kohtaa(liikkuva_olio, olio2):
    def x_arvojoukot_kohtaa():
        if olio2.vasen_laita() <= liikkuva_olio.oikea_laita() <= olio2.oikea_laita():
            return True

        if olio2.vasen_laita() <= liikkuva_olio.vasen_laita() <= olio2.oikea_laita():
            return True

    def y_arvojoukot_kohtaa():
        if olio2.ylareuna() <= liikkuva_olio.alareuna() <= olio2.alareuna():
            return True

        if olio2.ylareuna() <= liikkuva_olio.ylareuna() <= olio2.alareuna():
            return True

    if x_arvojoukot_kohtaa() and y_arvojoukot_kohtaa():
        return True


class Hahmo:
    def __init__(self, kuvanimi: str, kuvakoko: int):
        kuva = pygame.image.load(f'{kuvanimi}.png')
        self.koko = kuvakoko
        self.kuva = pygame.transform.scale(kuva, (self.koko, self.koko))
        self.x = 0
        self.y = 0

    def vasen_laita(self):
        return self.x

    def oikea_laita(self):
        return self.x + self.koko

    def ylareuna(self):
        return self.y

    def alareuna(self):
        return self.y + self.koko


class Robo(Hahmo):
    def __init__(self):
        super().__init__("robo", kartta.skaala - 1)


class Morko(Hahmo):
    def __init__(self):
        super().__init__("hirvio", kartta.skaala)
        self.suunta = "ylos"
        self.osui_roboon = False

    def liikkuu(self):
        if self.suunta == "ylos":
            if self.seina_edessa():
                self.suunta = random.choice(["oikealle", "vasemmalle"])
                return
            self.y -= 2

        elif self.suunta == "alas":
            if self.seina_edessa():
                self.suunta = random.choice(["oikealle", "vasemmalle"])
                return
            self.y += 2

        elif self.suunta == "oikealle":
            if self.seina_edessa():
                self.suunta = random.choice(["alas", "ylos"])
                return
            self.x += 2

        elif self.suunta == "vasemmalle":
            if self.seina_edessa():
                self.suunta = random.choice(["alas", "ylos"])
                return
            self.x -= 2

        if oliot_kohtaa(self, robo):
            self.osui_roboon = True

    def suuntaehto(self, seina: Seina):
        def seina_ei_sivuilla():
            return seina.vasen_laita() != self.oikea_laita() and seina.oikea_laita() != self.vasen_laita()

        def seina_ei_yla_tai_alapuolella():
            return seina.alareuna() != self.ylareuna() and seina.ylareuna() != self.alareuna()

        if self.suunta == "ylos" and seina.alareuna() == self.ylareuna() and seina_ei_sivuilla():
            return True
        elif self.suunta == "alas" and seina.ylareuna() == self.alareuna() and seina_ei_sivuilla():
            return True
        elif self.suunta == "oikealle" and seina.vasen_laita() == self.oikea_laita() and seina_ei_yla_tai_alapuolella():
            return True
        elif (self.suunta == "vasemmalle" and seina.oikea_laita() == self.vasen_laita()
              and seina_ei_yla_tai_alapuolella()):
            return True

    def seina_edessa(self):
        for seina in kartta.seinat:
            if oliot_kohtaa(self, seina) and self.suuntaehto(seina):
                return True


class Kolikot:
    def __init__(self):
        kuva = pygame.image.load('kolikko.png')
        koko = kartta.kuvakoko
        self.kuva = pygame.transform.scale(kuva, (koko, koko))
        self.satunnaiset_kolikot()

    def sallitut_koordinaatit(self):
        skaala = kartta.skaala
        sallitut = []
        POLKU_VIITE = 0
        for y, x in itertools.product(range(kartta.korkeus), range(kartta.leveys)):
            ruutu = kartta.kartta[y][x]
            if ruutu == POLKU_VIITE:
                koordinaatit = {"x": x * skaala, "y": y * skaala}
                sallitut.append(koordinaatit)
        return sallitut

    def satunnaiset_kolikot(self):
        KOLIKKOMAARA = 10
        self.koordinaatit = random.sample(self.sallitut_koordinaatit(), KOLIKKOMAARA)


class Peli:
    def __init__(self):
        pygame.init()

        self.lataa_kuvat()
        self.uusi_peli()

        self.ikkunan_korkeus = kartta.korkeus * kartta.skaala + kartta.skaala
        self.ikkunan_leveys = kartta.leveys * kartta.skaala
        self.naytto = pygame.display.set_mode((self.ikkunan_leveys, self.ikkunan_korkeus))

        self.fontti = pygame.font.SysFont("Arial", 24)
        self.VARI = (102, 0, 102)
        self.NOPEUS = 2

        self.robo = {"x": 0, "y": 0}
        self.suunnat = {"oikealle": {"nappain": pygame.K_RIGHT, "liike": False},
                        "vasemmalle": {"nappain": pygame.K_LEFT, "liike": False},
                        "ylos": {"nappain": pygame.K_UP, "liike": False},
                        "alas": {"nappain": pygame.K_DOWN, "liike": False}}
        self.hirviot = [hirvio]
        self.score = 0
        self.game_over = False

        self.kello = pygame.time.Clock()

        pygame.display.set_caption("Robo-Man")

        self.silmukka()

    def lataa_kuvat(self):
        def lataa_kuva(nimi: str):
            kuva = pygame.image.load(f'{nimi}.png')
            # pinennetään kuvaa jotta se mahtuu kivasti yhden ruudun sisälle
            pikselikoko = kartta.skaala - 1
            return pygame.transform.scale(kuva, (pikselikoko, pikselikoko))

        self.kuvat = {nimi: lataa_kuva(nimi) for nimi in ["hirvio", "robo"]}
        self.robo_leveys = self.kuvat["robo"].get_width()

    def uusi_peli(self):
        self.kartta = kartta.kartta
        self.pisteet = 0

    def silmukka(self):
        while True:
            self.tutki_tapahtumat()
            if not self.game_over:
                self.piirra_naytto()
            else:
                self.peli_loppu()

            self.liikkuu()
            for hirvio in self.hirviot:
                hirvio.liikkuu()
                if hirvio.osui_roboon:
                    self.game_over = True

            self.kello.tick(60)

    def tutki_tapahtumat(self):
        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.KEYDOWN:
                self.nappain_alas(tapahtuma)

            if tapahtuma.type == pygame.KEYUP:
                self.nappain_ylos(tapahtuma)

            if tapahtuma.type == pygame.QUIT:
                exit()

    def nappain_alas(self, tapahtuma):
        for arvot in self.suunnat.values():
            if tapahtuma.key == arvot["nappain"]:
                arvot["liike"] = True

        if tapahtuma.key == pygame.K_ESCAPE:
            exit()

    def nappain_ylos(self, tapahtuma):
        for arvot in self.suunnat.values():
            if tapahtuma.key == arvot["nappain"]:
                arvot["liike"] = False

    def liikkuu(self):
        suunnat = self.suunnat
        if suunnat["oikealle"]["liike"]:
            self.liike_oikealle()

        if suunnat["vasemmalle"]["liike"]:
            self.liike_vasemmalle()

        if suunnat["ylos"]["liike"]:
            self.liike_ylos()

        if suunnat["alas"]["liike"]:
            self.liike_alas()

        self.osuuko_kolikkoon()

    def osuuko_kolikkoon(self):
        robo_leveys = range(robo.vasen_laita(), robo.oikea_laita())
        robo_korkeus = range(robo.ylareuna(), robo.alareuna())
        poistettava = {}
        KORJAUS = 5
        for kolikko in kolikot.koordinaatit:
            vasen_laita = kolikko["x"]
            oikea_laita = kolikko["x"] + kartta.kuvakoko
            kolikko_leveys = range(vasen_laita, oikea_laita)
            ylareuna = kolikko["y"]
            alareuna = kolikko["y"] + kartta.kuvakoko
            kolikko_korkeus = range(ylareuna, alareuna)

            suurin_vasen_laita = max(robo_leveys[0], kolikko_leveys[0])
            pienin_oikea_laita = min(robo_leveys[-1], kolikko_leveys[-1])
            # ilman korjausta, kolikko katoaa hieman liian aikaisin
            paallekkaiset_x_koordinaatit = range(suurin_vasen_laita, pienin_oikea_laita - KORJAUS)

            matalin_ylareuna = max(robo_korkeus[0], kolikko_korkeus[0])
            korkein_alareuna = min(robo_korkeus[-1], kolikko_korkeus[-1])
            paallekkaiset_y_koordinaatit = range(matalin_ylareuna, korkein_alareuna - KORJAUS)

            # jos näiden pituus on yli 0, se vastaa arvoa True
            if paallekkaiset_x_koordinaatit and paallekkaiset_y_koordinaatit:
                poistettava = kolikko
                self.score += 1
        if poistettava:
            kolikot.koordinaatit.remove(poistettava)
            if not kolikot.koordinaatit:
                kolikot.satunnaiset_kolikot()
                uusi_hirvio = Morko()
                uusi_hirvio.x = self.hirvion_aloitus_x
                uusi_hirvio.y = self.hirvion_aloitus_y
                self.hirviot.append(uusi_hirvio)

    def liike_oikealle(self):
        for seina in kartta.seinat:
            kylki_seinassa = seina.vasen_laita() <= robo.oikea_laita() <= seina.oikea_laita()
            if kylki_seinassa and self.korkeudet_tasmaavat(seina):
                return
        robo.x += self.NOPEUS
        # mahdollista Robon liikkuminen näytön puolelta toiselle
        if robo.x >= kartta.leveys * kartta.skaala:
            # lisätään korjaus, sillä muuten robon x-koordinaatista tulisi pariton, mikä aiheuttaa bugeja
            KORJAUS = 1
            robo.x = -self.robo_leveys + self.NOPEUS + KORJAUS

    def liike_vasemmalle(self):
        for seina in kartta.seinat:
            kylki_seinassa = seina.vasen_laita() <= robo.vasen_laita() <= seina.oikea_laita()
            if kylki_seinassa and self.korkeudet_tasmaavat(seina):
                return
        robo.x -= self.NOPEUS
        # mahdollista Robon liikkuminen näytön puolelta toiselle
        KORJAUS = 1
        # ilman korjausta, robo on mahdollista hävittää täysin ikkunan ulkopuolelle
        if robo.x <= KORJAUS - self.robo_leveys:
            robo.x = kartta.leveys * kartta.skaala - self.NOPEUS

    def liike_ylos(self):
        for seina in kartta.seinat:
            paa_seinassa = seina.ylareuna() <= robo.ylareuna() <= seina.alareuna()
            if paa_seinassa and self.leveydet_tasmaavat(seina):
                return
        robo.y -= self.NOPEUS

    def liike_alas(self):
        for seina in kartta.seinat:
            jalat_seinassa = seina.ylareuna() <= robo.alareuna() <= seina.alareuna()
            if jalat_seinassa and self.leveydet_tasmaavat(seina):
                return
        robo.y += self.NOPEUS

    def korkeudet_tasmaavat(self, seina: Seina):
        ylareuna_kohdalla = seina.ylareuna() <= robo.ylareuna() < seina.alareuna()
        # ilman korjausta, robo ei pääse liikkumaan sivuittain, jalkojen ollessa kiinni alapuolen seinässä
        KORJAUS = 1
        alareuna_kohdalla = seina.ylareuna() + KORJAUS < robo.alareuna() <= seina.alareuna()
        return ylareuna_kohdalla or alareuna_kohdalla

    def leveydet_tasmaavat(self, seina: Seina):
        # ilman korjausta, robo jää jumiin kun menee kiinni oikeanpuoleiseen seinään
        KORJAUS = 1
        oikea_laita_kohdalla = seina.vasen_laita() + KORJAUS < robo.oikea_laita() < seina.oikea_laita()
        vasen_laita_kohdalla = seina.vasen_laita() < robo.vasen_laita() < seina.oikea_laita()
        return oikea_laita_kohdalla or vasen_laita_kohdalla

    def maarita_aloituskoordinaatit(self, objekti, x: int, y: int):
        objekti.x = x * kartta.skaala
        objekti.y = y * kartta.skaala

    def piirra_naytto(self):
        skaala = kartta.skaala
        VALKOINEN = (255, 255, 255)
        self.naytto.fill(VALKOINEN)
        SEINA = 1
        HIRVIO = 2
        ROBO = 3
        # itertools.product antaa kahden iteroitavan olion karteesisen tulon
        # sillä voi kätevästi korvata sisäkkäiset for-silmukat
        for y, x in itertools.product(range(kartta.korkeus), range(kartta.leveys)):
            ruutu = self.kartta[y][x]
            if ruutu == SEINA:
                nelio = (x * skaala, y * skaala, skaala, skaala)
                pygame.draw.rect(self.naytto, self.VARI, nelio)
            elif ruutu == HIRVIO:
                self.hirvion_aloitus_x = x * kartta.skaala
                self.hirvion_aloitus_y = y * kartta.skaala
                self.maarita_aloituskoordinaatit(hirvio, x, y)
                self.kartta[y][x] = 0
            elif ruutu == ROBO:
                self.maarita_aloituskoordinaatit(robo, x, y)
                self.kartta[y][x] = 0

        MUSTA = (0, 0, 0)
        suorakulmion_leveys = kartta.leveys * skaala
        suorakulmion_ylareuna = kartta.korkeus * skaala
        suorakulmio = (0, suorakulmion_ylareuna, suorakulmion_leveys, skaala)
        pygame.draw.rect(self.naytto, MUSTA, suorakulmio)

        PUNAINEN = (0, 0, 255)
        teksti = self.fontti.render(f"Score: {self.score}", True, PUNAINEN)
        TEKSTI_X = 12
        teksti_y = suorakulmion_ylareuna + 10
        self.naytto.blit(teksti, (TEKSTI_X, teksti_y))

        for koordinaatti in kolikot.koordinaatit:
            self.naytto.blit(kolikot.kuva, (koordinaatti["x"], koordinaatti["y"]))

        for hahmo in [*self.hirviot, robo]:
            self.naytto.blit(hahmo.kuva, (hahmo.x, hahmo.y))

        pygame.display.flip()

    def peli_loppu(self):
        PUNAINEN = (255, 0, 0)
        MUSTA = (0, 0, 0)
        self.naytto.fill(MUSTA)

        def piirra_teksti(teksti: str, y_offset: int = 0):
            teksti = self.fontti.render(teksti, True, PUNAINEN)
            teksti_x = self.ikkunan_leveys / 2 - teksti.get_width() / 2
            teksti_y = self.ikkunan_korkeus / 2 - teksti.get_height() / 2 + y_offset
            self.naytto.blit(teksti, (teksti_x, teksti_y))

        piirra_teksti("GAME OVER")
        Y_OFFSET = 40
        piirra_teksti(f"Score: {self.score}", Y_OFFSET)

        pygame.display.flip()


if __name__ == "__main__":
    kartta = Kartta()
    robo = Robo()
    hirvio = Morko()
    kolikot = Kolikot()
    Peli()
