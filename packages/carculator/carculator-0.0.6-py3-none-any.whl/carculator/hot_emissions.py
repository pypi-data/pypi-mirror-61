import numpy as np
import xarray
import numexpr as ne


def _(o):
    """Add a trailing dimension to make input arrays broadcast correctly"""
    if isinstance(o, (np.ndarray, xarray.DataArray)):
        return np.expand_dims(o, -1)
    else:
        return o


class HotEmissionsModel:
    """
    Calculate hot pollutants emissions based on HBEFA 4.1 data, function of speed (given by the driving cycle)
    for vehicles with a combustion engine.

    :param cycle: Driving cycle. Pandas Series of second-by-second speeds (km/h) or name (str)
        of cycle e.g., "WLTC","WLTC 3.1","WLTC 3.2","WLTC 3.3","WLTC 3.4","CADC Urban","CADC Road",
        "CADC Motorway","CADC Motorway 130","CADC","NEDC".
    :type cycle: pandas.Series

    """

    def __init__(self, cycle):

        self.cycle = cycle

    def get_emissions_per_powertrain(self, powertrain_type):
        """
        Calculate hot pollutants emissions given a powertrain type (i.e., diesel, petrol, CNG), per air sub-compartment
        (i.e., urban, suburban and rural).

        The emission sums are further divided into `air compartments`: urban, suburban and rural.

            * *urban*: from 0 to 50 km/k
            * *suburban*: from 51 km/h to 80 km/h
            * *rural*: above 80 km/h


        :return: Pollutants emission per km driven, per air compartment.
        :rtype: numpy.array
        """
        c = self.cycle

        em_arr = np.zeros((len(self.cycle), 11))

        if powertrain_type == "diesel":
            # HC
            em_arr[:, 0] = ne.evaluate("1.42e-09 * c ** 3 - 3.905e-07 * c ** 2 + 6.247e-05 * c + 0.004804")
            # CO
            em_arr[:, 1] = ne.evaluate("2.6e-09 * c ** 3 + 9.256e-07 * c ** 2 - 0.0002761 * c + 0.02438")
            # NOx + NO2
            em_arr[:, 2] = ne.evaluate("(1.159e-07 * c ** 3 - 1.891e-05 * c ** 2 + 0.0008328 * c + 0.01852) + (4.056e-08 * c ** 3 - 6.618e-06 * c ** 2 + 0.0002915 * c + 0.006481)")
            # PM <= 2.5 um
            em_arr[:, 3] = ne.evaluate("2.12e-09 * c ** 3 - 4.61e-07 * c ** 2 + 3.018e-05 * c - 0.0001433")
            # CH4
            em_arr[:, 4] = ne.evaluate("1.278e-09 * c ** 3 - 3.514e-07 * c ** 2  + 5.622e-05 * c + 0.004324")
            # NMVOC
            em_arr[:, 5] = ne.evaluate("1.42e-10 * c ** 3 - 3.905e-08 * c ** 2 + 6.247e-06 * c + 0.0004804")
            # Pb
            # No Pb!
            # SO2
            em_arr[:, 7] = ne.evaluate("2.631e-10 * c ** 3 + 1.122e-08 * c ** 2 - 6.082e-06 * c + 0.001071")
            # N2O
            em_arr[:, 8] = ne.evaluate("-0.000107 * c + 0.01941")
            # NH3
            em_arr[:, 9] = ne.evaluate("1.927e-05 * c + 0.006249")
            # Benzene
            em_arr[:, 10] = ne.evaluate("1.136e-11 * c ** 3 - 3.124e-09 * c ** 2 + 4.998e-07 * c + 3.844e-05")

        if powertrain_type == "petrol":
            # HC
            em_arr[:, 0] = ne.evaluate("-6.698e-09 * c ** 3 + 2.661e-06 * c ** 2 - 0.0002239 * c + 0.008068")
            # CO
            em_arr[:, 1] = ne.evaluate("5.385e-07 * c ** 3 - 0.0001104 * c ** 2 + 0.006821 * c + 0.1707")
            # NO + NO2
            em_arr[:, 2] = ne.evaluate("(1.379e-07 * c ** 3 - 2.708e-05 * c ** 2 + 0.001678 * c - 0.01762) + (6.894e-09 * c ** 3 - 1.354e-06 * c ** 2 + 8.388e-05 * c - 0.0008809)")
            # PM <= 2.5 um
            em_arr[:, 3] = ne.evaluate("-3.18e-10 * c ** 3 + 2.95e-07 * c ** 2 - 2.911e-05 * c + 0.001359")
            # CH4
            em_arr[:, 4] = ne.evaluate("-2.679e-09 * c ** 3 + 1.064e-06 * c ** 2 - 8.957e-05 * c + 0.003227")
            # NMVOC
            em_arr[:, 5] = ne.evaluate("-4.019e-09 * c ** 3 + 1.597e-06 * c ** 2 - 0.0001344 * c + 0.004841")
            # Pb
            em_arr[:, 6] = ne.evaluate("-2.062e-11 * c ** 3 + 9.669e-09 * c ** 2 - 1.099e-06 * c + 7.273e-05")
            # SO2
            em_arr[:, 7] = ne.evaluate("-3.264e-10 * c ** 3 + 1.53e-07 * c ** 2 - 1.74e-05 * c + 0.001151")
            # N2O
            em_arr[:, 8] = ne.evaluate("-6.351e-06 * c + 0.0007994")
            # NH3
            em_arr[:, 9] = ne.evaluate("9.559e-05 * c + 0.009297")
            # Benzene
            em_arr[:, 10] = ne.evaluate("-6.698e-11 * c ** 3 + 2.661e-08 * c ** 2 - 2.239e-06 * c + 8.068e-05")

        if powertrain_type == "CNG":
            # HC
            em_arr[:, 0] = ne.evaluate("5.502e-08 * c ** 3 - 1.239e-05 * c ** 2 + 0.000846 * c - 0.004044")
            # CO
            em_arr[:, 1] = ne.evaluate("2.678e-06 * c ** 3 - 0.0005585 * c ** 2 + 0.03632 * c - 0.5159")
            # NO + NO2
            em_arr[:, 2] = ne.evaluate("(2.163e-08 * c ** 3 - 3.758e-06 * c ** 2 + 5.485e-05 * c + 0.02848) + (4.35e-09 * c ** 3 - 7.625e-07 * c ** 2 + 2.251e-05 * c + 0.002413)")
            # PM <= 2.5 um
            em_arr[:, 3] = ne.evaluate("1.997e-09 * c ** 3 - 2.116e-07 * c ** 2 - 1.277e-05 * c + 0.002135")
            # CH4
            em_arr[:, 4] = ne.evaluate("4.568e-08 * c ** 3 - 1.052e-05 * c ** 2 + 0.0007284 * c - 0.003946")
            # NMVOC
            em_arr[:, 5] = ne.evaluate("9.338e-09 * c ** 3 - 1.872e-06 * c ** 2 + 0.0001175 * c - 9.78e-05")
            # Pb
            em_arr[:, 6] = ne.evaluate("-1.38e-11 * c ** 3 + 6.464e-09 * c ** 2 - 7.366e-07 * c + 4.665e-05")
            # SO2
            em_arr[:, 7] = ne.evaluate("-2.185e-10 * c ** 3 + 1.023e-07 * c ** 2 - 1.166e-05 * c + 0.0007384")
            # N2O
            em_arr[:, 8] = ne.evaluate("-7.104e-06 * c + 0.0008573")
            # NH3
            em_arr[:, 9] = ne.evaluate("8.615e-05 * c + 0.01022")
            # Benzene
            em_arr[:, 10] = ne.evaluate("9.493e-11 * c ** 3 - 1.694e-08 * c ** 2 + 9.587e-07 * c + 4.34e-06")

        if powertrain_type not in ("petrol", "diesel", "CNG"):
            raise TypeError(
                "The powertrain type is not valid."
            )

        distance = self.cycle.sum() / 3600
        dist_urban = self.cycle[self.cycle <= 50].sum() / 3600
        dist_suburban = self.cycle[(self.cycle > 50) & (self.cycle <= 80)].sum() / 3600
        dist_rural = self.cycle[self.cycle > 80].sum() / 3600

        urban = np.mean(em_arr[self.cycle <= 50], axis=0) * (dist_urban / distance)
        urban /= 1000  # going from grams to kg
        suburban = np.mean(em_arr[(self.cycle > 50) & (self.cycle <= 80)], axis=0) * (
            dist_suburban / distance
        )
        suburban /= 1000  # going from grams to kg
        rural = np.mean(em_arr[self.cycle > 80], axis=0) * (dist_rural / distance)
        rural /= 1000  # going from grams to kg

        suburban = np.nan_to_num(suburban)
        rural = np.nan_to_num(rural)

        return (urban, suburban, rural)
