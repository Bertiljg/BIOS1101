# transcribe function
def transcribe(dna):
    """
    Translate a DNA string to its corresponding mRNA
    """
    rna = dna.replace("T", "U")
    return rna

# translate function
def translate(mRNA):
    """
    Translate a mRNA string to a protein.
    """

    codon_dict = {
        "UUU": "F", "UUC": "F", "UUA": "L", "UUG": "L",
        "UCU": "S", "UCC": "S", "UCA": "S", "UCG": "S",
        "UAU": "Y", "UAC": "Y", "UAA": "*", "UAG": "*",
        "UGU": "C", "UGC": "C", "UGA": "*", "UGG": "W",
        "CUU": "L", "CUC": "L", "CUA": "L", "CUG": "L",
        "CCU": "P", "CCC": "P", "CCA": "P", "CCG": "P",
        "CAU": "H", "CAC": "H", "CAA": "Q", "CAG": "Q",
        "CGU": "R", "CGC": "R", "CGA": "R", "CGG": "R",
        "AUU": "I", "AUC": "I", "AUA": "I", "AUG": "M",
        "ACU": "T", "ACC": "T", "ACA": "T", "ACG": "T",
        "AAU": "N", "AAC": "N", "AAA": "K", "AAG": "K",
        "AGU": "S", "AGC": "S", "AGA": "R", "AGG": "R",
        "GUU": "V", "GUC": "V", "GUA": "V", "GUG": "V",
        "GCU": "A", "GCC": "A", "GCA": "A", "GCG": "A",
        "GAU": "D", "GAC": "D", "GAA": "E", "GAG": "E",
        "GGU": "G", "GGC": "G", "GGA": "G", "GGG": "G"
    }

    index = mRNA.index("AUG")
    protein = ""
    amino_acid = ""
    while amino_acid != "*" and index < len(mRNA):
        # Convert a codon to an amino acid
        # and add it to our protein
        codon = mRNA[index:index + 3]
        # The last slice of the string may be shorter
        # if the length of the sequence to translate is not a multiple of 3 bases.
        # We thus need to check that the codon is 3 nucleotides.
        if len(codon) == 3:
            amino_acid = codon_dict[codon]
            protein += amino_acid
        index += 3

    return protein


# read FASTA function
def load_fasta(filename):
    """
    Load a FASTA file and return the sequence as a string.
    """
    f = open(filename, "r")
    lines = f.readlines()
    f.close()

    mRNA = ""
    for line in lines[1:]:
        mRNA += line.strip()

    return mRNA


def load_fastq_sequences(filename):
    """
    Read a FASTQ file and return the sequences as a list.
    """
    f = open(filename, "r")
    lines = f.readlines()
    f.close()

    sequences = []

    for i in range(len(lines)):
        line = lines[i].strip()

        if i % 4 == 1:
            sequences.append(line)

    return sequences


def fastq_to_fasta_text(filename):
    """
    Read a FASTQ file and return the sequences as FASTA text.
    """
    sequences = load_fastq_sequences(filename)

    fasta_text = ""
    read_number = 1

    for sequence in sequences:
        fasta_text += f">read_{read_number}\n"
        fasta_text += sequence + "\n"
        read_number += 1

    return fasta_text


def write_text_to_file(text, filename="reads_from_fastq.fasta"):
    """
    Write text to a file.
    """
    f = open(filename, "w")
    f.write(text)
    f.close()
