import sys
import re


class PhonoDict(object):
    def __init__(self, word_files=None, pseudoword_files=None):
        self._files = {'dictionaries/cmu/cmudict-0.7b': 'cmu'} if word_files is None else word_files
        self._pseudoword_files = {} if pseudoword_files is None else pseudoword_files

        self._words = {'phonemes':[],
                       'stresses':[],
                       'all':[],
                       'syl_lengths': []}
        self._pwords = {}

        for filename in self._files:
            self._load_word_file(filename, format=self._files[filename])

        for filename in self._pseudoword_files:
            self._load_word_file(filename, format=self._pseudoword_files[filename])

    def _load_word_file(self, filename, format):
        if format == 'cmu':
            self._load_word_file_cmu(filename)
        else:
            raise Exception("Format '%s' not implemented." % (format,))

    def _load_word_file_cmu(self, filename):
        n_words = 0
        print "Reading:  %s ..." % (filename, )
        with open(filename, 'r') as infile:
            for line in infile.readlines():
                line = line.rstrip()
                if line.startswith(';;;'):
                    continue

                parts = re.search('^(.+)  (.+)$', line)

                if not parts:
                    print "\n\nSkipping line:  %s\n" % (line,)
                    continue

                parts = parts.groups()
                word, phone_str = parts[0], parts[1]
                phones = re.findall('([^ ]+)', phone_str)

                v_pos = [i for i, v in enumerate(phones) if v[-1] in ['0', '1', '2']]

                c_pos = [i for i, v in enumerate(phones) if v[-1] not in ['0', '1', '2']]
                stresses = []
                for i, v in enumerate(v_pos):
                    stresses.append(int(phones[v][-1]))
                    phones[v] = phones[v][:-1]


                n_words += 1
                if n_words % 1000 == 0:
                    print "..%i" % (n_words, ),
                    sys.stdout.flush()
        print "\nRead %i words.\n" % (n_words, )

    def create(self, line_patterns, stop_at_n=1):
        pattern = [re.findall('([A-Z]+[^A-Z]+)', line) for line in line_patterns]
        flat_pat = [x for l in pattern for x in l]
        syllables = list(set([re.findall('[A-Z]+', s)[0] for s in flat_pat ]))

        syl_assign = {s: None for s in syllables}
        remainder = []
        poem = []

        # ???

        return poem


if __name__ == "__main__":
    pd = PhonoDict()
    poem_pattern = ["A-B.A-B.C-B.A-B.",
                    "C-D.A-D.A-",
                    "C-D.C-D.EE-D.C-D.",
                    "EE-D.A-D.EE-"]
    poem = pd.create(poem_pattern)
    print "\n".join(poem)