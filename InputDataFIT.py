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

r1 = 1+0.02


class HealthStates(Enum):
    """ health states of patients """
    WELL = 0
    SMALL = 1
    LARGE = 2
    CRC = 3
    CRC_DEATH = 4
    NATURAL_DEATH = 5
    SCREEN_NO_DISEASE = 6
    SCREEN_DISEASE = 7
    TREATMENT = 8

# transition rate matrix for 45 yrs without screening:
# WELL SMALL LARGE CRC CRC_DEATH NATURAL_DEATH SCREEN_NO_DISEASE SCREEN_DISEASE TREATMENT
TRANS45_Screen_MATRIX = [
    [0,      0.01122,       0,     0.0004488,       0,      0.0026605,   1,  0,   0],  # WELL
    [0,          0,    0.0102,           0,       0,      0.0026605,   0,  1,   0],  # SMALL
    [0,          0,       0,        0.051,        0,      0.0026605,   0,  1,   0],  # LARGE
    [0,          0,       0,           0, 0.011172,      0.0026605,   0,  1,   0],  # CRC
    [0,          0,       0,           0,        0,              0,   0,  0,   0],  # CRC_DEATH
    [0,          0,       0,           0,        0,              0,   0,  0,   0],  # NATUAL_DEATH
    [351.86,     0,       0,           0,        0,   0.0026605*r1,   0,  0, 13.14],  # SCREEN_NO_DISEASE
    [0,     337.26,   278.13,      97.455,       0,    0.0026605*r1,   0,  0, 382.155],  # SCREEN_DISEASE
    [3.92,      0,        0,           0,        0,    0.0026605*r1,   0,  0,    0],  # TREATMENT
]

# transition rate matrix for 45 yrs with screening:
# WELL SMALL LARGE CRC CRC_DEATH NATURAL_DEATH SCREEN_NO_DISEASE SCREEN_DISEASE TREATMENT
TRANS50_Screen_MATRIX = [
    [0,      0.011,       0,     0.00044,       0,      0.0041757,   1,  0,   0],  # WELL
    [0,          0,    0.01,           0,       0,      0.0041757,   0,  1,   0],  # SMALL
    [0,          0,       0,        0.05,        0,      0.0041757,   0,  1,   0],  # LARGE
    [0,          0,       0,           0, 0.011061,      0.0041757,   0,  1,   0],  # CRC
    [0,          0,       0,           0,        0,              0,   0,  0,   0],  # CRC_DEATH
    [0,          0,       0,           0,        0,              0,   0,  0,   0],  # NATUAL_DEATH
    [351.86,     0,       0,           0,        0,    0.0041757*r1,   0,  0, 13.14],  # SCREEN_NO_DISEASE
    [0,     337.26,   278.13,      97.455,       0,    0.0041757*r1,   0,  0, 382.155],  # SCREEN_DISEASE
    [3.92,      0,        0,           0,        0,    0.0041757*r1,   0,  0,    0],  # TREATMENT
]
# annual health utility of each health state
ANNUAL_STATE_UTILITY = [
    1,           # WELL
    0.9,           # SMALL
    0.85,           # LARGE
    0.70,        # CRC
    0,           # CRC_DEATH
    0,           # NATUAL_DEATH
    1,           # SCREEN_NO_DISEASE
    0.95,           # SCREEN_DISEASE
    0.82,        # TREATMENT
    ]
# annual cost of each health state
ANNUAL_STATE_COST = [
    0,           # WELL
    256,           # SMALL
    426,           # LARGE
    4497,        # CRC
    0,           # CRC_DEATH
    0,           # NATUAL_DEATH
    0,           # SCREEN_NO_DISEASE
    0,           # SCREEN_DISEASE
    0,           # TREATMENT
    ]

print('Transition probability matrix without screening at 45:', TRANS45_Screen_MATRIX)
print('Transition probability matrix with screening at 45:', TRANS50_Screen_MATRIX)
print('')
