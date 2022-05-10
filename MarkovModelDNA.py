import numpy as np
import SimPy.Markov as Markov
import SimPy.SamplePath as Path
from InputDataDNA import HealthStates
import SimPy.EconEval as Econ
import SimPy.Statistics as Stat


class Patient:
    def __init__(self, id, parameters):
        """ initiates a patient
        :param id: ID of the patient
        :param trans_rate_matrix: transition rate matrix
        """

        self.id = id
        self.params = parameters
        self.stateMonitor = PatientStateMonitor(parameters=parameters)

    def simulate(self, sim_length):
        """ simulate the patient over the specified simulation length """

        # random number generator for this patient
        rng = np.random.RandomState(seed=self.id)
        # gillespie algorithm
        gillespie = Markov.Gillespie(transition_rate_matrix=self.params.transRateMatrix)

        t = 0  # simulation time
        if_stop = False

        # while the patient is alive and simulation length is not yet reached
        while not if_stop:
            # find time until next event (dt), and next state
            # (note that the gillespie algorithm returns None for dt if the process
            # is in an absorbing state)
            dt, new_state_index = gillespie.get_next_state(
                current_state_index=self.stateMonitor.currentState.value,
                rng=rng)

            # stop if time to next event (dt) is None (i.e. we have reached an absorbing state)
            if dt is None:
                if_stop = True

            else:
                # else if next event occurs beyond simulation length
                if dt + t > sim_length:
                    # advance time to the end of the simulation and stop
                    t = sim_length
                    # the individual stays in the current state until the end of the simulation
                    new_state_index = self.stateMonitor.currentState.value
                    if_stop = True
                else:
                    # advance time to the time of next event
                    t += dt
                # update health state
                self.stateMonitor.update(time=t, new_state=HealthStates(new_state_index))


class PatientStateMonitor:

    def __init__(self, parameters):

        self.currentState = parameters.initialHealthState     # assuming everyone starts in "Well"
        self.survivalTime = None
        self.nPolyps = 0
        self.nTreatments = 0
        self.costUtilityMonitor = PatientCostUtilityMonitor(parameters=parameters)

    def update(self, time, new_state):
        """
        update the current health state to the new health state
        :param time: current time
        :param new_state: new state
        """

        # update survival time
        if new_state in (HealthStates.CRC_DEATH, HealthStates.NATURAL_DEATH):
            self.survivalTime = time

        # update number of strokes
        if new_state in (HealthStates.SMALL, HealthStates.LARGE):
            self.nPolyps += 1

        if new_state == HealthStates.TREATMENT:
            self.nTreatments += 1

        # update cost and utility
        self.costUtilityMonitor.update(time=time,
                                       current_state=self.currentState,
                                       next_state=new_state)

        # update current health state
        self.currentState = new_state


class PatientCostUtilityMonitor:

    def __init__(self, parameters):

        self.tLastRecorded = 0  # time when the last cost and outcomes got recorded

        # model parameters for this patient
        self.params = parameters

        # total cost and utility
        self.totalDiscountedCost = 0
        self.totalDiscountedUtility = 0

    def update(self, time, current_state, next_state):
        """ updates the discounted total cost and health utility
        :param time: simulation time
        :param current_state: current health state
        :param next_state: next health state
        """

        # cost and utility (per unit of time) during the period since the last recording until now
        if current_state in (HealthStates.SCREEN_NO_DISEASE, HealthStates.SCREEN_DISEASE):
            cost = self.params.annualStateCosts[current_state.value] + self.params.annualTreatmentCost
        else:
            cost = self.params.annualStateCosts[current_state.value]
        utility = self.params.annualStateUtilities[current_state.value]

        # discounted cost and utility (continuously compounded)
        discounted_cost = Econ.pv_continuous_payment(payment=cost,
                                                     discount_rate=self.params.discountRate,
                                                     discount_period=(self.tLastRecorded, time))
        discounted_utility = Econ.pv_continuous_payment(payment=utility,
                                                        discount_rate=self.params.discountRate,
                                                        discount_period=(self.tLastRecorded, time))
        if next_state in (HealthStates.SMALL, HealthStates.LARGE):
            discounted_cost += Econ.pv_single_payment(payment=1823, discount_rate=0.03,
                                                      discount_period=time,
                                                      discount_continuously=True)
        if next_state == HealthStates.CRC:
            discounted_cost += Econ.pv_single_payment(payment=64986, discount_rate=0.03,
                                                      discount_period=time,
                                                      discount_continuously=True)

        if next_state == HealthStates.TREATMENT:
            discounted_cost += Econ.pv_single_payment(payment=1278, discount_rate=0.03,
                                                      discount_period=time,
                                                      discount_continuously=True)
        # if we want to add stroke into the model, stroke is one time thing
        '''Econ.pv_single_payment(payment=1000, discount_rate=0.03,
                               discount_period=time,
                               discount_continuously=True) '''

        # update total discounted cost and utility
        self.totalDiscountedCost += discounted_cost
        self.totalDiscountedUtility += discounted_utility

        # update the time since last recording to the current time
        self.tLastRecorded = time


class Cohort:

    def __init__(self, id, pop_size, parameters):
        """ create a cohort of patients
        :param id: cohort ID
        :param pop_size: population size of this cohort
        :param trans_rate_matrix: transition rate matrix
        """
        self.id = id
        self.popSize = pop_size
        self.params = parameters
        self.cohortOutcomes = CohortOutcomes()

    def simulate(self, sim_length):
        """ simulate the cohort of patients over the specified number of time-steps
        :param sim_length: simulation length
        """

        # populate and simulate the cohort
        for i in range(self.popSize):
            # create a new patient (use id * pop_size + n as patient id)
            patient = Patient(id=self.id * self.popSize + i,
                              parameters=self.params)
            # simulate
            patient.simulate(sim_length)

            # store outputs of this simulation
            self.cohortOutcomes.extract_outcome(simulated_patient=patient)

        # calculate cohort outcomes
        self.cohortOutcomes.calculate_cohort_outcomes(initial_pop_size=self.popSize)


class CohortOutcomes:
    def __init__(self):

        self.survivalTimes = []
        self.nTotalPolyps = []
        self.NTreatments = []
        self.nLivingPatients = None
        self.costs = []  # patients' discounted costs
        self.utilities = []  # patients' discounted utilities

        self.statSurvivalTime = None  # summary statistics for survival time
        self.statNPolyps = None
        self.statNTreatments = None
        self.statCost = None  # summary statistics for discounted cost
        self.statUtility = None  # summary statistics for discounted utility

    def extract_outcome(self, simulated_patient):
        """ extracts outcomes of a simulated patient
        :param simulated_patient: a simulated patient"""

        # survival time
        if not (simulated_patient.stateMonitor.survivalTime is None):
            self.survivalTimes.append(simulated_patient.stateMonitor.survivalTime)
        # number of strokes
        self.nTotalPolyps.append(simulated_patient.stateMonitor.nPolyps)
        self.NTreatments.append(simulated_patient.stateMonitor.nTreatments)

        self.costs.append(simulated_patient.stateMonitor.costUtilityMonitor.totalDiscountedCost)
        self.utilities.append(simulated_patient.stateMonitor.costUtilityMonitor.totalDiscountedUtility)

    def calculate_cohort_outcomes(self, initial_pop_size):
        """ calculates the cohort outcomes
        :param initial_pop_size: initial population size
        """
        # summary statistics
        self.statSurvivalTime = Stat.SummaryStat(name='Survival time', data=self.survivalTimes)
        self.statNPolyps = Stat.SummaryStat(name='Post-stroke time', data=self.nTotalPolyps)
        self.statNTreatments = Stat.SummaryStat(name='Post-stroke time', data=self.NTreatments)
        self.statCost = Stat.SummaryStat(name='Discounted cost', data=self.costs)
        self.statUtility = Stat.SummaryStat(name='Discounted utility', data=self.utilities)

        # survival curve
        self.nLivingPatients = Path.PrevalencePathBatchUpdate(
            name='# of living patients',
            initial_size=initial_pop_size,
            times_of_changes=self.survivalTimes,
            increments=[-1]*len(self.survivalTimes)
        )
