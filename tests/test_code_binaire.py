#!/usr/bin/python3
# @u:file test_code_binaire.py

import pytest
from huffman.code_binaire import *

@pytest.mark.parametrize("code_binaire_1, code_binaire_2, resultat",
                         [(CodeBinaire(Bit.BIT_0), CodeBinaire(Bit.BIT_0), True),
                          (CodeBinaire(Bit.BIT_1), CodeBinaire(Bit.BIT_1), True),
                          (CodeBinaire(Bit.BIT_1), CodeBinaire(Bit.BIT_0), False),
                          (CodeBinaire(Bit.BIT_1, Bit.BIT_0), CodeBinaire(Bit.BIT_1, Bit.BIT_0), True),
                          (CodeBinaire(Bit.BIT_1, Bit.BIT_1), CodeBinaire(Bit.BIT_1, Bit.BIT_0), False),
                        ])
def test_egalite(code_binaire_1, code_binaire_2, resultat):
    assert (code_binaire_1 == code_binaire_2) == resultat


def test_ajoute_bien_a_la_fin():
    c = CodeBinaire(Bit.BIT_0)
    c.ajouter(Bit.BIT_1)
    assert c[len(c)-1] == Bit.BIT_1

@pytest.mark.parametrize("code_binaire, indice_slice, resultat",
                         [(CodeBinaire(Bit.BIT_0), 0, Bit.BIT_0),
                          (CodeBinaire(Bit.BIT_0, Bit.BIT_1), 1, Bit.BIT_1),
                          (CodeBinaire(Bit.BIT_0, Bit.BIT_1), -1, Bit.BIT_1),
                          (CodeBinaire(Bit.BIT_0, Bit.BIT_1), -2, Bit.BIT_0),
                          (CodeBinaire(Bit.BIT_0, Bit.BIT_1, Bit.BIT_0), slice(0,1), CodeBinaire(Bit.BIT_0)),
                          (CodeBinaire(Bit.BIT_0, Bit.BIT_1, Bit.BIT_0), slice(1,3), CodeBinaire(Bit.BIT_1,Bit.BIT_0)),
                          (CodeBinaire(Bit.BIT_0, Bit.BIT_1, Bit.BIT_0), slice(None,None), CodeBinaire(Bit.BIT_0, Bit.BIT_1,Bit.BIT_0)),
                          (CodeBinaire(Bit.BIT_0, Bit.BIT_1, Bit.BIT_0), slice(None,-1), CodeBinaire(Bit.BIT_0, Bit.BIT_1)),
                          (CodeBinaire(Bit.BIT_0, Bit.BIT_1, Bit.BIT_0), slice(-2, None), CodeBinaire(Bit.BIT_1, Bit.BIT_0)),
                        ])
def test_get(code_binaire, indice_slice, resultat):
    assert code_binaire[indice_slice] == resultat

@pytest.mark.parametrize("code_binaire, indice_slice, bit_bits_ou_code_binaire, resultat",
                         [(CodeBinaire(Bit.BIT_0), 0, Bit.BIT_1, CodeBinaire(Bit.BIT_1)),
                          (CodeBinaire(Bit.BIT_0, Bit.BIT_1, Bit.BIT_0), 1, Bit.BIT_0, CodeBinaire(Bit.BIT_0, Bit.BIT_0, Bit.BIT_0)),
                          (CodeBinaire(Bit.BIT_0, Bit.BIT_1, Bit.BIT_0), slice(0,2), [Bit.BIT_1, Bit.BIT_0], CodeBinaire(Bit.BIT_1, Bit.BIT_0, Bit.BIT_0)),
                          (CodeBinaire(Bit.BIT_0, Bit.BIT_1, Bit.BIT_0), slice(0,2), CodeBinaire(Bit.BIT_1, Bit.BIT_0), CodeBinaire(Bit.BIT_1, Bit.BIT_0, Bit.BIT_0)),
                          (CodeBinaire(Bit.BIT_0, Bit.BIT_1, Bit.BIT_0), slice(0,2), [Bit.BIT_1, Bit.BIT_1, Bit.BIT_0], CodeBinaire(Bit.BIT_1, Bit.BIT_1, Bit.BIT_0, Bit.BIT_0)),                        
                        ])    
def test_set(code_binaire, indice_slice, bit_bits_ou_code_binaire, resultat):
    code_binaire[indice_slice] = bit_bits_ou_code_binaire
    assert code_binaire == resultat

@pytest.mark.parametrize("code_binaire, indice_slice, resultat",
                         [(CodeBinaire(Bit.BIT_0, Bit.BIT_1, Bit.BIT_0), 0, CodeBinaire(Bit.BIT_1, Bit.BIT_0)),
                          (CodeBinaire(Bit.BIT_0, Bit.BIT_1, Bit.BIT_0), slice(1,3), CodeBinaire(Bit.BIT_0)),
                        ])    
def test_del(code_binaire, indice_slice, resultat):
    del(code_binaire[indice_slice])
    assert code_binaire == resultat

@pytest.mark.parametrize("code_binaire_1, code_binaire_2, resultat",
                         [(CodeBinaire(Bit.BIT_0), CodeBinaire(Bit.BIT_1), CodeBinaire(Bit.BIT_0, Bit.BIT_1)),
                          (CodeBinaire(Bit.BIT_1), CodeBinaire(Bit.BIT_0), CodeBinaire(Bit.BIT_1, Bit.BIT_0))
                        ])    
def test_concatenation(code_binaire_1, code_binaire_2, resultat):
    assert code_binaire_1 + code_binaire_2 == resultat



@pytest.mark.parametrize("code_binaire, longueur",
                         [(CodeBinaire(Bit.BIT_0), 1),
                          (CodeBinaire(Bit.BIT_1, Bit.BIT_0), 2),
                        ])        
def test_longueur_apres_creation(code_binaire, longueur):
    assert len(code_binaire) == longueur

def test_longueur_apres_ajout():
    c = CodeBinaire(Bit.BIT_0)
    l = len(c)
    c.ajouter(Bit.BIT_0)
    assert len(c) == l+1

def test_del_au_moins_bit_erreur():
    with pytest.raises(AuMoinsUnBitErreur):
        c = CodeBinaire(Bit.BIT_0)
        del c[0] 

@pytest.mark.parametrize("code_binaire", [CodeBinaire(Bit.BIT_0), CodeBinaire(Bit.BIT_1, Bit.BIT_0)])
def test_repr(code_binaire):
    assert eval(repr(code_binaire)) == code_binaire

@pytest.mark.parametrize("code_binaire, string",
                         [(CodeBinaire(Bit.BIT_0), "0"),
                          (CodeBinaire(Bit.BIT_1), "1"),
                          (CodeBinaire(Bit.BIT_1, Bit.BIT_0), "10"),
                        ])     
def test_str(code_binaire, string):
    assert str(code_binaire) == string

def test_type_erreur():
    with pytest.raises(TypeError):
        CodeBinaire(Bit.BIT_0) + 1

def test_add():
    assert CodeBinaire(Bit.BIT_0) + CodeBinaire(Bit.BIT_1) == CodeBinaire(Bit.BIT_0,Bit.BIT_1)        