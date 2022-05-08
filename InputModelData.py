from enum import Enum
# problem 1 matrix with anticoagulation drugs
# simulation settings
POP_SIZE = 1000         # cohort population size
SIM_TIME_STEPS = 30    # length of simulation (years)
ALPHA = 0.05        # significance level for calculating confidence intervals
DISCOUNT = 0.03     # annual discount rate

# annual costs for each status
FIT_COST = 17.7

PPVS = 0.1857
PPVL = 0.0163
PPVCA = 0.0078203

r1 = 1+0.075
r2 = 1+0.02

class HealthStates(Enum):
    """ health states of patients """
    WELL = 0
    SMALL = 1
    LARGE = 2
    CRC = 3
    CRC_DEATH = 4
    NATURAL_DEATH = 5

# transition rate matrix for 45 yrs without screening: well small large CRC CRC_DEATH NATURAL_DEATH
TRANS45_NoScreen_MATRIX = [
    [0,     0.011,        0,       0.00044,     0,       0.0026605],      # WELL
    [0,         0,      0.01,      0,           0,       0.0026605],     # SMALL
    [0,         0,         0,      0.05,        0,       0.0026605],     # LARGE
    [0,         0,         0,      0,          0.04395,  0.0026605],             # CRC
    [0,         0,         0,      0,           0,       0],             # CRC_DEATH
    [0,         0,         0,      0,           0,       0],                # NATUAL_DEATH
    ]

# transition rate matrix for 45 yrs with screening:: well small large CRC CRC_DEATH NATURAL_DEATH
TRANS45_Screen_MATRIX = [
    [0,     0.011,        0,       0.00044*(1-PPVCA),     0,       0.0026605*r2],      # WELL
    [0,         0,      0.01*(1-PPVS),      0,           0,       0.0026605*r1],     # SMALL
    [0,         0,         0,      0.05*(1-PPVL),        0,       0.0026605*r1],     # LARGE
    [0,         0,         0,      0,          0.011061,  0.0026605*r2],             # CRC
    [0,         0,         0,      0,           0,       0],             # CRC_DEATH
    [0,         0,         0,      0,           0,       0],                # NATUAL_DEATH
    ]

# annual health utility of each health state
ANNUAL_STATE_UTILITY = [
    1,           # WELL
    0,           # SMALL
    0,           # LARGE
    0.82,        # CRC
    0,           # CRC_DEATH
    0,           # NATUAL_DEATH
    ]
# annual cost of each health state
ANNUAL_STATE_COST = [
    0,           # WELL
    256,           # SMALL
    426,           # LARGE
    4497,        # CRC
    0,           # CRC_DEATH
    0,           # NATUAL_DEATH
    ]

print('Transition probability matrix without screening at 45:', TRANS45_NoScreen_MATRIX)
print('Transition probability matrix with screening at 45:', TRANS45_Screen_MATRIX)
print('')
