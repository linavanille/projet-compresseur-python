#!/usr/bin/env python3
""" Module proposant la classe ArbreHuffman"""

class ArbreHuffmanErreur(Exception):
    pass

class DoitEtreUneFeuilleErreur(ArbreHuffmanErreur):
    pass

class NeDoitPasEtreUneFeuilleErreur(ArbreHuffmanErreur):
    pass

class ArbreHuffmanIncoherentErreur(ArbreHuffmanErreur):
    pass

class ArbreHuffman:
    def __init__(self, element=None, nb_occurrences=None, fils_gauche = None, fils_droit= None):
        if  element is not None and nb_occurrences is not None and fils_droit is None and fils_gauche is None:
            self._element = element
            self._nb_occurrences = nb_occurrences
            self._fils_gauche = None
            self._fils_droit = None
        elif element is None and nb_occurrences is None and fils_gauche is not None and fils_droit is not None:
            if fils_droit is fils_gauche:
                raise ArbreHuffmanIncoherentErreur("les fils sont identiques")
            self._element = None
            self._fils_droit = fils_droit
            self._fils_gauche = fils_gauche
            self._nb_occurrences = fils_gauche.nb_occurrences + fils_droit.nb_occurrences
        else:
            raise ArbreHuffmanIncoherentErreur("incohérence dans l'arbre")
    
    @property
    def est_une_feuille(self):
        return self._fils_droit is None and self._fils_gauche is None

    @property
    def nb_occurrences(self):
        return self._nb_occurrences

    @property
    def element(self):
        if not self.est_une_feuille:
            raise DoitEtreUneFeuilleErreur("ce n'est pas une feuille")
        return self._element

    @property
    def fils_gauche(self):
        if self.est_une_feuille:
            raise NeDoitPasEtreUneFeuilleErreur("c'est une feuille")
        return self._fils_gauche

    @property
    def fils_droit(self):
        if self.est_une_feuille:
            raise NeDoitPasEtreUneFeuilleErreur("c'est une feuille")
        return self._fils_droit

    def equivalent(self, autre):
        if not isinstance(autre, ArbreHuffman):
            return False
        if self.est_une_feuille and autre.est_une_feuille:
            return self.element == autre.element and self.nb_occurrences == autre.nb_occurrences
        if not self.est_une_feuille and not autre.est_une_feuille:
            return self._fils_gauche.equivalent(autre._fils_gauche) and self._fils_droit.equivalent(autre._fils_droit)
        return False

    def __lt__(self, autre):
        """Comparaison de l'arbre courant avec un autre sur la base du nombre d'occurrences."""
        return self._nb_occurrences < autre._nb_occurrences

    def __le__(self, autre):
        """Comparaison de l'arbre courant avec un autre sur la base du nombre d'occurrences (inférieur ou égal)."""
        return self._nb_occurrences <= autre._nb_occurrences
        
    def __add__(self, autre):
        """Permet d'utiliser l'opérateur '+' pour ajouter deux arbres."""
        return self.add(autre)

    def __gt__(self, autre):
        """Comparaison de l'arbre courant avec un autre sur la base du nombre d'occurrences (supérieur)."""
        return self._nb_occurrences > autre._nb_occurrences

    def __ge__(self, autre):
        """Comparaison de l'arbre courant avec un autre sur la base du nombre d'occurrences (supérieur ou égal)."""
        return self._nb_occurrences >= autre._nb_occurrences

    def __add__(self, autre):
        return ArbreHuffman(fils_gauche=self, fils_droit=autre)
    
    def __repr__(self):
        """Retourne une représentation en chaîne de caractères de l'arbre."""
        if self.est_une_feuille:
            return f"Feuille({self._element}, {self._nb_occurrences})"
        return f"Noeud({self._nb_occurrences}, {repr(self._fils_gauche)}, {repr(self._fils_droit)})"

    def __str__(self):
        if self.est_une_feuille:
            return f"{self._element} ({self._nb_occurrences})"
        return f"({str(self._fils_gauche)} + {str(self._fils_droit)}) ({self._nb_occurrences})"
