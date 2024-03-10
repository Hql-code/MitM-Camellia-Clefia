from utils import *
from gurobipy import *
import os

class Vars_generator:
    @staticmethod
    def genVars_input_of_round(i, r, pos):
        return [f'IP_{i}_r{r}_{pos}_{j}' for j in range(bs)]

    @staticmethod
    def genVars_IP_isWhite(r, pos):
        return [f'IP_isWhite_r{r}_{pos}_{j}' for j in range(bs)]

    @staticmethod
    def genVars_SupP_Blue_input_of_round(i, r, pos):
        return [f'IP_SupP_Blue_{i}_r{r}_{pos}_{j}' for j in range(bs)]

    @staticmethod
    def genVars_SupP_Red_input_of_round(i, r, pos):
        return [f'IP_SupP_Red_{i}_r{r}_{pos}_{j}' for j in range(bs)]

    @staticmethod
    def genVars_input_of_MixColumns(i, r):
        return [f'IMC_{i}_r{r}_{j}' for j in range(bs)]

    @staticmethod
    def genVars_input_of_MixColumns_isWhite(r):
        return [f'IMC_isWhite_r{r}_{j}' for j in range(bs)]

    @staticmethod
    def genVars_SupP_Blue_input_of_MixColumns(i, r):
        return [f'IMC_SupP_Blue_{i}_r{r}_{j}' for j in range(bs)]

    @staticmethod
    def genVars_SupP_Red_input_of_MixColumns(i, r):
        return [f'IMC_SupP_Red_{i}_r{r}_{j}' for j in range(bs)]

    @staticmethod
    def genVars_OXor_SupP_Blue_isWhite(r):
        return [f'OXor_SupP_Blue_isWhite_r{r}_{j}' for j in range(bs)]

    @staticmethod
    def genVars_OXor_SupP_Red_isWhite(r):
        return [f'OXor_SupP_Red_isWhite_r{r}_{j}' for j in range(bs)]

    @staticmethod
    def genVars_Xor_ConsumedDeg_Blue(r):
        return [f'CD_Xor_Blue_r{r}_{j}' for j in range(bs)]

    @staticmethod
    def genVars_Xor_ConsumedDeg_Red(r):
        return [f'CD_Xor_Red__r{r}_{j}' for j in range(bs)]

    @staticmethod
    def genVars_MC_SupP_Blue_SumGray(r):
        return [f'G_SupP_Blue_SumGray_r{r}_{j}' for j in range(bs)]

    @staticmethod
    def genVars_MC_SupP_Red_SumGray(r):
        return [f'G_SupP_Red_SumGray_r{r}_{j}' for j in range(bs)]

    @staticmethod
    def genVars_OXor_SupP_Blue_AND(i, r):
        return [f'OXor_SupP_Blue_AND_{i}_r{r}_{j}' for j in range(bs)]

    @staticmethod
    def genVars_OXor_SupP_Red_AND(i, r):
        return [f'OXor_SupP_Red_AND_{i}_r{r}_{j}' for j in range(bs)]

    # Initial Degree
    @staticmethod
    def genVars_degree__forward():
        return ['deg_f_' + str(j) for j in range(bs * b)]

    @staticmethod
    def genVars_degree_backward():
        return ['deg_b_' + str(j) for j in range(bs * b)]

    # Match
    @staticmethod
    def genVars_Match_Counter():
        return [f'Match_Counter_{j}' for j in range(bs * 16)]

    @staticmethod
    def genVars_Match_input():
        return [f'Match_input_{j}' for j in range(bs * 16)]

    @staticmethod
    def genVars_Match_output():
        return [f'Match_output_{j}' for j in range(bs * 16)]


class Constraints_generator:
    def __init__(self, total_round):
        self.ini_r = 0
        self.TR = total_round
        self.pos2 = ['L', 'R']

    def genConstraints_initial_degree(self):
        cons = []
        d1 = Vars_generator.genVars_degree__forward()
        d2 = Vars_generator.genVars_degree_backward()
        IP_1 = []
        IP_2 = []
        IP_SupP_Blue_1 = []
        IP_SupP_Blue_2 = []
        IP_SupP_Red_1 = []
        IP_SupP_Red_2 = []
        IP_isWhite = []
        for pos in self.pos2:
            IP_1 = IP_1 + Vars_generator.genVars_input_of_round(1, self.ini_r, pos)
            IP_2 = IP_2 + Vars_generator.genVars_input_of_round(2, self.ini_r, pos)
            IP_SupP_Blue_1 = IP_SupP_Blue_1 + Vars_generator.genVars_SupP_Blue_input_of_round(1, self.ini_r, pos)
            IP_SupP_Blue_2 = IP_SupP_Blue_2 + Vars_generator.genVars_SupP_Blue_input_of_round(2, self.ini_r, pos)
            IP_SupP_Red_1 = IP_SupP_Red_1 + Vars_generator.genVars_SupP_Red_input_of_round(1, self.ini_r, pos)
            IP_SupP_Red_2 = IP_SupP_Red_2 + Vars_generator.genVars_SupP_Red_input_of_round(2, self.ini_r, pos)
            IP_isWhite = IP_isWhite + Vars_generator.genVars_IP_isWhite(self.ini_r, pos)
        for bi in range(bs * b):
            cons = cons + [IP_1[bi] + ' + ' + IP_2[bi] + ' >= 1']
            cons = cons + [d1[bi] + ' + ' + IP_2[bi] + ' = 1']
            cons = cons + [d2[bi] + ' + ' + IP_1[bi] + ' = 1']
        for bi in range(bs * b):
            cons = cons + MITMPreConstraints.Separate_Without_Guess_i(
                IP_1[bi],
                IP_2[bi],
                IP_SupP_Blue_1[bi],
                IP_SupP_Blue_2[bi],
                IP_SupP_Red_1[bi],
                IP_SupP_Red_2[bi],
                IP_isWhite[bi]
            )
        return cons

    def genConstraints_forward_round(self, r):
        cons = []
        IP_SupP_Blue_1 = []
        IP_SupP_Blue_2 = []
        IP_SupP_Red_1 = []
        IP_SupP_Red_2 = []
        IP_nextr_SupP_Blue_1 = []
        IP_nextr_SupP_Blue_2 = []
        IP_nextr_SupP_Red_1 = []
        IP_nextr_SupP_Red_2 = []
        IP_inir_SupP_Blue_1 = []
        IP_inir_SupP_Blue_2 = []
        IP_inir_SupP_Red_1 = []
        IP_inir_SupP_Red_2 = []
        for pos in self.pos2:
            IP_SupP_Blue_1.append(Vars_generator.genVars_SupP_Blue_input_of_round(1, r, pos))
            IP_SupP_Blue_2.append(Vars_generator.genVars_SupP_Blue_input_of_round(2, r, pos))
            IP_SupP_Red_1.append(Vars_generator.genVars_SupP_Red_input_of_round(1, r, pos))
            IP_SupP_Red_2.append(Vars_generator.genVars_SupP_Red_input_of_round(2, r, pos))
            IP_nextr_SupP_Blue_1.append(Vars_generator.genVars_SupP_Blue_input_of_round(1, r + 1, pos))
            IP_nextr_SupP_Blue_2.append(Vars_generator.genVars_SupP_Blue_input_of_round(2, r + 1, pos))
            IP_nextr_SupP_Red_1.append(Vars_generator.genVars_SupP_Red_input_of_round(1, r + 1, pos))
            IP_nextr_SupP_Red_2.append(Vars_generator.genVars_SupP_Red_input_of_round(2, r + 1, pos))
            IP_inir_SupP_Blue_1.append(Vars_generator.genVars_SupP_Blue_input_of_round(1, 0, pos))
            IP_inir_SupP_Blue_2.append(Vars_generator.genVars_SupP_Blue_input_of_round(2, 0, pos))
            IP_inir_SupP_Red_1.append(Vars_generator.genVars_SupP_Red_input_of_round(1, 0, pos))
            IP_inir_SupP_Red_2.append(Vars_generator.genVars_SupP_Red_input_of_round(2, 0, pos))

        IMC_1 = Vars_generator.genVars_input_of_MixColumns(1, r)
        IMC_2 = Vars_generator.genVars_input_of_MixColumns(2, r)
        for bi in range(bs):
            cons = cons + MITMPreConstraints.Determine_Allone([IP_SupP_Blue_1[0][bi], IP_SupP_Red_1[0][bi]], IMC_1[bi])
            cons = cons + MITMPreConstraints.Determine_Allone([IP_SupP_Blue_2[0][bi], IP_SupP_Red_2[0][bi]], IMC_2[bi])

        # Separate
        IMC_SupP_Blue_1 = Vars_generator.genVars_SupP_Blue_input_of_MixColumns(1, r)
        IMC_SupP_Blue_2 = Vars_generator.genVars_SupP_Blue_input_of_MixColumns(2, r)
        IMC_SupP_Red_1 = Vars_generator.genVars_SupP_Red_input_of_MixColumns(1, r)
        IMC_SupP_Red_2 = Vars_generator.genVars_SupP_Red_input_of_MixColumns(2, r)
        IMC_isWhite = Vars_generator.genVars_input_of_MixColumns_isWhite(r)
        for bi in range(bs):
            cons = cons + MITMPreConstraints.Separate_Without_Guess_i(
                IMC_1[bi],
                IMC_2[bi],
                IMC_SupP_Blue_1[bi],
                IMC_SupP_Blue_2[bi],
                IMC_SupP_Red_1[bi],
                IMC_SupP_Red_2[bi],
                IMC_isWhite[bi]
            )
        # nXor
        CD_Xor_Blue = Vars_generator.genVars_Xor_ConsumedDeg_Blue(r)
        SumGray_SupP_Blue = Vars_generator.genVars_MC_SupP_Blue_SumGray(r)
        OXor_SupP_Blue_isWhite = Vars_generator.genVars_OXor_SupP_Blue_isWhite(r)
        OXor_SupP_Blue_AND_2 = Vars_generator.genVars_OXor_SupP_Blue_AND(2, r)
        CD_Xor_Red = Vars_generator.genVars_Xor_ConsumedDeg_Red(r)
        SumGray_SupP_Red = Vars_generator.genVars_MC_SupP_Red_SumGray(r)
        OXor_SupP_Red_isWhite = Vars_generator.genVars_OXor_SupP_Red_isWhite(r)
        OXor_SupP_Red_AND_1 = Vars_generator.genVars_OXor_SupP_Red_AND(1, r)
        if r not in [1, 2]:
            for bi in range(bs):
                cons = cons + MITMPreConstraints.genConstraints_of_nXor_SupP_Blue_i(
                    Perm_Camellia(bi, IMC_SupP_Blue_1) + [IP_SupP_Blue_1[1][bi]],
                    Perm_Camellia(bi, IMC_SupP_Blue_2) + [IP_SupP_Blue_2[1][bi]],
                    IP_nextr_SupP_Blue_1[0][bi],
                    IP_nextr_SupP_Blue_2[0][bi],
                    CD_Xor_Blue[bi],
                    SumGray_SupP_Blue[bi],
                    OXor_SupP_Blue_isWhite[bi],
                    OXor_SupP_Blue_AND_2[bi]
                )
                cons = cons + MITMPreConstraints.genConstraints_of_nXor_SupP_Red_i(
                    Perm_Camellia(bi, IMC_SupP_Red_1) + [IP_SupP_Red_1[1][bi]],
                    Perm_Camellia(bi, IMC_SupP_Red_2) + [IP_SupP_Red_2[1][bi]],
                    IP_nextr_SupP_Red_1[0][bi],
                    IP_nextr_SupP_Red_2[0][bi],
                    CD_Xor_Red[bi],
                    SumGray_SupP_Red[bi],
                    OXor_SupP_Red_isWhite[bi],
                    OXor_SupP_Red_AND_1[bi]
                )
        elif r == 1:
            for bi in range(bs):
                cons = cons + MITMPreConstraints.genConstraints_of_nXor_SupP_Blue_i(
                    Perm_Camellia(bi, IMC_SupP_Blue_1) + [IP_SupP_Blue_1[1][bi], IP_inir_SupP_Blue_1[0][bi]],
                    Perm_Camellia(bi, IMC_SupP_Blue_2) + [IP_SupP_Blue_2[1][bi], IP_inir_SupP_Blue_2[0][bi]],
                    IP_nextr_SupP_Blue_1[0][bi],
                    IP_nextr_SupP_Blue_2[0][bi],
                    CD_Xor_Blue[bi],
                    SumGray_SupP_Blue[bi],
                    OXor_SupP_Blue_isWhite[bi],
                    OXor_SupP_Blue_AND_2[bi]
                )
                cons = cons + MITMPreConstraints.genConstraints_of_nXor_SupP_Red_i(
                    Perm_Camellia(bi, IMC_SupP_Red_1) + [IP_SupP_Red_1[1][bi], IP_inir_SupP_Red_1[0][bi]],
                    Perm_Camellia(bi, IMC_SupP_Red_2) + [IP_SupP_Red_2[1][bi], IP_inir_SupP_Red_2[0][bi]],
                    IP_nextr_SupP_Red_1[0][bi],
                    IP_nextr_SupP_Red_2[0][bi],
                    CD_Xor_Red[bi],
                    SumGray_SupP_Red[bi],
                    OXor_SupP_Red_isWhite[bi],
                    OXor_SupP_Red_AND_1[bi]
                )
        elif r == 2:
            for bi in range(bs):
                cons = cons + MITMPreConstraints.genConstraints_of_nXor_SupP_Blue_i(
                    Perm_Camellia(bi, IMC_SupP_Blue_1) + [IP_SupP_Blue_1[1][bi], IP_inir_SupP_Blue_1[1][bi]],
                    Perm_Camellia(bi, IMC_SupP_Blue_2) + [IP_SupP_Blue_2[1][bi], IP_inir_SupP_Blue_2[1][bi]],
                    IP_nextr_SupP_Blue_1[0][bi],
                    IP_nextr_SupP_Blue_2[0][bi],
                    CD_Xor_Blue[bi],
                    SumGray_SupP_Blue[bi],
                    OXor_SupP_Blue_isWhite[bi],
                    OXor_SupP_Blue_AND_2[bi]
                )
                cons = cons + MITMPreConstraints.genConstraints_of_nXor_SupP_Red_i(
                    Perm_Camellia(bi, IMC_SupP_Red_1) + [IP_SupP_Red_1[1][bi], IP_inir_SupP_Red_1[1][bi]],
                    Perm_Camellia(bi, IMC_SupP_Red_2) + [IP_SupP_Red_2[1][bi], IP_inir_SupP_Red_2[1][bi]],
                    IP_nextr_SupP_Red_1[0][bi],
                    IP_nextr_SupP_Red_2[0][bi],
                    CD_Xor_Red[bi],
                    SumGray_SupP_Red[bi],
                    OXor_SupP_Red_isWhite[bi],
                    OXor_SupP_Red_AND_1[bi]
                )

        # Link
        cons = cons + MITMPreConstraints.equalConstraints(IP_SupP_Blue_1[0], IP_nextr_SupP_Blue_1[1])
        cons = cons + MITMPreConstraints.equalConstraints(IP_SupP_Blue_2[0], IP_nextr_SupP_Blue_2[1])
        cons = cons + MITMPreConstraints.equalConstraints(IP_SupP_Red_1[0], IP_nextr_SupP_Red_1[1])
        cons = cons + MITMPreConstraints.equalConstraints(IP_SupP_Red_2[0], IP_nextr_SupP_Red_2[1])
        return cons

    def genConstraints_Match(self):
        cons = []
        Match_Counter = Vars_generator.genVars_Match_Counter()
        Match_input = Vars_generator.genVars_Match_input()
        Match_output = Vars_generator.genVars_Match_output()
        IP_inir_SupP_Blue_1 = []
        IP_lastr_SupP_Blue_1 = []
        for pos in self.pos2:
            IP_inir_SupP_Blue_1 = IP_inir_SupP_Blue_1 + Vars_generator.genVars_SupP_Blue_input_of_round(1, self.ini_r, pos)
            IP_lastr_SupP_Blue_1 = IP_lastr_SupP_Blue_1 + Vars_generator.genVars_SupP_Blue_input_of_round(1, self.TR, pos)
        for bi in range(bs * 2):
            for j in range(8):
                cons = cons + [IP_inir_SupP_Blue_1[bi] + ' - ' + Match_input[bi * 8 + j] + ' = 0']
                cons = cons + [IP_lastr_SupP_Blue_1[bi] + ' - ' + Match_output[bi * 8 + j] + ' = 0']
        Match_new_output = Match_output[30: 94] + Match_output[94: 128] + Match_output[0: 30]
        assert len(Match_new_output) == 128
        for bi in range(bs * 16):
            cons = cons + MITMPreConstraints.Determine_Allone([Match_input[bi], Match_new_output[bi]], Match_Counter[bi])
        return cons

    def genConstraints_additional(self):
        cons = []
        CD_Blue = []
        CD_Red = []
        for r in range(self.TR):
            CD_Blue = CD_Blue + Vars_generator.genVars_Xor_ConsumedDeg_Blue(r)
            CD_Red = CD_Red + Vars_generator.genVars_Xor_ConsumedDeg_Red(r)

        d1 = Vars_generator.genVars_degree__forward()
        d2 = Vars_generator.genVars_degree_backward()

        Deg1 = 'GDeg1'
        Deg2 = 'GDeg2'

        if len(CD_Blue) > 0:
            cons = cons + [
                Deg1 + ' - ' + BasicTools.minusTerms(d1) + ' + ' + BasicTools.plusTerms(CD_Blue) + ' = 0']
        else:
            cons = cons + [Deg1 + ' - ' + BasicTools.minusTerms(d1) + ' = 0']
        if len(CD_Red) > 0:
            cons = cons + [
                Deg2 + ' - ' + BasicTools.minusTerms(d2) + ' + ' + BasicTools.plusTerms(CD_Red) + ' = 0']
        else:
            cons = cons + [Deg2 + ' - ' + BasicTools.minusTerms(d2) + ' = 0']

        cons = cons + [Deg1 + ' >= 1']
        cons = cons + [Deg2 + ' >= 1']

        Match_counter = []
        Match_counter = Match_counter + Vars_generator.genVars_Match_Counter()
        GM = 'GMat'
        cons = cons + [GM + ' - ' + BasicTools.minusTerms(Match_counter) + ' = 0']
        cons = cons + [GM + ' >= 8']
        cons = cons + [BasicTools.plusTerms(CD_Blue) + ' = 0']
        cons = cons + [BasicTools.plusTerms(CD_Red) + ' = 9']
        return cons

    def genConstraints_total(self):
        cons = []
        cons = cons + self.genConstraints_initial_degree()
        for r in range(self.TR):
            cons = cons + self.genConstraints_forward_round(r)
        cons = cons + self.genConstraints_Match()
        cons = cons + self.genConstraints_additional()
        return cons

    def genModel(self, filename):
        V = set([])
        cons = []
        cons = cons + self.genConstraints_total()

        # cons = cons + ['GDeg1 + GDeg2 >= 32']
        cons = cons + ['GObj - GDeg1 <= 0']
        cons = cons + ['GObj - GDeg2 <= 0']
        cons = cons + ['GObj - 0.125 GMat <= 0']
        cons = cons + ['GObj >= 1']

        V = BasicTools.getVariables_From_Constraints(cons)

        with open(filename + ".lp", "w") as fid:
            fid.write('Maximize' + '\n')
            fid.write('GObj' + '\n')
            fid.write('\n')
            fid.write('Subject To')
            fid.write('\n')
            for c in cons:
                fid.write(c)
                fid.write('\n')

            GV = []
            BV = []
            for v in V:
                if v[0] == 'G':
                    GV.append(v)
                else:
                    BV.append(v)

            fid.write('Binary' + '\n')
            for bv in BV:
                fid.write(bv + '\n')

            fid.write('Generals' + '\n')
            for gv in GV:
                fid.write(gv + '\n')


if __name__ == '__main__':
    TR = 4
    root = f'./Model_key/TR{TR}'
    if not os.path.exists(root):
        os.mkdir(root)
    with open(f"./Model_key/Result_{TR}.txt", "w") as rd:
        rd.write('d1, d2, m' + '\n')
        filename = f'./Model_key/KeySchedule'
        A = Constraints_generator(TR)
        A.genModel(filename)
        Model = read(filename + '.lp')
        # Model.setParam('TimeLimit', 180 * 60)
        Model.optimize()

        if Model.SolCount == 0:
            pass
        else:
            Model.write(filename + '.sol')
            solFile = open(filename + '.sol', 'r')
            Sol = dict()

            for line in solFile:
                if line[0] != '#':
                    temp = line
                    # temp = temp.replace('-', ' ')
                    temp = temp.split()
                    Sol[temp[0]] = int(eval(temp[1]))
            # rd.write(str(TR) + ',' + str(ini_r) + ',' + str(mat_r) + ':')
            rd.write(str(Sol['GDeg1']) + ',' + str(Sol['GDeg2']) + ',' + str(Sol['GMat']) + '\n')
            rd.flush()