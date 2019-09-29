import pandas as pd


class Lightning:

    @staticmethod
    def get_df(response):

        col_names = [
            "version", "year", "month", "day", "hour", "minutes", "seconds", "nanoseconds",
            "latitude", "longitude", "peakCurrent", "multiplicity", "numSensors",
            "degreesOfFreedom", "ellipseAngle", "semiMajorAxis", "semiMinorAxis", "chiSquareValue",
            "riseTime", "peakToZeroTime", "maxRateOfRise", "cloudIndicator", "angleIndicator", "signalIndicator", "timingIndicator"
        ]

        int_type = (
            [True for i in range(8)] + [False for i in range(2)]
            + [True for i in range(4)] + [False for i in range(7)] + [True for i in range(4)]
        )

        lst = []
        for line in response.text.split('\n')[:-1]:  # Last line is empty
            lst.append([])
            for int_t, i in zip(int_type, line.split(' ')):
                try:
                    if int_t:
                        lst[-1].append(int(i))
                    else:
                        lst[-1].append(float(i))
                except ValueError:
                    print(",", i, int_t)

        return pd.DataFrame(lst, columns=col_names)