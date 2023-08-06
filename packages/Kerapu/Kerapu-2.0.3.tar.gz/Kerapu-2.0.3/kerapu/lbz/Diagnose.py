import csv
from typing import Optional, Dict, List, Tuple

from kerapu import clean_code, clean_date, clean_str, LEN_DIAGNOSE_CODE, LEN_SPECIALISME_CODE


class Diagnose:
    """
    Klasse voor diagnosen.
    """
    # ------------------------------------------------------------------------------------------------------------------
    __diagnose_tabel: Dict[Tuple[str, str], List[Dict[str, str]]] = {}
    """
    De diagnosen referentietabel.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, specialisme_code: str, diagnose_code: str):
        """
        Object constructor.

        :param str specialisme_code: De code van het uitvoerend specialisme.
        :param str diagnose_code: De code van deze diagnose.
        """
        self.__specialisme_code: str = clean_code(specialisme_code, LEN_SPECIALISME_CODE)
        """
        De code van het uitvoerend specialisme.
        """

        self.__diagnose_code: str = clean_code(diagnose_code, LEN_DIAGNOSE_CODE)
        """
        De code van deze diagnose.
        """

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def __lees_diagnose_tabel(folder: str) -> None:
        """
        Leest de diagnose referentietabel (opgeslagen in CSV).

        :param str folder: De folder met alle goupertabellen.
        """
        with open(folder + '/Diagnosen.csv', 'r', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            regel_nummer = 0
            for regel in reader:
                regel_nummer += 1

                # Sla de eerste regel met koppen over.
                if regel_nummer == 1:
                    continue

                specialisme_code = clean_code(regel[0], LEN_SPECIALISME_CODE)
                diagnose_code = clean_code(regel[1], LEN_DIAGNOSE_CODE)
                diagnose_attribute_code = clean_str(regel[3])
                diagnose_cluster01 = clean_str(regel[5])
                diagnose_cluster02 = clean_str(regel[6])
                diagnose_cluster03 = clean_str(regel[7])
                diagnose_cluster04 = clean_str(regel[8])
                diagnose_cluster05 = clean_str(regel[9])
                diagnose_cluster06 = clean_str(regel[10])
                begin_datum = clean_date(regel[11])
                eind_datum = clean_date(regel[12])

                sleutel = (specialisme_code, diagnose_code)

                rij = {'specialisme_code':        specialisme_code,
                       'diagnose_code':           diagnose_code,
                       'diagnose_attribute_code': diagnose_attribute_code,
                       'diagnose_cluster1':       diagnose_cluster01,
                       'diagnose_cluster2':       diagnose_cluster02,
                       'diagnose_cluster3':       diagnose_cluster03,
                       'diagnose_cluster4':       diagnose_cluster04,
                       'diagnose_cluster5':       diagnose_cluster05,
                       'diagnose_cluster6':       diagnose_cluster06,
                       'begin_datum':             begin_datum,
                       'eind_datum':              eind_datum}

                if sleutel not in Diagnose.__diagnose_tabel:
                    Diagnose.__diagnose_tabel[sleutel] = []

                Diagnose.__diagnose_tabel[sleutel].append(rij)

        print("Aantal diagnosen: %d" % (regel_nummer - 1))

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def init_static(folder: str) -> None:
        """
        Initialiseert alle statistische data.

        :param str folder: De folder met alle goupertabellen.
        """
        Diagnose.__lees_diagnose_tabel(folder)

    # ------------------------------------------------------------------------------------------------------------------
    def __diagnose_referentie(self, datum: str) -> Optional[Dict]:
        """
        Zoekt de referentie data voor deze diagnose in de diagnosen referentietabel.

        :param str datum: De begindatum van het subtraject.
        :rtype: dict[str,str]
        """
        if (self.__specialisme_code, self.__diagnose_code) in self.__diagnose_tabel:
            for referentie in self.__diagnose_tabel[(self.__specialisme_code, self.__diagnose_code)]:
                if referentie['begin_datum'] <= datum <= referentie['eind_datum']:
                    # Een geldige referentie rij gevonden.
                    return referentie

            # Er is geen geldige referentie rij gevonden.
            return None

        else:
            return None

    # ------------------------------------------------------------------------------------------------------------------
    def diagnose_attribute_aantal(self, diagnose_attribute_code: str, datum: str) -> int:
        """
        Geeft het aantal malen (d.w.z. 0 of 1) data deze diagnose voldoet aan een (specialismecode, diagnosecode)
        op een peildatum.

        :param str diagnose_attribute_code: De attribuutcode voor de (specialismecode, diagnosecode) combinatie.
        :param str datum: De peildatum.

        :rtype: int
        """
        referentie = self.__diagnose_referentie(datum)

        if not referentie:
            # De diagnose komt niet voor in de referentie tabel. Geef 0 terug.
            return 0

        if referentie['diagnose_attribute_code'] == diagnose_attribute_code:
            return 1

        return 0

    # ------------------------------------------------------------------------------------------------------------------
    def diagnose_cluster_aantal(self, cluster_code: str, cluster_nummer: int, datum: str) -> int:
        """
        Geeft het aantal malen (d.w.z. 0 of 1) data deze diagnose voorkomt in een diagnosecodecluster op een peildatum.

        :param str cluster_code: De diagnoseclustercode.
        :param int cluster_nummer: De clusternummer (0..6).
        :param str datum: De peildatum.

        :rtype: int
        """
        referentie = self.__diagnose_referentie(datum)

        if not referentie:
            # De diagnose komt niet voor in de referentie tabel. Geef 0 terug.
            return 0

        if cluster_nummer == 0:
            return 1

        if 1 <= cluster_nummer <= 6:
            if referentie['diagnose_cluster%d' % cluster_nummer] == cluster_code:
                # Deze diagnose komt voor in het gevraagde cluster.
                return 1

            return 0

        raise RuntimeError("Onbekend clusternummer %d." % cluster_nummer)

# ----------------------------------------------------------------------------------------------------------------------
