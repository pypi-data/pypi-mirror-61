"""Gibson testing."""

import os
import unittest

from Bio.SeqIO import parse
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq

from synbio.assembly import gibson

DIR_NAME = os.path.abspath(os.path.dirname(__file__))
TEST_DIR = os.path.join(DIR_NAME, "..", "..", "data", "gibson")


class TestGibson(unittest.TestCase):
    """Test Gibson class"""

    def test_gibson(self):
        """Create primers for a Gibson assembly."""

        s1 = Seq(
            "GCGTTTTATAGAAGCCTAGGGGAACAGATTGGTCTAATTAGCTTAAGAGAGTAAATTCTGGGATCATTCAGTAGTAATCACAAATTTACGGTGGGGCTTTTTTGGCGGATCTTTACAGATACTAACCAGGTGATTTCAACTAATTTAGTTGACGATTTAGGCGCGCTATCCCGTAATCTTCAAATTAAAACATAGCGTTCCATGAGGGCTAGAATTACTTACCGGCCTTCACCATGCCTGCGTTATTCGCGCCCACTCTCCCATTTATCCGCGCAAGCGGATGCGATGCGATTGCCCGCT"
        )
        s2 = Seq(
            "AAGATATTCTTACGTGTAACGTAGCTAAGTATTCTACAGAGCTGGCGTACGCGTTGAACACTTCACAGATGATAGGGATTCGGGTAAAGAGCGTGTCATTGGGGGCTTATACAGGCGTAGACTACAATGGGCCCAACTCAATCACAGCTCGAGCGCCTTGAATAACATACTCATCTCTATACATTCTCGACAATCTATCGAGCGAGTCGATTATCAACGGGTGTGTTGCAGTTTTAATCTCTTGCCAGCATTGTAATAGCCACCAAGAGATTGATGATAGTCATGGGTGCTGAGCTGAGA"
        )
        s3 = Seq(
            "CGGCGTCGATGCATAGCGGACTTTCGGTCAGTCGCAATTCCTCACGAGACTGGTCCTGTTGTGCGCATCACTCTCAATGTACAAGCAACCCAAGAAGGCTGAGCCTGGACTCAACCGGTTGCTGGGTGAACTCCAGACTCGGGGCGACAACTCTTCATACATAGAGCAAGGGCGTCGAACGGTCGTGAAAGTCTTAGTACCGCACGTACCAACTTACTGAGGATATTGCCTGAAGCTGTACCGTTTTAGGGGGGGAAGGTTGAAGATCTCCTCTTCTCATGACTGAACTCGCGAGGGCCG"
        )
        r1 = SeqRecord(s1)
        r2 = SeqRecord(s2)
        r3 = SeqRecord(s3)

        self._run_and_verify([r1, r2, r3])

    def test_gibson_offtarget_primer(self):
        """Create Gibson primers when there's offtarget in one's end (1)."""

        s1 = Seq(  # GCGTTTTATAGAAGCCTAGGGGAAC shows up twice
            "GCGTTTTATAGAAGCCTAGGGGAACAGATTGGTCTAATTAGCTTAAGAGAGTAAATGGCGTTTTATAGAAGCCTAGGGGAACCTGGGATCATTCAGTAGTAATCACAAATTTACGGTGGGGCTTTTTTGGCGGATCTTTACAGATACTAACCAGGTGATTTCAACTAATTTAGTTGACGATTTAGGCGCGCTATCCCGTAATCTTCAAATTAAAACATAGCGTTCCATGAGGGCTAGAATTACTTACCGGCCTTCACCATGCCTGCGTTATTCGCGCCCACTCTCCCATTTATCCGCGCAAGCGGATGCGATGCGATTGCCCGCT"
        )
        s2 = Seq(
            "AAGATATTCTTACGTGTAACGTAGCTAAGTATTCTACAGAGCTGGCGTACGCGTTGAACACTTCACAGATGATAGGGATTCGGGTAAAGAGCGTGTCATTGGGGGCTTATACAGGCGTAGACTACAATGGGCCCAACTCAATCACAGCTCGAGCGCCTTGAATAACATACTCATCTCTATACATTCTCGACAATCTATCGAGCGAGTCGATTATCAACGGGTGTGTTGCAGTTTTAATCTCTTGCCAGCATTGTAATAGCCACCAAGAGATTGATGATAGTCATGGGTGCTGAGCTGAGA"
        )
        s3 = Seq(
            "CGGCGTCGATGCATAGCGGACTTTCGGTCAGTCGCAATTCCTCACGAGACTGGTCCTGTTGTGCGCATCACTCTCAATGTACAAGCAACCCAAGAAGGCTGAGCCTGGACTCAACCGGTTGCTGGGTGAACTCCAGACTCGGGGCGACAACTCTTCATACATAGAGCAAGGGCGTCGAACGGTCGTGAAAGTCTTAGTACCGCACGTACCAACTTACTGAGGATATTGCCTGAAGCTGTACCGTTTTAGGGGGGGAAGGTTGAAGATCTCCTCTTCTCATGACTGAACTCGCGAGGGCCG"
        )
        r1 = SeqRecord(s1)
        r2 = SeqRecord(s2)
        r3 = SeqRecord(s3)

        self._run_and_verify([r1, r2, r3])

    def test_gibson_offtarget_primer2(self):
        """Create Gibson primers when there's offtarget in one's end (2)."""

        insert = next(parse(os.path.join(TEST_DIR, "BBa_K1649003.fa"), "fasta"))
        backbone = next(parse(os.path.join(TEST_DIR, "pDusk.fa"), "fasta"))

        plasmid, primer_pairs = gibson([insert, backbone])

        self.assertTrue(plasmid and primer_pairs)

    def _run_and_verify(self, records):
        """Verify the primers and plasmid sequence are correct."""

        plasmid, primer_pairs = gibson(records)

        doubled_seq = "".join(str(r.seq) for r in records + records)
        self.assertIsInstance(plasmid, SeqRecord)
        self.assertIn(str(plasmid.seq), doubled_seq)

        for i, primers in enumerate(primer_pairs):
            # primers' sequences are in the final plasmid
            self.assertIn(primers.fwd, plasmid.seq)
            self.assertIn(primers.rev.reverse_complement(), plasmid.seq + plasmid.seq)

            record = records[i]
            self.assertIn(primers.fwd[-15:], record.seq)
            self.assertIn(primers.rev[-15:].reverse_complement(), record.seq)

        return plasmid, primer_pairs
