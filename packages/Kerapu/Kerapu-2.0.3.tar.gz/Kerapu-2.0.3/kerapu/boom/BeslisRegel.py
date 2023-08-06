from typing import Optional

from kerapu.boom.AttribuutGroep import AttribuutGroep
from kerapu.lbz.Subtraject import Subtraject


class BeslisRegel:
    """
    Klasse voor beslisregels.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 beslist_regel_id: int,
                 attribuut_groep: AttribuutGroep,
                 label_true: str,
                 label_false: str,
                 indicatie_aanspraakbeperking: bool):
        """
        Object constructor.

        :param int beslist_regel_id: Het ID van deze beslisregel.
        :param AttribuutGroep attribuut_groep: De attribuutgroep van deze beslisregel.
        :param str label_true: Label voor True.
        :param str label_false: Label voor False.
        :param bool indicatie_aanspraakbeperking: Vlag voor aanspraakbeperking.
        """
        self._beslist_regel_id: int = beslist_regel_id
        """
         Het ID van deze beslisregel.
        """

        self._attribuut_groep: AttribuutGroep = attribuut_groep
        """
        De attribuutgroep van deze beslisregel.
        """

        self._beslist_regel_true: Optional[BeslisRegel] = None
        """
        De beslisregel die gevolgt moet worden als deze beslisregel True is.
        """

        self._beslist_regel_false: Optional[BeslisRegel] = None
        """
        De beslisregel die gevolgt moet worden als deze beslisregel False is.
        """

        self._label_true: str = label_true
        """
        Label voor True.
        """

        self._label_false: str = label_false
        """
        Label voor False.
        """

        self._indicatie_aanspraakbeperking: bool = indicatie_aanspraakbeperking
        """
        Vlag voor aanspraakbeperking.
        """

    # ------------------------------------------------------------------------------------------------------------------
    def verrijk(self, beslist_regel_true, beslist_regel_false) -> None:
        """
        Verrijkt deze beslisregel met beslisregels voor True and False.

        :param kerapu.boom.BeslisRegel.BeslisRegel beslist_regel_true: De beslisregel voor True.
        :param kerapu.boom.BeslisRegel.BeslisRegel beslist_regel_false: De beslisregel voor False.
        """
        self._beslist_regel_true = beslist_regel_true
        self._beslist_regel_false = beslist_regel_false

    # ------------------------------------------------------------------------------------------------------------------
    def klim(self, subtraject: Subtraject) -> str:
        """
        Klimt door de beslisboom een geeft het uiteindelijk gevonden label terug.

        :param Subtraject subtraject: Het subtraject.

        :rtype: str
        """
        test = self._attribuut_groep.test(subtraject)

        if not test:
            if self._beslist_regel_false:
                return self._beslist_regel_false.klim(subtraject)

            return self._label_false

        if self._beslist_regel_true:
            return self._beslist_regel_true.klim(subtraject)

        return self._label_true

# ----------------------------------------------------------------------------------------------------------------------
