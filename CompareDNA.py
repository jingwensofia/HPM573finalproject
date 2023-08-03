import InputDataDNA as D
import ParameterDNA as P
import MarkovModelDNA as Cls
import SupportDNA as Support


# simulating screening at 45 strategy
# create a cohort
# id could be any number, could be changed to 0
# this is a test
# test
# test
# test 123456789


cohort_45screen = Cls.Cohort(id=1,
                             pop_size=D.POP_SIZE,
                             parameters=P.Parameters(therapy=P.Therapies.Screen45))
# simulate the cohort
cohort_45screen.simulate(sim_length=D.SIM_TIME_STEPS)

# simulating screening at 50 strategy
# create a cohort
cohort_50screen = Cls.Cohort(id=0,
                             pop_size=D.POP_SIZE,
                             parameters=P.Parameters(therapy=P.Therapies.Screen50))
# simulate the cohort
cohort_50screen.simulate(sim_length=D.SIM_TIME_STEPS)

# print the estimates for different therapies
Support.print_outcomes(sim_outcomes=cohort_45screen.cohortOutcomes,
                       therapy_name=P.Therapies.Screen45)
Support.print_outcomes(sim_outcomes=cohort_50screen.cohortOutcomes,
                       therapy_name=P.Therapies.Screen50)

# draw survival curves and histograms
Support.plot_survival_curves_and_histograms(sim_outcomes_45screen=cohort_45screen.cohortOutcomes,
                                            sim_outcomes_50screen=cohort_50screen.cohortOutcomes)


# print comparative outcomes
Support.print_comparative_outcomes(sim_outcomes_45screen=cohort_45screen.cohortOutcomes,
                                   sim_outcomes_50screen=cohort_50screen.cohortOutcomes)

# report the CEA results
Support.report_CEA_CBA(sim_outcomes_45screen=cohort_45screen.cohortOutcomes,
                       sim_outcomes_50screen=cohort_50screen.cohortOutcomes)


print('For MT-sDNA screening every 3 years, screening at 45 years old is a dominant strategy')
