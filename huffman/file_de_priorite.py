#!/usr/bin/env python3
""" Module proposant la classe FileDePriorite """

class FileDePrioriteVideErreur(Exception):
    pass

class ElementNonComparableErreur(Exception):
    pass

class FileDePriorite:
    def __init__(self, elements=(), cle= lambda e:e):
        self.cle = cle
        self.file = []
        for i in elements:
            self.enfiler(i)

    @property
    def est_vide(self):
        return len(self.file) == 0

    def enfiler(self, element):
        i = 0
        element_cle = self.cle(element)

        try:
            _ = element_cle < element_cle
        except TypeError:
            raise ElementNonComparableErreur(
                f"La classe de {element} ne possède pas les méthodes de comparaison"
            )

        if self.file:
            try:
                while i < len(self.file) and self.cle(self.file[i]) <= element_cle:
                    i += 1
            except TypeError:
                raise ElementNonComparableErreur(
                    f"{element} ne peut être comparé à {self.file[0]}"
                )
            except Exception as e:
                raise ElementNonComparableErreur(
                    f"Erreur de comparaison entre {element} et {self.file[0]}: {e}"
                )

        self.file.insert(i, element)

    def defiler(self):
        if self.est_vide:
            raise FileDePrioriteVideErreur("La file est vide")
        element = self.file.pop(0)
        return element

    @property
    def element(self):
        if self.est_vide:
            raise FileDePrioriteVideErreur("La file est vide")
        return self.file[0]

    def __len__(self):
        return len(self.file)


    def __iter__(self):
        """Permet d'itérer sur les éléments du plus prioritaire au moins prioritaire."""
        return iter(self.file)

    
    def __eq__(self, other):
        """Vérifie si deux files de priorités sont égales."""
        if not isinstance(other, FileDePriorite):
            return False
        return self.file == other.file

    def __repr__(self):
        return f"FileDePriorite({self.file})"

    def __str__(self):
        """Représentation lisible de la file de priorité pour l'utilisateur."""
        return f"Éléments triés par priorité: {self.file}" if not self.est_vide else "File de priorité vide"
    