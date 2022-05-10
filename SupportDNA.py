import InputDataDNA as D
import SimPy.EconEval as Econ
import SimPy.Plots.Histogram as Hist
import SimPy.Plots.SamplePaths as Path
import SimPy.Statistics as Stat
import numpy as np

def print_outcomes(sim_outcomes, therapy_name):
    """ prints the outcomes of a simulated cohort
    :param sim_outcomes: outcomes of a simulated cohort
    :param therapy_name: the name of the selected therapy
    """
    # mean and confidence interval of patient survival time
    survival_mean_CI_text = sim_outcomes.statSurvivalTime\
        .get_formatted_mean_and_interval(interval_type='c',
                                         alpha=D.ALPHA,
                                         deci=2)

    # mean and confidence interval text of time to AIDS
    number_of_polyp_CI_text = sim_outcomes.statNPolyps\
        .get_formatted_mean_and_interval(interval_type='c',
                                         alpha=D.ALPHA,
                                         deci=2)
    # mean and confidence interval text of time to AIDS
    number_of_treat_CI_text = sim_outcomes.statNTreatments\
        .get_formatted_mean_and_interval(interval_type='c',
                                         alpha=D.ALPHA,
                                         deci=2)

    # mean and confidence interval text of discounted total cost
    cost_mean_CI_text = sim_outcomes.statCost\
        .get_formatted_mean_and_interval(interval_type='c',
                                         alpha=D.ALPHA,
                                         deci=0,
                                         form=',')

    # mean and confidence interval text of discounted total utility
    utility_mean_CI_text = sim_outcomes.statUtility\
        .get_formatted_mean_and_interval(interval_type='c',
                                         alpha=D.ALPHA,
                                         deci=2)

    # print outcomes
    print(therapy_name)
    print("  Estimate of mean survival time and {:.{prec}%} confidence interval:".format(1 - D.ALPHA, prec=0),
          survival_mean_CI_text)
    print("  Estimate of expected number of polyps and {:.{prec}%} confidence interval:".format(1 - D.ALPHA, prec=0),
          number_of_polyp_CI_text)
    print("  Estimate of expected number of treatments and {:.{prec}%} confidence interval:".format(1 - D.ALPHA, prec=0),
          number_of_treat_CI_text)
    print("  Estimate of discounted cost and {:.{prec}%} confidence interval:".format(1 - D.ALPHA, prec=0),
          cost_mean_CI_text)
    print("  Estimate of discounted utility and {:.{prec}%} confidence interval:".format(1 - D.ALPHA, prec=0),
          utility_mean_CI_text)
    print("")


def plot_survival_curves_and_histograms(sim_outcomes_45screen, sim_outcomes_50screen):
    """ draws the survival curves and the histograms of time until HIV deaths
    :param sim_outcomes_mono: outcomes of a cohort simulated under mono therapy
    :param sim_outcomes_combo: outcomes of a cohort simulated under combination therapy
    """

    # get survival curves of both treatments
    survival_curves = [
        sim_outcomes_50screen.nLivingPatients,
        sim_outcomes_45screen.nLivingPatients
    ]

    # graph survival curve
    Path.plot_sample_paths(
        sample_paths=survival_curves,
        title='Survival curve',
        x_label='Simulation time step (year)',
        y_label='Number of alive patients',
        legends=['Screen at 50', 'Screen at 45'],
        color_codes=['green', 'blue']
    )

    # histograms of survival times
    set_of_survival_times = [
        sim_outcomes_50screen.survivalTimes,
        sim_outcomes_45screen.survivalTimes
    ]

    # graph histograms
    Hist.plot_histograms(
        data_sets=set_of_survival_times,
        title='Histogram of patient survival time',
        x_label='Survival time (year)',
        y_label='Counts',
        bin_width=1,
        legends=['Screen at 50', 'Screen at 45'],
        color_codes=['green', 'blue'],
        transparency=0.5
    )


def print_comparative_outcomes(sim_outcomes_45screen, sim_outcomes_50screen):
    """ prints average increase in survival time, discounted cost, and discounted utility
    under combination therapy compared to mono therapy
    :param sim_outcomes_mono: outcomes of a cohort simulated under mono therapy
    :param sim_outcomes_combo: outcomes of a cohort simulated under combination therapy
    """

    # increase in mean survival time under combination therapy with respect to mono therapy
    increase_survival_time = Stat.DifferenceStatIndp(
        name='Increase in mean survival time',
        x=sim_outcomes_45screen.survivalTimes,
        y_ref=sim_outcomes_50screen.survivalTimes)

    # estimate and CI
    estimate_CI = increase_survival_time.get_formatted_mean_and_interval(interval_type='c',
                                                                         alpha=D.ALPHA,
                                                                         deci=2)
    print("Increase in mean survival time and {:.{prec}%} confidence interval:"
          .format(1 - D.ALPHA, prec=0),
          estimate_CI)

    # increase in mean discounted cost under combination therapy with respect to mono therapy
    increase_discounted_cost = Stat.DifferenceStatIndp(
        name='Increase in mean discounted cost',
        x=sim_outcomes_45screen.costs,
        y_ref=sim_outcomes_50screen.costs)

    # estimate and CI
    estimate_CI = increase_discounted_cost.get_formatted_mean_and_interval(interval_type='c',
                                                                           alpha=D.ALPHA,
                                                                           deci=2,
                                                                           form=',')
    print("Increase in mean discounted cost and {:.{prec}%} confidence interval:"
          .format(1 - D.ALPHA, prec=0),
          estimate_CI)

    # increase in mean discounted utility under combination therapy with respect to mono therapy
    increase_discounted_utility = Stat.DifferenceStatIndp(
        name='Increase in mean discounted utility',
        x=sim_outcomes_45screen.utilities,
        y_ref=sim_outcomes_50screen.utilities)

    # estimate and CI
    estimate_CI = increase_discounted_utility.get_formatted_mean_and_interval(interval_type='c',
                                                                              alpha=D.ALPHA,
                                                                              deci=2)
    print("Increase in mean discounted utility and {:.{prec}%} confidence interval:"
          .format(1 - D.ALPHA, prec=0),
          estimate_CI)

    decrease_number_polyp = Stat.DifferenceStatIndp(
        name='Decrease in expected number of polyps',
        x=sim_outcomes_45screen.nTotalPolyps,
        y_ref=sim_outcomes_50screen.nTotalPolyps)

    # estimate and CI
    estimate_CI = decrease_number_polyp.get_formatted_mean_and_interval(interval_type='c',
                                                                         alpha=D.ALPHA,
                                                                         deci=2)
    print("Decrease in expected number of polyps and {:.{prec}%} confidence interval:"
          .format(1 - D.ALPHA, prec=0),
          estimate_CI)

    increase_number_treat = Stat.DifferenceStatIndp(
        name='Increase in expected number of treatments',
        x=sim_outcomes_45screen.NTreatments,
        y_ref=sim_outcomes_50screen.NTreatments)

    # estimate and CI
    estimate_CI = increase_number_treat.get_formatted_mean_and_interval(interval_type='c',
                                                                        alpha=D.ALPHA,
                                                                        deci=2)
    print("Increase in expected number of treatments and {:.{prec}%} confidence interval:"
          .format(1 - D.ALPHA, prec=0),
          estimate_CI)

def report_CEA_CBA(sim_outcomes_45screen, sim_outcomes_50screen):
    """ performs cost-effectiveness and cost-benefit analyses
    :param sim_outcomes_mono: outcomes of a cohort simulated under mono therapy
    :param sim_outcomes_combo: outcomes of a cohort simulated under combination therapy
    """

    # define two strategies
    screen45_strategy = Econ.Strategy(
        name='Screen At 45',
        cost_obs=sim_outcomes_45screen.costs,
        effect_obs=sim_outcomes_45screen.utilities,
        color='green'
    )
    screen50_strategy = Econ.Strategy(
        name='Screen At 50',
        cost_obs=sim_outcomes_50screen.costs,
        effect_obs=sim_outcomes_50screen.utilities,
        color='blue'
    )

    # do CEA
    # (the first strategy in the list of strategies is assumed to be the 'Base' strategy)
    CEA = Econ.CEA(
        strategies=[screen50_strategy, screen45_strategy],
        if_paired=False
    )

    # plot cost-utility figure
    CEA.plot_CE_plane(
        title='Cost-Utility Analysis',
        x_label='Additional Utilities',
        y_label='Additional Cost',
        x_range=(-0.5, 0.8),
        y_range=(-1000, 3000),
        interval_type='c'  # to show confidence intervals for cost and effect of each strategy
    )

    # report the CE table
    CEA.build_CE_table(
        interval_type='c',
        alpha=D.ALPHA,
        cost_digits=0,
        effect_digits=2,
        icer_digits=2,
        file_name='CETable.csv')

    # CBA
    NBA = Econ.CBA(
        strategies=[screen50_strategy, screen45_strategy],
        wtp_range=[0, 11000],
        if_paired=False
    )
    # show the net monetary benefit figure
    NBA.plot_incremental_nmbs(
        title='Cost-Benefit Analysis',
        x_label='Willingness-to-pay per Utility ($)',
        y_label='Incremental Net Monetary Benefit ($)',
        interval_type='c',
        show_legend=True,
        figure_size=(6, 5)
    )
