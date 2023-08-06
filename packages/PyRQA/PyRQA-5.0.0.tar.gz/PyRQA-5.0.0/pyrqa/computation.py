#!/usr/bin/env python

"""
Factories for creating recurrence analysis computations.
"""

from pyrqa.exceptions import UnsupportedNeighbourhoodException
from pyrqa.neighbourhood import FixedRadius, RadiusCorridor, FAN

from pyrqa.variants.rp.radius.execution_engine import ExecutionEngine as RPExecutionEngine
from pyrqa.variants.rqa.radius.execution_engine import ExecutionEngine as RQAExecutionEngine

__author__ = "Tobias Rawald"
__copyright__ = "Copyright 2015, 2018, 2019, 2020 The PyRQA project"
__credits__ = ["Tobias Rawald",
               "Mike Sips"]
__license__ = "Apache-2.0"
__maintainer__ = "Tobias Rawald"
__email__ = "pyrqa@gmx.net"
__status__ = "Development"


class RPComputation(object):
    """
    Factory for creating a recurrence plot computation.
    """

    @classmethod
    def create(cls,
               settings,
               **kwargs):
        """
        Create RQA computation.

        :param settings: Recurrence analysis settings.
        :param kwargs: Keyword arguments.
        """

        if isinstance(settings.neighbourhood, FixedRadius) or isinstance(settings.neighbourhood, RadiusCorridor):
            return RPExecutionEngine(settings,
                                     **kwargs)
        elif isinstance(settings.neighbourhood,
                        FAN):
            raise UnsupportedNeighbourhoodException("Neighbourhood '%s' is not yet supported!" % settings.neighbourhood.__class__.__name__)
        else:
            raise UnsupportedNeighbourhoodException("Neighbourhood '%s' is not supported!" % settings.neighbourhood.__class__.__name__)


class RQAComputation(object):
    """
    Factory for creating a recurrence quantification analysis computation.
    """

    @classmethod
    def create(cls,
               settings,
               **kwargs):
        """
        Create recurrence plot computation.

        :param settings: Recurrence analysis settings.
        :param kwargs: Keyword arguments.
        """

        if isinstance(settings.neighbourhood, FixedRadius) or isinstance(settings.neighbourhood, RadiusCorridor):
            return RQAExecutionEngine(settings,
                                      **kwargs)
        elif isinstance(settings.neighbourhood,
                        FAN):
            raise UnsupportedNeighbourhoodException("Neighbourhood '%s' is not yet supported!" % settings.neighbourhood.__class__.__name__)
        else:
            raise UnsupportedNeighbourhoodException("Neighbourhood '%s' is not supported!" % settings.neighbourhood.__class__.__name__)
