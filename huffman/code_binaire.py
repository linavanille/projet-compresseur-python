#!/usr/bin/env python3
""" Module proposant les classes Bit et CodeBinaire"""
from enum import Enum

class TypeError(Exception):
    pass

class AuMoinsUnBitErreur(Exception):
    pass

class Bit(Enum):
    BIT_0 = 0
    BIT_1 = 1

    def __repr__(self):
        return f"Bit.{self.name}"

class CodeBinaire:
    def __init__(self, bit, *bits):
        
        if not isinstance(bit, Bit):
            raise TypeError("bit doit etre construit à partie de Bit")
        self.code_binaire = [bit]
        for element in bits:
            if not isinstance(element, Bit):
                raise TypeError("bit doit etre construit à partie de Bit")
            self.code_binaire.append(element)

    def ajouter(self, bit):
        if not isinstance(bit, Bit):
            raise TypeError("bit doit etre construit à partie de Bit")
        self.code_binaire.append(bit)

    @property
    def bits(self):
        return tuple(self.code_binaire)

    def __len__(self):
        return len(self.code_binaire)

    def __add__(self, other):
        if isinstance(other, Bit):
            return CodeBinaire(*self.code_binaire, other)
        elif isinstance(other, CodeBinaire):
            return CodeBinaire(*self.code_binaire, *other.code_binaire)
        else:
            raise TypeError("On ne peut concaténer qu'avec un CodeBinaire ou un Bit")

    def __getitem__(self, indice_ou_slice):
        if isinstance(indice_ou_slice, slice):
            return CodeBinaire(*self.code_binaire[indice_ou_slice])
        return self.code_binaire[indice_ou_slice]

    def __setitem__(self, indice_ou_slice, bit_ou_bits):
        if isinstance(indice_ou_slice, int):
            self.code_binaire[indice_ou_slice] = bit_ou_bits
        elif isinstance(indice_ou_slice, slice):
            if isinstance(bit_ou_bits, CodeBinaire):
                self.code_binaire[indice_ou_slice] = bit_ou_bits.bits
            elif isinstance(bit_ou_bits, list) or isinstance(bit_ou_bits, tuple):
                self.code_binaire[indice_ou_slice] = bit_ou_bits

    def __delitem__(self, indice_ou_slice):
        copie = self.code_binaire.copy()
        del copie[indice_ou_slice]
        
        if len(copie) == 0:
            raise AuMoinsUnBitErreur("Un code binaire doit posséder au moins un bit")
        
        del self.code_binaire[indice_ou_slice]

    def __iter__(self):
        """Permet d'itérer sur les bits du code binaire."""
        return iter(self.code_binaire)

    def __eq__(self, other):
        """Vérifie si deux codes binaires sont égaux."""
        if not isinstance(other, CodeBinaire):
            return False
        return self.code_binaire == other.code_binaire

    def __repr__(self):
        """Représentation évaluable de l'objet."""
        return f"CodeBinaire({', '.join(f'Bit.{bit.name}' for bit in self.code_binaire)})"

    def __str__(self):
        """Représentation sous forme d'une suite de 0 et 1."""
        result = ""
        for bit in self.code_binaire:
            result += str(bit.value)
        return result
