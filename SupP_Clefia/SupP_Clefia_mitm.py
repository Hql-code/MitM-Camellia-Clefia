
from SupP_Clefia.utils import *
from gurobipy import *


class Vars_generator:
    # - Input
    @staticmethod
    def genVars_Input_of_Round(i, r, pos):
        return [f'IP_{i}_r{r}_{pos}_{j}' for j in range(bs)]

    @staticmethod
    def genVars_Input_isWhite(r, pos):
        return [f'IP_isWhite_r{r}_{pos}_{j}' for j in range(bs)]

    @staticmethod
    def genVars_SupP_Blue_Input_of_Round(i, r, pos):
        return [f'IP_SupP_Blue_{i}_r{r}_{pos}_{j}' for j in range(bs)]

    @staticmethod
    def genVars_SupP_Red_Input_of_Round(i, r, pos):
        return [f'IP_SupP_Red_{i}_r{r}_{pos}_{j}' for j in range(bs)]

    # - MixColumns
    @staticmethod
    def genVars_Input_of_MixColumns(i, r, pos):
        return [f'IMC_{i}_r{r}_{pos}_{j}' for j in range(bs)]

    @staticmethod
    def genVars_Input_of_MixColumns_isWhite(r, pos):
        return [f'IMC_isWhite_r{r}_{pos}_{j}' for j in range(bs)]

    @staticmethod
    def genVars_SupP_Blue_Input_of_MixColumns(i, r, pos):
        return [f'IMC_SupP_Blue_{i}_r{r}_{pos}_{j}' for j in range(bs)]

    @staticmethod
    def genVars_SupP_Red_Input_of_MixColumns(i, r, pos):
        return [f'IMC_SupP_Red_{i}_r{r}_{pos}_{j}' for j in range(bs)]

    @staticmethod
    def genVars_SupP_Blue_Output_of_MixColumns(i, r, pos):
        return [f'OMC_SupP_Blue_{i}_r{r}_{pos}_{j}' for j in range(bs)]

    @staticmethod
    def genVars_SupP_Red_Output_of_MixColumns(i, r, pos):
        return [f'OMC_SupP_Red_{i}_r{r}_{pos}_{j}' for j in range(bs)]

    @staticmethod
    def genVars_MC_SupP_Blue_ColExistWhite(r, pos):
        return f'MC_SupP_Blue_ColExistWhite_r{r}_{pos}'

    @staticmethod
    def genVars_MC_SupP_Red_ColExistWhite(r, pos):
        return f'MC_SupP_Red_ColExistWhite_r{r}_{pos}'

    @staticmethod
    def genVars_MC_SupP_Blue_ColAllGray(r, pos):
        return f'MC_SupP_Blue_ColAllGray_r{r}_{pos}'

    @staticmethod
    def genVars_MC_SupP_Red_ColAllGray(r, pos):
        return f'MC_SupP_Red_ColAllGray_r{r}_{pos}'

    @staticmethod
    def genVars_MC_SupP_Blue_SumGray(r, pos):
        return f'G_SupP_Blue_SumGray_r{r}_{pos}'

    @staticmethod
    def genVars_MC_SupP_Red_SumGray(r, pos):
        return f'G_SupP_Red_SumGray_r{r}_{pos}'

    @staticmethod
    def genVars_MC_ConsumedDeg_Blue(r, pos):
        return f'G_CD_MC_Blue_r{r}_{pos}'

    @staticmethod
    def genVars_MC_ConsumedDeg_Red(r, pos):
        return f'G_CD_MC_Red__r{r}_{pos}'

    # - Xor
    @staticmethod
    def genVars_Xor_ConsumedDeg_Blue(r, pos):
        return [f'CD_Xor_Blue_r{r}_{pos}_{j}' for j in range(bs)]

    @staticmethod
    def genVars_Xor_ConsumedDeg_Red(r, pos):
        return [f'CD_Xor_Red__r{r}_{pos}_{j}' for j in range(bs)]

    @staticmethod
    def genVars_OXor_isWhite(r, pos):
        return [f'OXor_isWhite_r{r}_{pos}_{j}' for j in range(bs)]

    @staticmethod
    def genVars_OXor_SupP_Blue_AND(i, r, pos):
        return [f'OXor_SupP_Blue_AND_{i}_r{r}_{pos}_{j}' for j in range(bs)]

    @staticmethod
    def genVars_OXor_SupP_Blue_OR(i, r, pos):
        return [f'OXor_SupP_Blue_OR_{i}_r{r}_{pos}_{j}' for j in range(bs)]

    @staticmethod
    def genVars_OXor_SupP_Red_AND(i, r, pos):
        return [f'OXor_SupP_Red_AND_{i}_r{r}_{pos}_{j}' for j in range(bs)]

    @staticmethod
    def genVars_OXor_SupP_Red_OR(i, r, pos):
        return [f'OXor_SupP_Red_OR_{i}_r{r}_{pos}_{j}' for j in range(bs)]

    # Initial Degree
    @staticmethod
    def genVars_degree__forward():
        return ['deg_f_' + str(j) for j in range(bs * b)]

    @staticmethod
    def genVars_degree_backward():
        return ['deg_b_' + str(j) for j in range(bs * b)]

    # Match
    @staticmethod
    def genVars_Match_IMC_isWhite(r, pos):
        return [f'Match_IMC_isWhite_r{r}_{pos}_{j}' for j in range(bs)]

    @staticmethod
    def genVars_Match_Input_isWhite(r, pos):
        return [f'Match_IP_isWhite_r{r}_{pos}_{j}' for j in range(bs)]

    @staticmethod
    def genVars_Match_Output_isWhite(r, pos):
        return [f'Match_OP_isWhite_r{r}_{pos}_{j}' for j in range(bs)]

    @staticmethod
    def genVars_Match_OXor_isWhite(r, pos):
        return [f'Match_OXor_isWhite_r{r}_{pos}_{j}' for j in range(bs)]

    @staticmethod
    def genVars_Match_Exist(r, pos):
        return f'Match_Exist_r{r}_{pos}'

    @staticmethod
    def genVars_Match_Counted(r, pos):
        return f'G_Match_Counted_r{r}_{pos}'


class Constraints_generator:
    def __init__(self, total_round, initial_round, matching_round):
        self.ini_r = initial_round
        self.mat_r = matching_round
        self.TR = total_round
        self.pos2 = ['L', 'R']
        self.pos = ['LL', 'LR', 'RL', 'RR']

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
        for pos in self.pos:
            IP_1 = IP_1 + Vars_generator.genVars_Input_of_Round(1, self.ini_r, pos)
            IP_2 = IP_2 + Vars_generator.genVars_Input_of_Round(2, self.ini_r, pos)
            IP_SupP_Blue_1 = IP_SupP_Blue_1 + Vars_generator.genVars_SupP_Blue_Input_of_Round(1, self.ini_r, pos)
            IP_SupP_Blue_2 = IP_SupP_Blue_2 + Vars_generator.genVars_SupP_Blue_Input_of_Round(2, self.ini_r, pos)
            IP_SupP_Red_1 = IP_SupP_Red_1 + Vars_generator.genVars_SupP_Red_Input_of_Round(1, self.ini_r, pos)
            IP_SupP_Red_2 = IP_SupP_Red_2 + Vars_generator.genVars_SupP_Red_Input_of_Round(2, self.ini_r, pos)
            IP_isWhite = IP_isWhite + Vars_generator.genVars_Input_isWhite(self.ini_r, pos)
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
        for pos in self.pos:
            IP_SupP_Blue_1.append(Vars_generator.genVars_SupP_Blue_Input_of_Round(1, r, pos))
            IP_SupP_Blue_2.append(Vars_generator.genVars_SupP_Blue_Input_of_Round(2, r, pos))
            IP_SupP_Red_1.append(Vars_generator.genVars_SupP_Red_Input_of_Round(1, r, pos))
            IP_SupP_Red_2.append(Vars_generator.genVars_SupP_Red_Input_of_Round(2, r, pos))
            IP_nextr_SupP_Blue_1.append(Vars_generator.genVars_SupP_Blue_Input_of_Round(1, r + 1, pos))
            IP_nextr_SupP_Blue_2.append(Vars_generator.genVars_SupP_Blue_Input_of_Round(2, r + 1, pos))
            IP_nextr_SupP_Red_1.append(Vars_generator.genVars_SupP_Red_Input_of_Round(1, r + 1, pos))
            IP_nextr_SupP_Red_2.append(Vars_generator.genVars_SupP_Red_Input_of_Round(2, r + 1, pos))

        IMC_1 = []
        IMC_2 = []
        for pos in self.pos2:
            IMC_1.append(Vars_generator.genVars_Input_of_MixColumns(1, r, pos))
            IMC_2.append(Vars_generator.genVars_Input_of_MixColumns(2, r, pos))

        # SubBytes
        for i in range(2):
            for bi in range(bs):
                cons = cons + MITMPreConstraints.Determine_Allone([IP_SupP_Blue_1[2 * i][bi], IP_SupP_Red_1[2 * i][bi]], IMC_1[i][bi])
                cons = cons + MITMPreConstraints.Determine_Allone([IP_SupP_Blue_2[2 * i][bi], IP_SupP_Red_2[2 * i][bi]], IMC_2[i][bi])

        # Separate
        IMC_SupP_Blue_1 = []
        IMC_SupP_Blue_2 = []
        IMC_SupP_Red_1 = []
        IMC_SupP_Red_2 = []
        IMC_isWhite = []
        for pos in self.pos2:
            IMC_SupP_Blue_1.append(Vars_generator.genVars_SupP_Blue_Input_of_MixColumns(1, r, pos))
            IMC_SupP_Blue_2.append(Vars_generator.genVars_SupP_Blue_Input_of_MixColumns(2, r, pos))
            IMC_SupP_Red_1.append(Vars_generator.genVars_SupP_Red_Input_of_MixColumns(1, r, pos))
            IMC_SupP_Red_2.append(Vars_generator.genVars_SupP_Red_Input_of_MixColumns(2, r, pos))
            IMC_isWhite.append(Vars_generator.genVars_Input_of_MixColumns_isWhite(r, pos))
        for i in range(2):
            for bi in range(bs):
                cons = cons + MITMPreConstraints.Separate_Without_Guess_i(
                    IMC_1[i][bi],
                    IMC_2[i][bi],
                    IMC_SupP_Blue_1[i][bi],
                    IMC_SupP_Blue_2[i][bi],
                    IMC_SupP_Red_1[i][bi],
                    IMC_SupP_Red_2[i][bi],
                    IMC_isWhite[i][bi]
                )

        # MixColumns
        OMC_SupP_Blue_1 = []
        OMC_SupP_Blue_2 = []
        OMC_SupP_Red_1 = []
        OMC_SupP_Red_2 = []
        for pos in self.pos2:
            OMC_SupP_Blue_1.append(Vars_generator.genVars_SupP_Blue_Output_of_MixColumns(1, r, pos))
            OMC_SupP_Blue_2.append(Vars_generator.genVars_SupP_Blue_Output_of_MixColumns(2, r, pos))
            OMC_SupP_Red_1.append(Vars_generator.genVars_SupP_Red_Output_of_MixColumns(1, r, pos))
            OMC_SupP_Red_2.append(Vars_generator.genVars_SupP_Red_Output_of_MixColumns(2, r, pos))
        for i in range(2):
            IMC_SupP_Blue_ColExistWhite = Vars_generator.genVars_MC_SupP_Blue_ColExistWhite(r, self.pos2[i])
            IMC_SupP_Red_ColExistWhite = Vars_generator.genVars_MC_SupP_Red_ColExistWhite(r, self.pos2[i])
            IMC_SupP_Blue_ColAllGray = Vars_generator.genVars_MC_SupP_Blue_ColAllGray(r, self.pos2[i])
            IMC_SupP_Red_ColAllGray = Vars_generator.genVars_MC_SupP_Red_ColAllGray(r, self.pos2[i])
            IMC_SupP_Blue_SumGray = Vars_generator.genVars_MC_SupP_Blue_SumGray(r, self.pos2[i])
            IMC_SupP_Red_SumGray = Vars_generator.genVars_MC_SupP_Red_SumGray(r, self.pos2[i])
            CD_Blue = Vars_generator.genVars_MC_ConsumedDeg_Blue(r, self.pos2[i])
            CD_Red = Vars_generator.genVars_MC_ConsumedDeg_Red(r, self.pos2[i])
            cons = cons + MITMPreConstraints.genSubConstraints_MC_SupP__Blue(
                IMC_SupP_Blue_1[i],
                IMC_SupP_Blue_2[i],
                IMC_SupP_Blue_ColExistWhite,
                IMC_SupP_Blue_ColAllGray,
                OMC_SupP_Blue_1[i],
                OMC_SupP_Blue_2[i],
                IMC_SupP_Blue_SumGray,
                CD_Blue
            )
            cons = cons + MITMPreConstraints.genSubConstraints_MC_SupP__Red(
                IMC_SupP_Red_1[i],
                IMC_SupP_Red_2[i],
                IMC_SupP_Red_ColExistWhite,
                IMC_SupP_Red_ColAllGray,
                OMC_SupP_Red_1[i],
                OMC_SupP_Red_2[i],
                IMC_SupP_Red_SumGray,
                CD_Red
            )

        # Xor
        IXor_SupP_Blue_1 = [IP_SupP_Blue_1[1], IP_SupP_Blue_1[3]]
        IXor_SupP_Blue_2 = [IP_SupP_Blue_2[1], IP_SupP_Blue_2[3]]
        IXor_SupP_Red_1 = [IP_SupP_Red_1[1], IP_SupP_Red_1[3]]
        IXor_SupP_Red_2 = [IP_SupP_Red_2[1], IP_SupP_Red_2[3]]
        OXor_SupP_Blue_1 = [IP_nextr_SupP_Blue_1[0], IP_nextr_SupP_Blue_1[2]]
        OXor_SupP_Blue_2 = [IP_nextr_SupP_Blue_2[0], IP_nextr_SupP_Blue_2[2]]
        OXor_SupP_Red_1 = [IP_nextr_SupP_Red_1[0], IP_nextr_SupP_Red_1[2]]
        OXor_SupP_Red_2 = [IP_nextr_SupP_Red_2[0], IP_nextr_SupP_Red_2[2]]
        for i in range(2):
            CD_Xor_Blue = Vars_generator.genVars_Xor_ConsumedDeg_Blue(r, self.pos2[i])
            CD_Xor_Red = Vars_generator.genVars_Xor_ConsumedDeg_Red(r, self.pos2[i])
            OXor_isWhite = Vars_generator.genVars_OXor_isWhite(r, self.pos2[i])
            OXor_SupP_Blue_AND_1 = Vars_generator.genVars_OXor_SupP_Blue_AND(1, r, self.pos2[i])
            OXor_SupP_Blue_AND_2 = Vars_generator.genVars_OXor_SupP_Blue_AND(2, r, self.pos2[i])
            OXor_SupP_Blue_OR_1 = Vars_generator.genVars_OXor_SupP_Blue_OR(1, r, self.pos2[i])
            OXor_SupP_Blue_OR_2 = Vars_generator.genVars_OXor_SupP_Blue_OR(2, r, self.pos2[i])
            OXor_SupP_Red_AND_1 = Vars_generator.genVars_OXor_SupP_Red_AND(1, r, self.pos2[i])
            OXor_SupP_Red_AND_2 = Vars_generator.genVars_OXor_SupP_Red_AND(2, r, self.pos2[i])
            OXor_SupP_Red_OR_1 = Vars_generator.genVars_OXor_SupP_Red_OR(1, r, self.pos2[i])
            OXor_SupP_Red_OR_2 = Vars_generator.genVars_OXor_SupP_Red_OR(2, r, self.pos2[i])
            for bi in range(bs):
                cons = cons + MITMPreConstraints.genConstrains_of_Xor_i(
                    OMC_SupP_Blue_1[i][bi],
                    OMC_SupP_Blue_2[i][bi],
                    OMC_SupP_Red_1[i][bi],
                    OMC_SupP_Red_2[i][bi],
                    IXor_SupP_Blue_1[i][bi],
                    IXor_SupP_Blue_2[i][bi],
                    IXor_SupP_Red_1[i][bi],
                    IXor_SupP_Red_2[i][bi],
                    OXor_SupP_Blue_1[i][bi],
                    OXor_SupP_Blue_2[i][bi],
                    OXor_SupP_Red_1[i][bi],
                    OXor_SupP_Red_2[i][bi],
                    CD_Xor_Blue[bi],
                    CD_Xor_Red[bi],
                    OXor_isWhite[bi],
                    OXor_SupP_Blue_AND_1[bi],
                    OXor_SupP_Blue_AND_2[bi],
                    OXor_SupP_Blue_OR_1[bi],
                    OXor_SupP_Blue_OR_2[bi],
                    OXor_SupP_Red_AND_1[bi],
                    OXor_SupP_Red_AND_2[bi],
                    OXor_SupP_Red_OR_1[bi],
                    OXor_SupP_Red_OR_2[bi]
                )
        # Link
        for bi in range(bs):
            cons = cons + MITMPreConstraints.equalConstraints(IP_SupP_Blue_1[0], IP_nextr_SupP_Blue_1[3])
            cons = cons + MITMPreConstraints.equalConstraints(IP_SupP_Blue_2[0], IP_nextr_SupP_Blue_2[3])
            cons = cons + MITMPreConstraints.equalConstraints(IP_SupP_Red_1[0], IP_nextr_SupP_Red_1[3])
            cons = cons + MITMPreConstraints.equalConstraints(IP_SupP_Red_2[0], IP_nextr_SupP_Red_2[3])
        for bi in range(bs):
            cons = cons + MITMPreConstraints.equalConstraints(IP_SupP_Blue_1[2], IP_nextr_SupP_Blue_1[1])
            cons = cons + MITMPreConstraints.equalConstraints(IP_SupP_Blue_2[2], IP_nextr_SupP_Blue_2[1])
            cons = cons + MITMPreConstraints.equalConstraints(IP_SupP_Red_1[2], IP_nextr_SupP_Red_1[1])
            cons = cons + MITMPreConstraints.equalConstraints(IP_SupP_Red_2[2], IP_nextr_SupP_Red_2[1])
        return cons

    def genConstraints_backward_round(self, r):
        cons = []
        IP_SupP_Blue_1 = []
        IP_SupP_Blue_2 = []
        IP_SupP_Red_1 = []
        IP_SupP_Red_2 = []
        IP_nextr_SupP_Blue_1 = []
        IP_nextr_SupP_Blue_2 = []
        IP_nextr_SupP_Red_1 = []
        IP_nextr_SupP_Red_2 = []
        for pos in self.pos:
            IP_SupP_Blue_1.append(Vars_generator.genVars_SupP_Blue_Input_of_Round(1, r, pos))
            IP_SupP_Blue_2.append(Vars_generator.genVars_SupP_Blue_Input_of_Round(2, r, pos))
            IP_SupP_Red_1.append(Vars_generator.genVars_SupP_Red_Input_of_Round(1, r, pos))
            IP_SupP_Red_2.append(Vars_generator.genVars_SupP_Red_Input_of_Round(2, r, pos))
            IP_nextr_SupP_Blue_1.append(Vars_generator.genVars_SupP_Blue_Input_of_Round(1, r + 1, pos))
            IP_nextr_SupP_Blue_2.append(Vars_generator.genVars_SupP_Blue_Input_of_Round(2, r + 1, pos))
            IP_nextr_SupP_Red_1.append(Vars_generator.genVars_SupP_Red_Input_of_Round(1, r + 1, pos))
            IP_nextr_SupP_Red_2.append(Vars_generator.genVars_SupP_Red_Input_of_Round(2, r + 1, pos))

        IMC_1 = []
        IMC_2 = []
        for pos in self.pos2:
            IMC_1.append(Vars_generator.genVars_Input_of_MixColumns(1, r, pos))
            IMC_2.append(Vars_generator.genVars_Input_of_MixColumns(2, r, pos))

        # SubBytes
        for i in range(2):
            for bi in range(bs):
                cons = cons + MITMPreConstraints.Determine_Allone([IP_SupP_Blue_1[2 * i][bi], IP_SupP_Red_1[2 * i][bi]],
                                                                  IMC_1[i][bi]
                                                                  )
                cons = cons + MITMPreConstraints.Determine_Allone([IP_SupP_Blue_2[2 * i][bi], IP_SupP_Red_2[2 * i][bi]],
                                                                  IMC_2[i][bi]
                                                                  )

        # Separate
        IMC_SupP_Blue_1 = []
        IMC_SupP_Blue_2 = []
        IMC_SupP_Red_1 = []
        IMC_SupP_Red_2 = []
        IMC_isWhite = []
        for pos in self.pos2:
            IMC_SupP_Blue_1.append(Vars_generator.genVars_SupP_Blue_Input_of_MixColumns(1, r, pos))
            IMC_SupP_Blue_2.append(Vars_generator.genVars_SupP_Blue_Input_of_MixColumns(2, r, pos))
            IMC_SupP_Red_1.append(Vars_generator.genVars_SupP_Red_Input_of_MixColumns(1, r, pos))
            IMC_SupP_Red_2.append(Vars_generator.genVars_SupP_Red_Input_of_MixColumns(2, r, pos))
            IMC_isWhite.append(Vars_generator.genVars_Input_of_MixColumns_isWhite(r, pos))
        for i in range(2):
            for bi in range(bs):
                cons = cons + MITMPreConstraints.Separate_Without_Guess_i(
                    IMC_1[i][bi],
                    IMC_2[i][bi],
                    IMC_SupP_Blue_1[i][bi],
                    IMC_SupP_Blue_2[i][bi],
                    IMC_SupP_Red_1[i][bi],
                    IMC_SupP_Red_2[i][bi],
                    IMC_isWhite[i][bi]
                )

        # MixColumns
        OMC_SupP_Blue_1 = []
        OMC_SupP_Blue_2 = []
        OMC_SupP_Red_1 = []
        OMC_SupP_Red_2 = []
        for pos in self.pos2:
            OMC_SupP_Blue_1.append(Vars_generator.genVars_SupP_Blue_Output_of_MixColumns(1, r, pos))
            OMC_SupP_Blue_2.append(Vars_generator.genVars_SupP_Blue_Output_of_MixColumns(2, r, pos))
            OMC_SupP_Red_1.append(Vars_generator.genVars_SupP_Red_Output_of_MixColumns(1, r, pos))
            OMC_SupP_Red_2.append(Vars_generator.genVars_SupP_Red_Output_of_MixColumns(2, r, pos))
        for i in range(2):
            IMC_SupP_Blue_ColExistWhite = Vars_generator.genVars_MC_SupP_Blue_ColExistWhite(r, self.pos2[i])
            IMC_SupP_Red_ColExistWhite = Vars_generator.genVars_MC_SupP_Red_ColExistWhite(r, self.pos2[i])
            IMC_SupP_Blue_ColAllGray = Vars_generator.genVars_MC_SupP_Blue_ColAllGray(r, self.pos2[i])
            IMC_SupP_Red_ColAllGray = Vars_generator.genVars_MC_SupP_Red_ColAllGray(r, self.pos2[i])
            IMC_SupP_Blue_SumGray = Vars_generator.genVars_MC_SupP_Blue_SumGray(r, self.pos2[i])
            IMC_SupP_Red_SumGray = Vars_generator.genVars_MC_SupP_Red_SumGray(r, self.pos2[i])
            CD_Blue = Vars_generator.genVars_MC_ConsumedDeg_Blue(r, self.pos2[i])
            CD_Red = Vars_generator.genVars_MC_ConsumedDeg_Red(r, self.pos2[i])
            cons = cons + MITMPreConstraints.genSubConstraints_MC_SupP__Blue(
                IMC_SupP_Blue_1[i],
                IMC_SupP_Blue_2[i],
                IMC_SupP_Blue_ColExistWhite,
                IMC_SupP_Blue_ColAllGray,
                OMC_SupP_Blue_1[i],
                OMC_SupP_Blue_2[i],
                IMC_SupP_Blue_SumGray,
                CD_Blue
            )
            cons = cons + MITMPreConstraints.genSubConstraints_MC_SupP__Red(
                IMC_SupP_Red_1[i],
                IMC_SupP_Red_2[i],
                IMC_SupP_Red_ColExistWhite,
                IMC_SupP_Red_ColAllGray,
                OMC_SupP_Red_1[i],
                OMC_SupP_Red_2[i],
                IMC_SupP_Red_SumGray,
                CD_Red
            )

        # Xor
        IXor_SupP_Blue_1 = [IP_nextr_SupP_Blue_1[0], IP_nextr_SupP_Blue_1[2]]
        IXor_SupP_Blue_2 = [IP_nextr_SupP_Blue_2[0], IP_nextr_SupP_Blue_2[2]]
        IXor_SupP_Red_1 = [IP_nextr_SupP_Red_1[0], IP_nextr_SupP_Red_1[2]]
        IXor_SupP_Red_2 = [IP_nextr_SupP_Red_2[0], IP_nextr_SupP_Red_2[2]]
        OXor_SupP_Blue_1 = [IP_SupP_Blue_1[1], IP_SupP_Blue_1[3]]
        OXor_SupP_Blue_2 = [IP_SupP_Blue_2[1], IP_SupP_Blue_2[3]]
        OXor_SupP_Red_1 = [IP_SupP_Red_1[1], IP_SupP_Red_1[3]]
        OXor_SupP_Red_2 = [IP_SupP_Red_2[1], IP_SupP_Red_2[3]]
        for i in range(2):
            CD_Xor_Blue = Vars_generator.genVars_Xor_ConsumedDeg_Blue(r, self.pos2[i])
            CD_Xor_Red = Vars_generator.genVars_Xor_ConsumedDeg_Red(r, self.pos2[i])
            OXor_isWhite = Vars_generator.genVars_OXor_isWhite(r, self.pos2[i])
            OXor_SupP_Blue_AND_1 = Vars_generator.genVars_OXor_SupP_Blue_AND(1, r, self.pos2[i])
            OXor_SupP_Blue_AND_2 = Vars_generator.genVars_OXor_SupP_Blue_AND(2, r, self.pos2[i])
            OXor_SupP_Blue_OR_1 = Vars_generator.genVars_OXor_SupP_Blue_OR(1, r, self.pos2[i])
            OXor_SupP_Blue_OR_2 = Vars_generator.genVars_OXor_SupP_Blue_OR(2, r, self.pos2[i])
            OXor_SupP_Red_AND_1 = Vars_generator.genVars_OXor_SupP_Red_AND(1, r, self.pos2[i])
            OXor_SupP_Red_AND_2 = Vars_generator.genVars_OXor_SupP_Red_AND(2, r, self.pos2[i])
            OXor_SupP_Red_OR_1 = Vars_generator.genVars_OXor_SupP_Red_OR(1, r, self.pos2[i])
            OXor_SupP_Red_OR_2 = Vars_generator.genVars_OXor_SupP_Red_OR(2, r, self.pos2[i])
            for bi in range(bs):
                cons = cons + MITMPreConstraints.genConstrains_of_Xor_i(
                    OMC_SupP_Blue_1[i][bi],
                    OMC_SupP_Blue_2[i][bi],
                    OMC_SupP_Red_1[i][bi],
                    OMC_SupP_Red_2[i][bi],
                    IXor_SupP_Blue_1[i][bi],
                    IXor_SupP_Blue_2[i][bi],
                    IXor_SupP_Red_1[i][bi],
                    IXor_SupP_Red_2[i][bi],
                    OXor_SupP_Blue_1[i][bi],
                    OXor_SupP_Blue_2[i][bi],
                    OXor_SupP_Red_1[i][bi],
                    OXor_SupP_Red_2[i][bi],
                    CD_Xor_Blue[bi],
                    CD_Xor_Red[bi],
                    OXor_isWhite[bi],
                    OXor_SupP_Blue_AND_1[bi],
                    OXor_SupP_Blue_AND_2[bi],
                    OXor_SupP_Blue_OR_1[bi],
                    OXor_SupP_Blue_OR_2[bi],
                    OXor_SupP_Red_AND_1[bi],
                    OXor_SupP_Red_AND_2[bi],
                    OXor_SupP_Red_OR_1[bi],
                    OXor_SupP_Red_OR_2[bi]
                )

        # Link
        for bi in range(bs):
            cons = cons + MITMPreConstraints.equalConstraints(IP_SupP_Blue_1[0], IP_nextr_SupP_Blue_1[3])
            cons = cons + MITMPreConstraints.equalConstraints(IP_SupP_Blue_2[0], IP_nextr_SupP_Blue_2[3])
            cons = cons + MITMPreConstraints.equalConstraints(IP_SupP_Red_1[0], IP_nextr_SupP_Red_1[3])
            cons = cons + MITMPreConstraints.equalConstraints(IP_SupP_Red_2[0], IP_nextr_SupP_Red_2[3])
        for bi in range(bs):
            cons = cons + MITMPreConstraints.equalConstraints(IP_SupP_Blue_1[2], IP_nextr_SupP_Blue_1[1])
            cons = cons + MITMPreConstraints.equalConstraints(IP_SupP_Blue_2[2], IP_nextr_SupP_Blue_2[1])
            cons = cons + MITMPreConstraints.equalConstraints(IP_SupP_Red_1[2], IP_nextr_SupP_Red_1[1])
            cons = cons + MITMPreConstraints.equalConstraints(IP_SupP_Red_2[2], IP_nextr_SupP_Red_2[1])
        return cons

    def genConstraints_splice(self):
        cons = []
        IP_SupP_Blue_1 = []
        IP_SupP_Blue_2 = []
        IP_SupP_Red_1 = []
        IP_SupP_Red_2 = []
        IP_nextr_SupP_Blue_1 = []
        IP_nextr_SupP_Blue_2 = []
        IP_nextr_SupP_Red_1 = []
        IP_nextr_SupP_Red_2 = []
        for pos in self.pos:
            IP_SupP_Blue_1.append(Vars_generator.genVars_SupP_Blue_Input_of_Round(1, self.TR - 1, pos))
            IP_SupP_Blue_2.append(Vars_generator.genVars_SupP_Blue_Input_of_Round(2, self.TR - 1, pos))
            IP_SupP_Red_1.append(Vars_generator.genVars_SupP_Red_Input_of_Round(1, self.TR - 1, pos))
            IP_SupP_Red_2.append(Vars_generator.genVars_SupP_Red_Input_of_Round(2, self.TR - 1, pos))
            IP_nextr_SupP_Blue_1.append(Vars_generator.genVars_SupP_Blue_Input_of_Round(1, 1, pos))
            IP_nextr_SupP_Blue_2.append(Vars_generator.genVars_SupP_Blue_Input_of_Round(2, 1, pos))
            IP_nextr_SupP_Red_1.append(Vars_generator.genVars_SupP_Red_Input_of_Round(1, 1, pos))
            IP_nextr_SupP_Red_2.append(Vars_generator.genVars_SupP_Red_Input_of_Round(2, 1, pos))
        for i in range(4):
            cons = cons + MITMPreConstraints.equalConstraints(IP_SupP_Blue_1[(i + 1) % 4], IP_nextr_SupP_Blue_1[i])
            cons = cons + MITMPreConstraints.equalConstraints(IP_SupP_Blue_2[(i + 1) % 4], IP_nextr_SupP_Blue_2[i])
            cons = cons + MITMPreConstraints.equalConstraints(IP_SupP_Red_1[(i + 1) % 4], IP_nextr_SupP_Red_1[i])
            cons = cons + MITMPreConstraints.equalConstraints(IP_SupP_Red_2[(i + 1) % 4], IP_nextr_SupP_Red_2[i])
        return cons

    def genConstraints_Match(self):
        cons = []
        IP_SupP_Blue_1 = []
        IP_SupP_Blue_2 = []
        IP_SupP_Red_1 = []
        IP_SupP_Red_2 = []
        IP_nextr_SupP_Blue_1 = []
        IP_nextr_SupP_Blue_2 = []
        IP_nextr_SupP_Red_1 = []
        IP_nextr_SupP_Red_2 = []
        for pos in self.pos:
            IP_SupP_Blue_1.append(Vars_generator.genVars_SupP_Blue_Input_of_Round(1, self.mat_r[0], pos))
            IP_SupP_Blue_2.append(Vars_generator.genVars_SupP_Blue_Input_of_Round(2, self.mat_r[0], pos))
            IP_SupP_Red_1.append(Vars_generator.genVars_SupP_Red_Input_of_Round(1, self.mat_r[0], pos))
            IP_SupP_Red_2.append(Vars_generator.genVars_SupP_Red_Input_of_Round(2, self.mat_r[0], pos))
            IP_nextr_SupP_Blue_1.append(Vars_generator.genVars_SupP_Blue_Input_of_Round(1, self.mat_r[1] + 1, pos))
            IP_nextr_SupP_Blue_2.append(Vars_generator.genVars_SupP_Blue_Input_of_Round(2, self.mat_r[1] + 1, pos))
            IP_nextr_SupP_Red_1.append(Vars_generator.genVars_SupP_Red_Input_of_Round(1, self.mat_r[1] + 1, pos))
            IP_nextr_SupP_Red_2.append(Vars_generator.genVars_SupP_Red_Input_of_Round(2, self.mat_r[1] + 1, pos))
        # SubBytes
        IMC_1 = []
        IMC_2 = []
        for r in self.mat_r:
            for pos in self.pos2:
                IMC_1.append(Vars_generator.genVars_Input_of_MixColumns(1, r, pos))
                IMC_2.append(Vars_generator.genVars_Input_of_MixColumns(2, r, pos))
        ISB_SupP_Blue_1 = [IP_SupP_Blue_1[0], IP_SupP_Blue_1[2], IP_nextr_SupP_Blue_1[3], IP_nextr_SupP_Blue_1[1]]
        ISB_SupP_Blue_2 = [IP_SupP_Blue_2[0], IP_SupP_Blue_2[2], IP_nextr_SupP_Blue_2[3], IP_nextr_SupP_Blue_2[1]]
        ISB_SupP_Red_1 = [IP_SupP_Red_1[0], IP_SupP_Red_1[2], IP_nextr_SupP_Red_1[3], IP_nextr_SupP_Red_1[1]]
        ISB_SupP_Red_2 = [IP_SupP_Red_2[0], IP_SupP_Red_2[2], IP_nextr_SupP_Red_2[3], IP_nextr_SupP_Red_2[1]]
        for i in range(4):
            for bi in range(bs):
                cons = cons + MITMPreConstraints.Determine_Allone([ISB_SupP_Blue_1[i][bi], ISB_SupP_Red_1[i][bi]], IMC_1[i][bi])
                cons = cons + MITMPreConstraints.Determine_Allone([ISB_SupP_Blue_2[i][bi], ISB_SupP_Red_2[i][bi]], IMC_2[i][bi])
        # Match
        Match_IP_isWhite = []
        Match_OP_isWhite = []
        Match_OXor_iswhite = []
        Match_IMC_isWhite = []
        for pos in self.pos:
            Match_IP_isWhite.append(Vars_generator.genVars_Match_Input_isWhite(self.mat_r[0], pos))
            Match_OP_isWhite.append(Vars_generator.genVars_Match_Output_isWhite(self.mat_r[1], pos))
        for r in self.mat_r:
            for pos in self.pos2:
                Match_IMC_isWhite.append(Vars_generator.genVars_Match_IMC_isWhite(r, pos))
                Match_OXor_iswhite.append(Vars_generator.genVars_Match_OXor_isWhite(r, pos))
        for i in range(4):
            for bi in range(bs):
                cons = cons + MITMPreConstraints.Determine_Merge_isWhite(
                    IP_SupP_Blue_1[i][bi],
                    IP_SupP_Blue_2[i][bi],
                    IP_SupP_Red_1[i][bi],
                    IP_SupP_Red_2[i][bi],
                    Match_IP_isWhite[i][bi]
                )
                cons = cons + MITMPreConstraints.Determine_Merge_isWhite(
                    IP_nextr_SupP_Blue_1[i][bi],
                    IP_nextr_SupP_Blue_2[i][bi],
                    IP_nextr_SupP_Red_1[i][bi],
                    IP_nextr_SupP_Red_2[i][bi],
                    Match_OP_isWhite[i][bi]
                )
        for bi in range(bs):
            cons = cons + BasicTools.OR_([Match_IP_isWhite[1][bi], Match_OP_isWhite[3][bi]], Match_OXor_iswhite[0][bi])
            cons = cons + BasicTools.OR_([Match_IP_isWhite[3][bi], Match_OP_isWhite[1][bi]], Match_OXor_iswhite[1][bi])
            cons = cons + BasicTools.OR_([Match_IP_isWhite[2][bi], Match_OP_isWhite[0][bi]], Match_OXor_iswhite[2][bi])
            cons = cons + BasicTools.OR_([Match_IP_isWhite[0][bi], Match_OP_isWhite[2][bi]], Match_OXor_iswhite[3][bi])
        for i in range(4):
            for bi in range(bs):
                cons = cons + MITMPreConstraints.Determine_Allzero([IMC_1[i][bi], IMC_2[i][bi]], Match_IMC_isWhite[i][bi])

        Match_Exist = []
        G_Match_Counter = []
        for r in self.mat_r:
            for pos in self.pos2:
                Match_Exist.append(Vars_generator.genVars_Match_Exist(r, pos))
                G_Match_Counter.append(Vars_generator.genVars_Match_Counted(r, pos))
        for i in range(4):
            cons = cons + [str(RowN + 1) + ' ' + Match_Exist[i] + ' + ' + BasicTools.plusTerms(Match_IMC_isWhite[i] + Match_OXor_iswhite[i]) + ' <= ' + str(SumIOMC)]
            cons = cons + [str(RowN) + ' ' + Match_Exist[i] + ' + ' + BasicTools.plusTerms(Match_IMC_isWhite[i] + Match_OXor_iswhite[i]) + ' >= ' + str(RowN)]
            cons = cons + [Match_Exist[i] + ' = 1 -> ' + G_Match_Counter[i] + ' + ' + BasicTools.plusTerms(Match_IMC_isWhite[i] + Match_OXor_iswhite[i]) + ' = ' + str(RowN)]
            cons = cons + [Match_Exist[i] + ' = 0 -> ' + G_Match_Counter[i] + ' = 0']
        return cons

    def genConstraints_additional(self):
        cons = []
        CD_Blue = []
        CD_Red = []
        for r in range(self.TR):
            if r not in self.mat_r and r not in [0, self.TR - 1]:
                for pos in self.pos2:
                    CD_Blue = CD_Blue + [Vars_generator.genVars_MC_ConsumedDeg_Blue(r, pos)]
                    CD_Blue = CD_Blue + Vars_generator.genVars_Xor_ConsumedDeg_Blue(r, pos)
                    CD_Red = CD_Red + [Vars_generator.genVars_MC_ConsumedDeg_Red(r, pos)]
                    CD_Red = CD_Red + Vars_generator.genVars_Xor_ConsumedDeg_Red(r, pos)

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

        G_Match_counter = []
        for r in self.mat_r:
            for pos in self.pos2:
                G_Match_counter.append(Vars_generator.genVars_Match_Counted(r, pos))
        GM = 'GMat'
        cons = cons + [GM + ' - ' + BasicTools.minusTerms(G_Match_counter) + ' = 0']
        cons = cons + [GM + ' >= 1']
        return cons

    def genConstraints_total(self):
        cons = []
        cons = cons + self.genConstraints_initial_degree()
        if self.ini_r <= self.mat_r[0]:
            for r in range(self.ini_r, self.mat_r[0]):
                cons = cons + self.genConstraints_forward_round(r)
            for r in range(self.mat_r[1] + 1, self.TR - 1):
                cons = cons + self.genConstraints_backward_round(r)
            for r in range(1, self.ini_r):
                cons = cons + self.genConstraints_backward_round(r)
        if self.ini_r > self.mat_r[1]:
            for r in range(self.ini_r, self.TR - 1):
                cons = cons + self.genConstraints_forward_round(r)
            for r in range(1, self.mat_r[0]):
                cons = cons + self.genConstraints_forward_round(r)
            for r in range(self.mat_r[1] + 1, self.ini_r):
                cons = cons + self.genConstraints_backward_round(r)
        cons = cons + self.genConstraints_splice()
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
        cons = cons + ['GObj - GMat <= 0']
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
    TR = 14
    root = f'./Model/TR{TR}'
    if not os.path.exists(root):
        os.mkdir(root)
    with open(f"./Model/Result_{TR}.txt", "w") as rd:
        rd.write('TR, ini_r, mat_r: d1, d2, m' + '\n')
        for mat_r in [[i, i + 1] for i in range(1, TR - 2)]:
            for ini_r in range(1, TR - 1):
        # for mat_r in [[3, 4]]:
        #     for ini_r in range(8, 9):
                if ini_r != mat_r[1]:
                    filename = f'./Model/TR{TR}/inir{ini_r}_matr{mat_r}'
                    A = Constraints_generator(TR, ini_r, mat_r)
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
                        rd.write(str(TR) + ',' + str(ini_r) + ',' + str(mat_r) + ':')
                        rd.write(str(Sol['GDeg1']) + ',' + str(Sol['GDeg2']) + ',' + str(Sol['GMat']) + '\n')
                        rd.flush()