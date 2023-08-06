from kerapu.boom.boom_parameter.BoomParameter import BoomParameter
from kerapu.lbz.Subtraject import Subtraject


class ZorgVraagCluster(BoomParameter):
    """
    Klasse voor boomparameter zorgvraagcluster.

    Boomparameternummers: 221, 222.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, cluster_nummer: int):
        """
        Object constructor.

        :param int cluster_nummer: Het clusternummer (1..2).
        """
        self._cluster_nummer: int = cluster_nummer
        """
        Het clusternummer (1..2).
        """

    # ------------------------------------------------------------------------------------------------------------------
    def tel(self, cluster_code: str, subtraject: Subtraject) -> int:
        """
        Geeft het aantal malen (d.w.z. 0 of 1) dat de zorgvraag van een subtraject voorkomt in een zorgvraagcluster.

        :param str cluster_code: De cluster_code waartegen getest moet worden.
        :param Subtraject subtraject: Het subtraject.

        :rtype: int
        """
        return subtraject.telling_zorg_vraag_cluster(cluster_code, self._cluster_nummer)

# ----------------------------------------------------------------------------------------------------------------------
