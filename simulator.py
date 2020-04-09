from outbreaksim import Simulation
import numpy as np
import matplotlib.pyplot as plt


# Monte Carlo Simulation with varying percentage of the population being stationary
def main():

    svals = [0.00, 0.25, 0.5, 0.75, 1]
    numRuns = 10000

    # Simulation Options
    options = {
        'N': 100,       # Grid Size (N x N)
        'M': 1000,      # Initial Population Size
        'X': 0.01,      # % Of initial population that is infected
        'Pm': 0.80,     # Mobility
        'Pd': 0.08,     # Death Rate of Virus
        'K': 7          # Mean Infection Duration
    }

    plot_death_rates = []
    plot_infection_rates = []
    plot_max_infection_rates = []
    plot_max_infection_times = []
    plot_t_stops = []

    for S in svals:
        print('Current Value of S: {}'.format(S))
        options['S'] = S

        death_rates = []
        infection_rates = []
        max_infection_rates = []
        max_infection_times = []
        t_stops = []

        for run in range(numRuns):
            Tmax = 500
            mySim = Simulation(options)
            mySim.initialize_population()

            Tstop = None
            for i in range(Tmax):
                new_infections = mySim.step()
                if not new_infections and mySim.all_healthy():
                    Tstop = i
                    break

            if Tstop is None:
                Tstop = Tmax

            death_rates.append(mySim.total_deaths / mySim.M)
            infection_rates.append(mySim.total_infected / mySim.M)
            max_infection_rates.append(mySim.max_infection_rate)
            max_infection_times.append(mySim.max_infection_time)
            t_stops.append(Tstop)

        plt.hist(100 * np.array(death_rates), bins=60)
        plt.title('Death Rate For S = {}'.format(S))
        plt.ylabel('Frequency')
        plt.xlabel('Total Death Rate (%)')

        plt.savefig('tdr_hist_{}.svg'.format(int(S * 100)))
        plt.show()

        plt.hist(100 * np.array(infection_rates), bins=60)
        plt.title('Total Infection Rate For S = {}'.format(S))
        plt.ylabel('Frequency')
        plt.xlabel('Total Infection Rate (%)')

        plt.savefig('tir_hist_{}.svg'.format(int(S * 100)))
        plt.show()

        plt.hist(100 * np.array(max_infection_rates), bins=60)
        plt.title('Max Infection Rate For S = {}'.format(S))
        plt.ylabel('Frequency')
        plt.xlabel('Max Infection Rate (%)')

        plt.savefig('mir_hist_{}.svg'.format(int(S * 100)))
        plt.show()

        average_total_infection = np.mean(infection_rates) * 100
        average_total_death = np.mean(death_rates) * 100
        average_max_infection = np.mean(max_infection_rates) * 100
        average_max_infection_time = np.mean(max_infection_times)
        average_t_stop = np.mean(t_stops)

        plot_infection_rates.append(average_total_infection)
        plot_death_rates.append(average_total_death)
        plot_max_infection_rates.append(average_max_infection)
        plot_max_infection_times.append(average_max_infection_time)
        plot_t_stops.append(average_t_stop)

        print('-----')
        print('Average Total Infection Rate: {:.4f} %'.format(average_total_infection))
        print('Average Total Death Rate: {:.4f} %'.format(average_total_death))
        print('Average Max Infection Rate: {:.4f} %'.format(average_max_infection))
        print('Average Max Infection Time: {:.2f}'.format(average_max_infection_time))
        print('Average T(Stop): {:.2f}'.format(average_t_stop))
        print('-----')

    plt.plot(svals, plot_death_rates)
    plt.xlabel('S')
    plt.ylabel('Total Death Rate (%)')

    plt.savefig('total_death_rate.svg')
    plt.show()

    plt.plot(svals, plot_infection_rates)
    plt.xlabel('S')
    plt.ylabel('Total Infection Rate (%)')

    plt.savefig('total_infection_rate.svg')
    plt.show()

    plt.plot(svals, plot_max_infection_rates)
    plt.xlabel('S')
    plt.ylabel('Max Infection Rate (%)')

    plt.savefig('max_infection_rate.svg')
    plt.show()

    plt.plot(svals, plot_t_stops)
    plt.xlabel('S')
    plt.ylabel('T (Stop)')

    plt.savefig('t_stop.svg')
    plt.show()

    plt.plot(svals, plot_max_infection_times)
    plt.xlabel('S')
    plt.ylabel('Max Infection Time ')

    plt.savefig('max_infection_time.svg')
    plt.show()


if __name__ == '__main__':
    main()
