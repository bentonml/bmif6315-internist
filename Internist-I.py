# internist-i project
# mary lauren benton, annika faucon, kim kondratieff, patrick wu
# bmif 6315 | spring 2018

###
#   libraries & arguments
###
import sys
import re
import argparse

arg_parser = argparse.ArgumentParser(description="Run the Internist-I algorithm. Runs interactively by default.")
arg_parser.add_argument("-i", "--infile", type=str, help='input file name')

# save parameters
args = arg_parser.parse_args()
INPUT_FILENAME = args.infile


###
#   classes
###
class Disease():
    def __init__(self, idx=-1, name=''):
        self.idx  = idx   # disease number
        self.name = name  # disease name
        self.mx   = []    # assoc. manifestations
        self.link = []    # linked diseases

    def __str__(self):
        return '{}: {} | # mx = {}, # link = {}'.format(self.idx, self.name,
                                                        len(self.mx), len(self.link))
    # get functions
    def get_idx(self):   return self.idx
    def get_name(self):  return self.name
    def get_mxs(self):   return self.mx
    def get_links(self): return self.link

    def get_mx_idxs(self):
        return [m.get_idx() for m in self.mx]

    # print manifestations
    def print_mxs(self):
        return [print(mx) for mx in self.mx]

    # add functions
    def add_mx(self, new_mx):
        self.mx.append(new_mx)

    def add_link(self, new_link):
        self.link.append(new_link)

    # is_in functions
    def has_manifestation(self, pt_m):
        for m in self.mx:
            if m.get_idx() == pt_m: return True
        return False


class Manifestation():
    def __init__(self, idx=-1, name='', es=-1, fq=-1, im=-1):
        self.idx  = idx   # mx number
        self.name = name  # mx name
        self.es   = es    # evoking strength
        self.fq   = fq    # frequency
        self.im   = im    # import

    def __eq__(self, other):
        return self.idx == other.idx

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return '{}: {} | es = {}, fq = {}, im = {}'.format(self.idx, self.name,
                                                           self.es, self.fq, self.im)

    # get functions
    def get_idx(self):  return self.idx
    def get_name(self): return self.name
    def get_es(self):   return self.es
    def get_fq(self):   return self.fq
    def get_im(self):   return self.im

    # nonlinear transformations
    def get_trans_es(self):
        trans = {'0': 1, '1': 4, '2': 10, '3': 20, '4': 40, '5': 80}
        return trans[self.es]

    def get_trans_fq(self):
        trans = {'1': -1, '2': -4, '3': -7, '4': -15, '5': -30}
        return trans[self.fq]

    def get_trans_im(self):
        trans = {'1': -2, '2': -6, '3': -10, '4': -20, '5': -40}
        return trans[self.im]

    # set functions
    def set_es(self, new_es):
        self.es = new_es
    def set_fq(self, new_fq):
        self.fq = new_fq
    def set_im(self, new_im):
        self.im = new_im


class Patient():
    def __init__(self, pos=None, neg=None):
        self.positive = pos  # + findings
        self.negative = neg  # - findings

    # get functions
    def get_positives(self): return self.positive
    def get_negatives(self): return self.negative

    # add functions
    def add_positive(self, new_pos):
        self.positive.append(new_pos)

    def add_negative(self, new_neg):
        self.negative.append(new_neg)


###
#   functions
###
def parse_disease(line):
    return line[1], ' '.join(line[2:])

def parse_manifestation(line):
    return line[2], ' '.join(line[3:]), line[1][0], line[1][1]

def parse_link(line):
    return line[3], ' '.join(line[4:])

def parse_even(line):
    return line[1], ' '.join(line[2:])

def parse_odd(line):
    return line[0], line[2]

def read_findings_file():
    FINDINGS = {}
    with open('./data/findings.txt', 'r') as fd_file:
        for i, line in enumerate(fd_file):
            line = line.strip('\n').split()
            if i % 2:
                idx, imp = parse_odd(line)
                FINDINGS[idx].set_im(imp)
            else:
                idx, name = parse_even(line)
                FINDINGS[idx] = Manifestation(idx, name)
    return FINDINGS

def read_diseases_file(FINDINGS):
    DISEASES = {}
    with open('./data/diseases.txt', 'r') as dz_file:
        for line in dz_file:
            if line != '\n':
                line = line.strip('\n').split()
                if line[0] == 'DX':
                    dz_idx, name = parse_disease(line)
                    DISEASES[dz_idx] = Disease(dz_idx, name)
                elif line[0] == 'MX':
                    idx, name, es, fq = parse_manifestation(line)
                    DISEASES[dz_idx].add_mx(Manifestation(idx, name, es, fq, FINDINGS[idx].get_im()))
                elif line[0] == 'LINK':
                    idx, name = parse_link(line)
                    DISEASES[dz_idx].add_link((idx, name))
    return DISEASES

def map_name_to_id(findings, mx_name):
    mapped_idx = None
    mx_name = re.sub('[<>]', '', mx_name)
    for idx, mx in findings.items():
        if mx.get_name() == mx_name.upper():
            mapped_idx = idx
    return mapped_idx

def from_file(INPUT_FILENAME, FINDINGS):
    PATIENT = Patient([], [])
    with open(INPUT_FILENAME, 'r') as pt_file:
        for line in pt_file:
            line = line.strip('\n').split()
            if line[0] == '+':
                mx_idx = map_name_to_id(FINDINGS, ' '.join(line[1:]))
                PATIENT.add_positive(mx_idx)
            elif line[0] == '-':
                mx_idx = map_name_to_id(FINDINGS, ' '.join(line[1:]))
                PATIENT.add_negative(mx_idx)
            else:
                print('Input line with error: {}'.format(' '.join(line)))
                sys.exit(1)
    return PATIENT

def from_stdin(FINDINGS):
    PATIENT = Patient([], [])
    print('Input manifestations (preceded by + for positive and - for negative):')
    for line in sys.stdin:
        line = line.strip('\n').split()
        print(line)
        if line[0] == '+':
            mx_idx = map_name_to_id(FINDINGS, ' '.join(line[1:]))
            PATIENT.add_positive(mx_idx)
        elif line[0] == '-':
            mx_idx = map_name_to_id(FINDINGS, ' '.join(line[1:]))
            PATIENT.add_negative(mx_idx)
        elif line[0] == '$':
            break
    return PATIENT

def build_disease_hyp(PATIENT, DISEASES):
    DDX_HYP  = {}
    for pos_finding in PATIENT.get_positives():
        for idx, dz in DISEASES.items():
            if dz.has_manifestation(pos_finding):
                DDX_HYP[idx] = None
    return DDX_HYP

def calculate_score(idx, PATIENT, FINDINGS, DISEASES):
    score = 0
    for mx in DISEASES[idx].get_mxs():
        if mx.get_idx() in PATIENT.get_positives():
            score += mx.get_trans_es()
        elif mx.get_idx() in PATIENT.get_negatives():
            score += mx.get_trans_fq()
    for pt_mx_idx in PATIENT.get_positives():
        if pt_mx_idx not in DISEASES[idx].get_mx_idxs():
            score += FINDINGS[pt_mx_idx].get_trans_im()
    return score

def create_ddx(FINAL_DDX, DISEASES):
    if len(FINAL_DDX) == 0:
        print('No diagnosis found.')
    elif len(FINAL_DDX) == 1:
        print('Most likely diagnosis is {} with score of {}.'.format(DISEASES[FINAL_DDX[0][0]].get_name(),
                                                                    FINAL_DDX[0][1]))
    elif (FINAL_DDX[0][1] - FINAL_DDX[1][1]) >= 90:
        print('Most likely diagnosis is {} with score of {}.'.format(DISEASES[FINAL_DDX[0][0]].get_name(),
                                                                    FINAL_DDX[0][1]))
    else:
        print('Set of most likely diagnoses, ranked by score:\n')
        print_final_ddx(DISEASES, FINAL_DDX)

def print_final_ddx(diseases, final_ddx):
    for dx in final_ddx:
        print('{} (score: {})'.format(diseases[dx[0]].get_name(), dx[1]))


###
#   main
###
def main(argv):

    FINDINGS = read_findings_file()  # manifestations from findings (#, NAME, IM)
    DISEASES = read_diseases_file(FINDINGS)  # diseases (#, NAME, MX, LINKS)

    # read from stdin or patient file
    if INPUT_FILENAME:
        PATIENT = from_file(INPUT_FILENAME, FINDINGS)
    else:
        PATIENT = from_stdin(FINDINGS)

    # pull each possible dx_hyp from disease list (based on +MX)
    DDX_HYP = build_disease_hyp(PATIENT, DISEASES)

    # calculate score for each dx_hyp
    for idx in DDX_HYP:
        DDX_HYP[idx] = calculate_score(idx, PATIENT, FINDINGS, DISEASES)

    # choose optimal ddx or return list in order
    create_ddx(sorted(DDX_HYP.items(), key=lambda x:x[1], reverse=True), DISEASES)


if __name__ == "__main__":
    main(sys.argv)
