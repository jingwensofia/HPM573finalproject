import InputModelData as D
import ParameterClasses as P
import MarkovModelClasses as Cls
import Support as Support


# simulating mono therapy
# create a cohort
cohort_screen = Cls.Cohort(id=1,      # id could be any number, could be changed to 0
                           pop_size=D.POP_SIZE,
                           parameters=P.Parameters(therapy=P.Therapies.Screen))
# simulate the cohort
cohort_screen.simulate(sim_length=D.SIM_TIME_STEPS)

# simulating combination therapy
# create a cohort
cohort_no_screen = Cls.Cohort(id=0,
                              pop_size=D.POP_SIZE,
                              parameters=P.Parameters(therapy=P.Therapies.NoScreen))
# simulate the cohort
cohort_no_screen.simulate(sim_length=D.SIM_TIME_STEPS)

# print the estimates for different therapies
Support.print_outcomes(sim_outcomes=cohort_screen.cohortOutcomes,
                       therapy_name=P.Therapies.Screen)
Support.print_outcomes(sim_outcomes=cohort_no_screen.cohortOutcomes,
                       therapy_name=P.Therapies.NoScreen)

# draw survival curves and histograms
Support.plot_survival_curves_and_histograms(sim_outcomes_screen=cohort_screen.cohortOutcomes,
                                            sim_outcomes_no_screen=cohort_no_screen.cohortOutcomes)


# print comparative outcomes
Support.print_comparative_outcomes(sim_outcomes_screen=cohort_screen.cohortOutcomes,
                                   sim_outcomes_no_screen=cohort_no_screen.cohortOutcomes)

# report the CEA results
Support.report_CEA_CBA(sim_outcomes_screen=cohort_screen.cohortOutcomes,
                       sim_outcomes_no_screen=cohort_no_screen.cohortOutcomes)


print('If the willingness-to-pay is $5069.6, I would recommend adopting this anticoagulation drug')
