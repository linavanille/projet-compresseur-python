#!/usr/bin/env python3
""" Module proposant la classe Compteur """
from typing import TypeVar

T = TypeVar('T')

class Compteur:
    """ Compteur permet d'avoir des statistiques (nombre d'occurences) sur
des éléments hashables

    arguments:
    val_init -- dictionnaire(element, nb_occurences) qui permet d'initialiser
le compteur à sa création
    """
    def __init__(self, val_init: dict[T, int] = None):
        """
        initialise le compteur
        """
        self._compt = dict((val_init or {}).items())

    def incrementer(self, element: T) -> None:
        """
        augmente le nb d'occurence d'un élément
        """
        self._compt[element] = self._compt.get(element, 0) + 1

    def fixer(self, element: T, nb_occurences: int) -> None:
        """
        fixe le nb occ
        """
        self._compt[element] = nb_occurences

    def nb_occurrences(self, element: T) -> int:
        """ donne le nb occ"""
        return self._compt.get(element, 0)

    @property
    def elements(self) -> set[T]:
        """ retourne tous les éléments"""
        return set(self._compt.keys())

    def elements_moins_frequents(self) -> set[T]:
        """retourne tous les elements les moins frequents

        resultat: un ensemble contenant les éléments les moins fréquents
        """
        if not self._compt:
            return set()
        occurence_min = min(self._compt.values())
        return {el for el, occ in self._compt.items() if occ == occurence_min}

    def elements_plus_frequents(self) -> set[T]:
        """retourne tous les elements les plus frequents

        resultat: un ensemble contenant les éléments les plus fréquents
        """
        if not self._compt:
            return set()
        occurence_max = max(self._compt.values())
        return {elem for elem, occ in self._compt.items() if occ == occurence_max}

    def elements_par_nb_occurrences(self) -> dict[int, set[T]]:
        """retourne pour chaque nombre d'occurences présents dans compteur
les éléments qui ont ces nombres d'occurences

        resultat: un dictionnaire dont les clés sont les nombres d'occurences
et les valeurs des ensembles d'éléments qui ont ce nombre d'occurences"""
        occurences = {}
        for elem, occ in self._compt.items():
            if occ not in occurences:
                occurences[occ] = set()
            occurences[occ].add(elem)
        return occurences

    def __iter__(self):
        """Permet d'itérer sur les éléments du plus prioritaire au moins prioritaire."""
        return iter(self._compt)

    
    def __eq__(self, other):
        """Vérifie si deux files de priorités sont égales."""
        if not isinstance(other, Compteur):
            return False
        return self._compt == other._compt

    def __repr__(self):
        return f"Compteur({self._compt})"


def main():
    """Tests unitaires du module"""
    def ok_ko_en_str(booleen):
        return "OK" if booleen else "KO"

    def ok_ko(fct, resultat_attendu, *param):
        """mini fonction de TU"""
        res = fct.__name__ + ' : '
        res = res + ok_ko_en_str(fct(*param) == resultat_attendu)
        print(res)

    cpt1 = Compteur()
    cpt1.incrementer('a')
    cpt1.incrementer('a')
    cpt1.incrementer('b')
    cpt1.incrementer('c')
    cpt1.incrementer('c')
    cpt1.incrementer('c')
    cpt1.incrementer('d')

    ok_ko(Compteur.nb_occurrences, 2, cpt1, 'a')
    ok_ko(Compteur.elements, {'a', 'b', 'c', 'd'}, cpt1)
    ok_ko(Compteur.elements_moins_frequents, {'b', 'd'}, cpt1)
    ok_ko(Compteur.elements_plus_frequents, {'c'}, cpt1)
    ok_ko(Compteur.elements_par_nb_occurrences, {1: {'b', 'd'}, 2: {'a'}, 3: {'c'}}, cpt1)

if __name__ == "__main__":
    main()
