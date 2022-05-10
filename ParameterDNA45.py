from enum import Enum
import InputDataDNA45 as Data


class Therapies(Enum):
    """ screening at 50 vs. screening at 45 strategy """
    ScreenDNA45 = 0
    ScreenFIT45 = 1


class Parameters:
    def __init__(self, therapy):

        # selected therapy
        self.therapy = therapy  # anticoagulation or no anticoagulation for clinical trial

        # initial health state
        self.initialHealthState = Data.HealthStates.WELL

        # annual treatment cost if stroke happens
        if self.therapy == Therapies.ScreenDNA45:
            self.annualTreatmentCost = Data.DNA_COST
        elif self.therapy == Therapies.ScreenFIT45:
            self.annualTreatmentCost = Data.FIT_COST

            # transition probability matrix of the selected therapy
        self.transRateMatrix = []

        # calculate transition probabilities between hiv states
        if self.therapy == Therapies.ScreenDNA45:
            # calculate transition probability matrix for the mono therapy
            self.transRateMatrix = Data.TRANS45_DNAScreen_MATRIX

        elif self.therapy == Therapies.ScreenFIT45:
            # calculate transition probability matrix for the combination therapy
            self.transRateMatrix = Data.TRANS45_FITScreen_MATRIX

        # annual state costs and utilities
        self.annualStateCosts = Data.ANNUAL_STATE_COST
        self.annualStateUtilities = Data.ANNUAL_STATE_UTILITY

        # discount rate
        self.discountRate = Data.DISCOUNT
