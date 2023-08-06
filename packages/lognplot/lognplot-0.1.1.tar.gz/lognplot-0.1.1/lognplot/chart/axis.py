import math
from ..time import TimeSpan


class Axis:
    """ Implement an axis with a minimum and maximum value.

    This class can also be used to generate appropriate tick values
    for the axis.
    """

    def __init__(self):
        self.minimum = -30
        self.maximum = 130

    def zoom(self, amount, around=None):
        """ Zoom this axis by a certain amount, optionally around the given value. """
        domain = self.domain
        if domain < 1e-18 and amount < 0:
            return

        if domain > 1e18 and amount > 0:
            return

        step = domain * amount
        if around is not None and self.minimum < around < self.maximum:
            left_part = (around - self.minimum) / domain
            assert left_part < 1.0
            right_part = 1.0 - left_part
            step_left = step * left_part
            step_right = step * right_part
        else:
            step_left = step_right = step

        self.minimum -= step_left
        self.maximum += step_right

    def pan_relative(self, amount):
        """ Pan a percentage of the axis range. """
        domain = self.domain
        step = domain * amount
        self.pan_absolute(step)

    def pan_absolute(self, step):
        """ Move the axis view by an absolute amount. """
        self.minimum += step
        self.maximum += step

    def set_limits(self, minimum, maximum):
        """ Set the ends of the axis. """
        assert maximum > minimum
        self.minimum = minimum
        self.maximum = maximum

    def get_timespan(self):
        begin = self.minimum
        end = self.maximum
        assert begin <= end
        return TimeSpan(begin, end)

    def get_ticks(self, n_ticks):
        """ Get tick values for this axis.

        This function should take care of the following:
        - tick values are rounded to logical multiples, such as 1, 2 or 0.2
        - tick values are returned as tuples of values and the string label.
        """
        domain = self.domain

        # Check for too small domain:
        assert not math.isclose(domain, 0)

        scale = math.floor(math.log10(domain))
        # print('domain', domain, 'scale', scale)
        approx = math.pow(10, -scale) * domain / n_ticks
        options = [0.1, 0.2, 0.5, 1.0, 2.0, 5.0]
        best = min(options, key=lambda x: abs(x - approx))

        step_size = best * math.pow(10, scale)
        start = ceil_to_multiple_of(self.minimum, step_size)
        end = self.maximum

        values = float_range(start, end, step_size)

        # If values are bigger than 1, do not use decimal
        # point.
        # If values are below 1, then use decimal rounding.
        # TODO, maybe return a gain factor, and scale the values?
        # TODO: maybe return an offset?
        if scale > 0:
            # Use integer values
            fmt = lambda x: f"{int(x)}"
        else:
            digits = -scale + 1
            fmt = lambda x: f"{round(x,digits):.0{digits}f}"

        return [(x, fmt(x)) for x in values]

    @property
    def domain(self):
        return self.maximum - self.minimum


def float_range(start, end, stepsize):
    values = []
    assert start < end
    assert stepsize > 0
    value = start
    while value < end:
        values.append(value)
        value += stepsize
    return values


def ceil_to_multiple_of(value, step):
    """ Round the given value to integer multiples of step.
    """
    assert step > 0
    offset = value % step
    if offset > 0:
        extra = step - offset
        return value + extra
    else:
        return value
