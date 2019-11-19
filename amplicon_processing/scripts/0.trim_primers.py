"""Convert read names, trim primers, and intersect forward and reverse files."""

from Bio import SeqIO


def rename_entries(entries):
    """Rename fastq records."""
    for entry_i, entry in enumerate(entries):
        new_id = "read{}".format(entry_i + 1)
        entry.id = new_id
        entry.description = ""
        yield entry


class TrimmedRecords:
    """generator class for iterating through fastq and trimming."""

    def __init__(self, primer, fastq_records, window, max_diffs):
        self.primer = primer
        self.fastq_records = fastq_records
        self.window = window
        self.max_diffs = max_diffs

        self.matching_chars = {('A', 'A'): 1, ('C', 'C'): 1, ('T', 'T'): 1, ('G', 'G'): 1, ('W', 'A'): 1, ('W', 'T'): 1, ('S', 'C'): 1, ('S', 'G'): 1, ('M', 'A'): 1, ('M', 'C'): 1, ('K', 'G'): 1, ('K', 'T'): 1, ('R', 'A'): 1, ('R', 'G'): 1, ('Y', 'C'): 1, ('Y', 'T'): 1, ('B', 'C'): 1, ('B', 'G'): 1, ('B', 'T'): 1, ('D', 'A'): 1, ('D', 'G'): 1, ('D', 'T'): 1, ('H', 'A'): 1, ('H', 'C'): 1, ('H', 'T'): 1, ('V', 'A'): 1, ('V', 'C'): 1, ('V', 'G'): 1, ('N', 'A'): 1, ('N', 'C'): 1, ('N', 'G'): 1, ('N', 'T'): 1}

    def __iter__(self):
        return self

    def __next__(self):
        best_diffs = None
        while best_diffs is None or best_diffs > self.max_diffs:
            record = next(self.fastq_records)
            seq = str(record.seq)
            pl = len(self.primer)

            best_i = None

            for i in range(self.window):
                diffs = self._hamming(seq[i: i + pl])
                if diffs == 0:
                    return record[i + pl:]
                else:
                    if best_diffs is None or diffs < best_diffs:
                        best_diffs = diffs
                        best_i = i

        return record[best_i + pl:]

    def _hamming(self, seq):
        dist = 0
        for pair in zip(self.primer, seq):
            if pair not in self.matching_chars:
                dist += 1

        return dist


def extract_number(header):
    return int(header.lstrip('read').split(";")[0])


class Intersect:
    def __init__(self, for_entries, rev_entries):
        self.for_entries = for_entries
        self.rev_entries = rev_entries

    def __iter__(self):
        return self

    def get_next_for_entry(self):
        self.for_entry = next(self.for_entries)
        self.for_entry_num = extract_number(self.for_entry.id)

    def get_next_rev_entry(self):
        self.rev_entry = next(self.rev_entries)
        self.rev_entry_num = extract_number(self.rev_entry.id)

    def nums(self):
        return [self.for_entry_num, self.rev_entry_num]

    def nums_equal(self):
        return self.for_entry_num == self.rev_entry_num

    def __next__(self):
        self.get_next_for_entry()
        self.get_next_rev_entry()

        while not self.nums_equal():
            if self.for_entry_num < self.rev_entry_num:
                print(self.for_entry_num)
                self.get_next_for_entry()
            elif self.for_entry_num > self.rev_entry_num:
                print(self.rev_entry_num)
                self.get_next_rev_entry()

        assert(self.nums_equal())

        return self.for_entry, self.rev_entry


def main():
    forward_entries = rename_entries(SeqIO.parse(snakemake.input.forward, 'fastq'))
    reverse_entries = rename_entries(SeqIO.parse(snakemake.input.reverse, 'fastq'))
    forward_trimmed = TrimmedRecords(snakemake.params.forward_primer, forward_entries, snakemake.params.window, snakemake.params.max_diffs)
    reverse_trimmed = TrimmedRecords(snakemake.params.reverse_primer, reverse_entries, snakemake.params.window, snakemake.params.max_diffs)
    for_recs, rev_recs = zip(*Intersect(forward_trimmed, reverse_trimmed))
    SeqIO.write(for_recs, snakemake.output.forward, 'fastq')
    SeqIO.write(rev_recs, snakemake.output.reverse, 'fastq')

if __name__ == '__main__':
    main()
