from typing import Generator
from rest_framework import serializers

DNA_BASE_PAIRS = {
    'T': 'A',
    'A': 'T',
    'C': 'G',
    'G': 'C',
    'N': '-',
    '-': 'N'
}

RNA_BASE_PAIRS = {
    'T': 'A',
    'A': 'U',
    'C': 'G',
    'G': 'C',
}

AMINOACID_PAIRS = {
    'UUU': 'F',
    'UUC': 'F',
    'UUA': 'L',
    'UUG': 'L',
    'UCU': 'S',
    'UCC': 'S',
    'UCA': 'S',
    'UCG': 'S',
    'UAU': 'Y',
    'UAC': 'Y',
    'UAA': '*',
    'UAG': '*',
    'UGU': 'C',
    'UGC': 'C',
    'UGA': '*',
    'UGG': 'W',
    'CUU': 'L',
    'CUC': 'L',
    'CUA': 'L',
    'CUG': 'L',
    'CCU': 'P',
    'CCC': 'P',
    'CCA': 'P',
    'CCG': 'P',
    'CAU': 'H',
    'CAC': 'H',
    'CAA': 'Q',
    'CAG': 'Q',
    'CGU': 'R',
    'CGC': 'R',
    'CGA': 'R',
    'CGG': 'R',
    'AUU': 'I',
    'AUC': 'I',
    'AUA': 'I',
    'AUG': 'M',
    'ACU': 'T',
    'ACC': 'T',
    'ACA': 'T',
    'ACG': 'T',
    'AAU': 'N',
    'AAC': 'N',
    'AAA': 'K',
    'AAG': 'K',
    'AGU': 'S',
    'AGC': 'S',
    'AGA': 'R',
    'AGG': 'R',
    'GUU': 'V',
    'GUC': 'V',
    'GUA': 'V',
    'GUG': 'V',
    'GCU': 'A',
    'GCC': 'A',
    'GCA': 'A',
    'GCG': 'A',
    'GAU': 'D',
    'GAC': 'D',
    'GAA': 'E',
    'GAG': 'E',
    'GGU': 'G',
    'GGC': 'G',
    'GGA': 'G',
    'GGG': 'G',
}

AMINOACID_DICT = {
    'F': 'Phenylalanine',
    'L': 'Leucine',
    'S': 'Serine',
    'Y': 'Tyrosine',
    '*': 'Stop',
    'C': 'Cysteine',
    'W': 'Tryptophan',
    'P': 'Proline',
    'H': 'Histidine',
    'Q': 'Glutamine',
    'R': 'Arginine',
    'I': 'Isoleucine',
    'M': 'Methionine',
    'T': 'Threonine',
    'N': 'Asparagine',
    'K': 'Lysine',
    'V': 'Valine',
    'A': 'Alanine',
    'D': 'Aspartic acid',
    'E': 'Glutamic acid',
    'G': 'Glycine',
}

ESSENTIAL_AMINOACIDS = ['Tryptophan', 'Threonine', 'Valine', 'Lysine',
                        'Isoleucine', 'Leucine', 'Methionine', 'Histidine', 'Phenylalanine']


class ProteinSerializer(serializers.Serializer):
    protein_string = serializers.CharField(max_length=65536)

    def validate(self, data):
        """Check credentials."""
        protein_string = data['protein_string']
        if not protein_string:
            raise serializers.ValidationError('Invalid protein string')
        return data

    def create(self, data):
        """Process a new protein."""
        protein_string = data['protein_string'].upper().replace(' ', '')
        aminoacids = [AMINOACID_DICT[base] for base in protein_string]
        essentials = {i: aminoacids.count(i) for i in ESSENTIAL_AMINOACIDS}
        return {
            'protein_string': protein_string,
            'aminoacids': aminoacids,
            'essentials': essentials
        }


class DNASerializer(serializers.Serializer):
    dna_string = serializers.CharField(max_length=65536)

    def group_by_3(self, s: str) -> Generator[str, None, None]:
        for i in range(len(s)):
            if i % 3 == 0:
                yield s[i:i+3]

    def validate(self, data):
        """Check credentials."""
        dna_string = data['dna_string']
        if not dna_string:
            raise serializers.ValidationError('Invalid DNA string')
        return data

    def read_dna_string(self, dna_string):
        dna_complement = ''.join([DNA_BASE_PAIRS[base] for base in dna_string])
        rna_string = ''.join([RNA_BASE_PAIRS[base] for base in dna_complement])
        protein = ''.join([AMINOACID_PAIRS[base] for base in self.group_by_3(rna_string)])
        return {
            'dna_string': dna_string,
            'dna_complement': dna_complement,
            'rna_string': rna_string,
            'aminoacids': [AMINOACID_DICT[base] for base in protein],
            'protein': protein
        }

    def create(self, data):
        dna_complement = ''.join([DNA_BASE_PAIRS[base] for base in data['dna_string']])
        reverse_complement = dna_complement[::-1]
        return {
            'forward': {
                'frame_1': self.read_dna_string(data['dna_string']),
                'frame_2': self.read_dna_string(data['dna_string'][1:len(data['dna_string'])-2]),
                'frame_3': self.read_dna_string(data['dna_string'][2:len(data['dna_string'])-1]),
            },
            'reverse': {
                'frame_1': self.read_dna_string(reverse_complement),
                'frame_2': self.read_dna_string(reverse_complement[1:len(dna_complement)-2]),
                'frame_3': self.read_dna_string(reverse_complement[2:len(dna_complement)-1]),
            }
        }
