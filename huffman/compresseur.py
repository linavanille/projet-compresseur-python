#!/usr/bin/env python3
""" script principal du module """
from typing import Dict
import io
import logging
from huffman.compteur import Compteur
from huffman.arbre_huffman import ArbreHuffman
from huffman.file_de_priorite import FileDePriorite
from huffman.code_binaire import CodeBinaire, Bit

LOGGER = logging.getLogger()

NB_OCTETS_CODAGE_INT = 4

def statistiques(source: io.BufferedReader) -> (Compteur, int):
    """ fonction qui retourne le nombre d'occurences (Compteur)
d'un flux d'octets et ainsi que le nombre d'octets"""
# @u:start statistiques

    MAX = 1024
    compteur = Compteur()
    taille = 0
    bloc = source.read(MAX)

    while bloc:
        for octet in bloc:
            compteur.incrementer(octet)
        taille += len(bloc)
        bloc = source.read(MAX)
    return compteur, taille

# @u:end statistiques

def arbre_de_huffman(stat: Compteur) -> ArbreHuffman:
    """ fonction qui retourne un arbre d'huffman à partir d'un compteur """
# @u:start arbre_de_huffman

    file = FileDePriorite(cle=lambda arbre: arbre.nb_occurrences)
    for lettre in sorted(stat.elements):
        freq = stat.nb_occurrences(lettre)
        file.enfiler(ArbreHuffman(element=lettre, nb_occurrences=freq))

    while len(file) > 1:
        a1 = file.defiler()
        a2 = file.defiler()
        file.enfiler(a1 + a2)
    
    return file.defiler()

# @u:end arbre_de_huffman

def codes_binaire(abr: ArbreHuffman) -> Dict[int, CodeBinaire]:
    """ fonction qui retourne le code binaire de tous les éléments
d'un arbre d'Huffman """
# @u:start code_binaire

    resultats = {}

    def parcours(arbre: ArbreHuffman, code: CodeBinaire):
        if arbre.est_une_feuille:
            resultats[arbre.element] = code[1:]
        else:
            parcours(arbre.fils_gauche, code + Bit.BIT_0)
            parcours(arbre.fils_droit, code + Bit.BIT_1)

    parcours(abr, CodeBinaire(Bit.BIT_0))
    return resultats

# @u:end code_binaire

def compresser(destination: io.RawIOBase,
               source: io.RawIOBase,
               nboctetspourserialisationdesint: int = 4,
               ordrepourserialisationdesint: str = 'big') -> None:
    
    # 1. Écrire l'identifiant du fichier compressé
    destination.write(bytes([52, 50]))  # 0x34, 0x32

    # 2. Calcul des statistiques et taille
    compteur, taille = statistiques(source)

    # Cas particulier : aucun octet
    if taille == 0:
        destination.write(bytes([0]))  # mode 0
        return

    # Cas particulier : un seul octet répété
    elements = list(compteur.elements)
    if len(elements) == 1:
        destination.write(bytes([1]))  # mode 1
        destination.write(taille.to_bytes(nboctetspourserialisationdesint, ordrepourserialisationdesint))
        destination.write(bytes([elements[0]]))
        return

    # Sinon : mode normal
    destination.write(bytes([2]))  # mode 2

    # 3. Écriture de la longueur du flux source
    destination.write(taille.to_bytes(nboctetspourserialisationdesint, ordrepourserialisationdesint))

    # 4. Écriture des statistiques (256 entiers de 4 octets chacun)
    for i in range(256):
        occ = compteur.nb_occurrences(i)
        destination.write(occ.to_bytes(nboctetspourserialisationdesint, ordrepourserialisationdesint))

    # 5. Arbre de Huffman et table des codes
    arbre = arbre_de_huffman(compteur)
    table_codes = codes_binaire(arbre)

    # 6. Deuxième lecture du fichier pour écrire les données compressées
    source.seek(0)  # repositionner le curseur au début du fichier
    octet_courant = 0
    position_bit = 0

    MAX = 1024
    bloc = source.read(MAX)

    while bloc:
        for octet in bloc:
            code = table_codes[octet]
            for bit in code:
                if bit == Bit.BIT_1:
                    octet_courant |= 2 ** position_bit
                position_bit += 1
                if position_bit == 8:
                    destination.write(bytes([octet_courant]))
                    octet_courant = 0
                    position_bit = 0
        bloc = source.read(MAX)

    # S'il reste des bits à écrire dans l’octet courant
    if position_bit > 0:
        destination.write(bytes([octet_courant]))

def decompresser(destination: io.RawIOBase,
                 source: io.RawIOBase,
                 nb_octets_pour_serialisation_des_int: int = 4,
                 ordre_pour_serialisation_des_int: str = 'big') -> None:
    
    identifiant = source.read(2)
    if identifiant != bytes([52, 50]):
        raise ValueError("Format de fichier compressé non reconnu")

    mode = int.from_bytes(source.read(1), ordre_pour_serialisation_des_int)

    if mode == 0:
        return

    elif mode == 1:
        taille = int.from_bytes(source.read(nb_octets_pour_serialisation_des_int), ordre_pour_serialisation_des_int)
        octet = source.read(1)
        destination.write(octet * taille)
        return

    elif mode == 2:
        taille = int.from_bytes(source.read(nb_octets_pour_serialisation_des_int), ordre_pour_serialisation_des_int)

        compteur = Compteur()
        for i in range(256):
            nb = int.from_bytes(source.read(nb_octets_pour_serialisation_des_int), ordre_pour_serialisation_des_int)
            if nb > 0:
                compteur.fixer(i, nb)

        arbre = arbre_de_huffman(compteur)

        courant = arbre
        lus = 0

        octet = source.read(1)
        while octet and lus < taille:
            byte = octet[0]
            for i in range(8):
                bit = (byte >> i) & 1
                if bit == 0:
                    courant = courant.fils_gauche
                else:
                    courant = courant.fils_droit

                if courant.est_une_feuille:
                    destination.write(bytes([courant.element]))
                    courant = arbre
                    lus += 1
                    if lus == taille:
                        break
            octet = source.read(1)
    else:
        raise ValueError("Mode de compression non reconnu")



if __name__ == "__main__":
    pass
