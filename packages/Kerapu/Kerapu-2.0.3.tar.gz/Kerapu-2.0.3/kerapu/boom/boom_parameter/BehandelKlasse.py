from kerapu.boom.boom_parameter.BoomParameter import BoomParameter
from kerapu.lbz.Subtraject import Subtraject


class BehandelKlasse(BoomParameter):
    """
    Klasse voor boomparameter behandelklasse: som van aantal (met en zonder weegfactor).

    Boomparameternummers: 351, 451, 551.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, weeg_factor_nummer: int):
        """
        Object contructor.

        :param int weeg_factor_nummer: Weegfactornummer:

                                       * 0: geen weegfactor
                                       * 1: weegfactor 1
                                       * 2: weegfactor 2
        """
        self._weeg_factor_nummer: int = weeg_factor_nummer
        """
        Weegfactornummer
        """

    # ------------------------------------------------------------------------------------------------------------------
    def tel(self, behandel_klasse_code: str, subtraject: Subtraject) -> int:
        """
        Geeft het aantal zorgactiviteiten (met inachtneming van weegfactor) in een subtraject voorkomt in een
        behandelklasse.

        :param str behandel_klasse_code: De behandelklassecode waartegen getest moet worden.
        :param Subtraject subtraject: Het subtraject.

        :rtype: int
        """
        return subtraject.telling_behandel_klasse(behandel_klasse_code, self._weeg_factor_nummer)

# ----------------------------------------------------------------------------------------------------------------------
