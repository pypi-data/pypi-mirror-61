from kerapu.boom.attribuut.Attribuut import Attribuut
from kerapu.boom.attribuut_groep_koppeling.AttribuutGroepKoppeling import AttribuutGroepKoppeling
from kerapu.boom.attribuut_groep_koppeling.AttribuutGroepKoppeling2 import AttribuutGroepKoppeling2


def maak_attribuut_groep_koppeling(attribute_groep_id: int,
                                   attribuut: Attribuut,
                                   attribuut_toets_wijze: int,
                                   onder_toets_waarde: int,
                                   boven_toets_waarde: int) -> AttribuutGroepKoppeling:
    """
    Fabriek voor het maken van attribuutgroepkoppelingen.

    :param int attribute_groep_id: Het ID van de koppeling.
    :param Attribuut attribuut: Het attribuut van de koppeling.
    :param int attribuut_toets_wijze: De attribuuttoetswijze.
    :param int onder_toets_waarde: De ondergrens.
    :param int boven_toets_waarde: De bovengrens.

    :rtype: AttribuutGroepKoppeling
    """
    if attribuut_toets_wijze == 1:
        # Attribuuttoetswijze 1 wordt thans niet gebruikt in de grouper.
        raise NotImplementedError("Attribuuttoetswijze %d is niet geïmplementeerd." % attribuut_toets_wijze)

    if attribuut_toets_wijze == 2:
        return AttribuutGroepKoppeling2(attribute_groep_id, attribuut, onder_toets_waarde, boven_toets_waarde)

    raise RuntimeError("Onbekende attribuuttoetswijze %d." % attribuut_toets_wijze)

# ----------------------------------------------------------------------------------------------------------------------
