def reverse_complement(seq):
    """
    Returns the reverse complement of a DNA string.
    Assumes that the input DNA string
    only consists of the four characters 'A', 'C', 'G' and 'T'.
    """
    complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
    rev_comp = ''
    for base in seq[::-1]:
        rev_comp += complement[base]
    return rev_comp
