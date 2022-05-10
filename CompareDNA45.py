import InputDataDNA45 as D
import ParameterDNA45 as P
import MarkovModelDNA45 as Cls
import SupportDNA45 as Support


# simulating mono therapy
# create a cohort
# id could be any number, could be changed to 0
cohort_DNAscreen = Cls.Cohort(id=1,
                              pop_size=D.POP_SIZE,
                              parameters=P.Parameters(therapy=P.Therapies.ScreenDNA45))
# simulate the cohort
cohort_DNAscreen.simulate(sim_length=D.SIM_TIME_STEPS)

# simulating combination therapy
# create a cohort
cohort_FITscreen = Cls.Cohort(id=0,
                              pop_size=D.POP_SIZE,
                              parameters=P.Parameters(therapy=P.Therapies.ScreenFIT45))
# simulate the cohort
cohort_FITscreen.simulate(sim_length=D.SIM_TIME_STEPS)

# print the estimates for different therapies
Support.print_outcomes(sim_outcomes=cohort_DNAscreen.cohortOutcomes,
                       therapy_name=P.Therapies.ScreenDNA45)
Support.print_outcomes(sim_outcomes=cohort_FITscreen.cohortOutcomes,
                       therapy_name=P.Therapies.ScreenFIT45)

# draw survival curves and histograms
Support.plot_survival_curves_and_histograms(sim_outcomes_DNAscreen=cohort_DNAscreen.cohortOutcomes,
                                            sim_outcomes_FITscreen=cohort_FITscreen.cohortOutcomes)


# print comparative outcomes
Support.print_comparative_outcomes(sim_outcomes_DNAscreen=cohort_DNAscreen.cohortOutcomes,
                                   sim_outcomes_FITscreen=cohort_FITscreen.cohortOutcomes)

# report the CEA results
Support.report_CEA_CBA(sim_outcomes_DNAscreen=cohort_DNAscreen.cohortOutcomes,
                       sim_outcomes_FITscreen=cohort_FITscreen.cohortOutcomes)


print('If the willingness-to-pay is $20,198, I would recommend adopting DNA screening strategy among '
      '45 years old population')
