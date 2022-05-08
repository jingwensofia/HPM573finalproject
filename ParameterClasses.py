from enum import Enum
import InputModelData as Data


class Therapies(Enum):
    """ mono vs. combination therapy """
    NoScreen = 0
    Screen = 1


class Parameters:
    def __init__(self, therapy):

        # selected therapy
        self.therapy = therapy  # anticoagulation or no anticoagulation for clinical trial

        # initial health state
        self.initialHealthState = Data.HealthStates.WELL

        # annual treatment cost if stroke happens
        if self.therapy == Therapies.Screen:
            self.annualTreatmentCost = Data.FIT_COST
        else:
            self.annualTreatmentCost = 0

            # transition probability matrix of the selected therapy
        self.transRateMatrix = []

        # calculate transition probabilities between hiv states
        if self.therapy == Therapies.Screen:
            # calculate transition probability matrix for the mono therapy
            self.transRateMatrix = Data.TRANS45_Screen_MATRIX

        elif self.therapy == Therapies.NoScreen:
            # calculate transition probability matrix for the combination therapy
            self.transRateMatrix = Data.TRANS45_NoScreen_MATRIX

        # annual state costs and utilities
        self.annualStateCosts = Data.ANNUAL_STATE_COST
        self.annualStateUtilities = Data.ANNUAL_STATE_UTILITY

        # discount rate
        self.discountRate = Data.DISCOUNT
