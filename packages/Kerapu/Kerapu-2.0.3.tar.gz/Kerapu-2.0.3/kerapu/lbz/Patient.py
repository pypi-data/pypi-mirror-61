class Patient:
    """
    Klasse voor patiëntenn.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, geboorte_datum: str, geslacht_code: str):
        """
        Object constructor.

        :param str geboorte_datum: De geboortedatum van de patiënt.
        :param str geslacht_code: Het geslacht van de patiënt.
        """
        self.__geboorte_datum: str = geboorte_datum
        """
        De geboortedatum van de patiënt.
        """

        self.__geslacht_code: str = Patient.normaliseer_geslacht_code(geslacht_code)
        """
        Het geslacht van de patiënt.
        """

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def geslacht_code(self) -> str:
        """
        Geeft het geslacht van deze patiënt.

        :rtype: str
        """
        return self.__geslacht_code

    # ------------------------------------------------------------------------------------------------------------------
    def leeftijd(self, datum: str) -> int:
        """
        Geeft de leeftijd van deze patient op een peildatum.

        :param str datum: De peildatum.

        :rtype: int
        """
        if not datum:
            raise RuntimeError("Datum is niet gespecificeerd.")

        if not self.__geboorte_datum:
            raise RuntimeError("Geboortedatum is niet gespecificeerd.")

        if datum < self.__geboorte_datum:
            raise RuntimeError("Leeftijd van patient gevraagd op datum (%s) voor geboortedatum (%s)." %
                               (datum, self.__geboorte_datum))

        age = int(datum[0:4]) - int(self.__geboorte_datum[0:4])
        if datum[-5:] < self.__geboorte_datum[-5:]:
            age -= 1

        return age

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def normaliseer_geslacht_code(geslacht_code: str) -> str:
        """
        Normaliseert een geslachtscode naar 1 (man), 2 (vrouw) of 9 (anders).

        :param str geslacht_code: De geslachtscode.

        :rtype: str
        """
        if geslacht_code.upper() in ('1', 'M'):
            return '1'

        if geslacht_code.upper() in ('2', 'V', 'F'):
            return '2'

        return '9'

# ----------------------------------------------------------------------------------------------------------------------
