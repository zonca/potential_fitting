avogadro = 6.02214129E+23    # NIST 2010
au_to_ev = 27.21138505       # NIST 2010
au_to_joule = 4.35974434E-18 # NIST 2010
cal_to_joule = 4.184
bohr = 0.52917721067e-10 # meter, 2014 CODATA
bohr_to_ang = bohr * 1.0e10
ang_to_bohr = 1/bohr_to_ang
# derived                                                                      
au_to_kcal = au_to_joule * avogadro * 1E-03 / cal_to_joule
ev_to_kcal = au_to_kcal / au_to_ev
au_per_bohr6_to_kcal_per_ang6 = au_to_kcal * ang_to_bohr ** 6

# atomic symbols ordered from lowest atomic number to highest
atomic_symbols = [
    "H",                                                                                                                                    "He",
    "Li",   "Be",                                                                                   "B",    "C",    "N",    "O",    "F",    "Ne",
    "Na",   "Mg",                                                                                   "Al",   "Si",   "P",    "S",    "Cl",   "Ar",
    "K",    "Ca",   "Sc",   "Ti",   "V",    "Cr",   "Mn",   "Fe",   "Co",   "Ni",   "Cu",   "Zn",   "Ga",   "Ge",   "As",   "Se",   "Br",   "Kr",
]

def symbol_to_number(symbol):
    """
    Converts an atomic symbol to an atomic number
    """

    # Make first letter uppercase and second letter (if exists) lowercase
    symbol = symbol[:1].upper() + symbol[1:].lower()

    try:
        return atomic_symbols.index(symbol) + 1
    except ValueError:
        raise ValueError("{} is not a recognized atomic symbol".format(symbol))

def number_to_symbol(number):
    try:
        if number < 1:
            raise ValueError("{} is not a recognized atomic number".format(number))
        return atomic_symbols[number - 1]
    except IndexError:
        raise ValueError("{} is not a recognized atomic number".format(number))
