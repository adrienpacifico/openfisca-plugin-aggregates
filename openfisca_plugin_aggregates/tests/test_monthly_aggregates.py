# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014, 2015 OpenFisca Team
# https://github.com/openfisca
#
# This file is part of OpenFisca.
#
# OpenFisca is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# OpenFisca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from openfisca_france_data.tests import base
from openfisca_france_data.surveys import SurveyScenario
from openfisca_france_data.input_data_builders import get_input_data_frame, get_monthly_input_data_frame #TODO : mensualized make a global solution for monthly and period
from openfisca_plugin_aggregates.aggregates import Aggregates


from openfisca_core import periods
import openfisca_france
OFF_TBS = openfisca_france.init_country()
openfisca_france_tax_benefit_system = OFF_TBS()



def create_survey_scenario(year = None):
    assert year is not None
    dataframe_by_periods = get_monthly_input_data_frame(year) #get_input_data_frame(year)  #TODO : mensualized modifié ! Attention !

    period = periods.period(year)
    assert "wprm" in dataframe_by_periods[period].columns


    #import ipdb ; ipdb.set_trace()




    survey_scenario = SurveyScenario().init_from_data_frames_by_period(   #TODO : comprendre les import du taxbenefit et où  est ajoutée la variable weight
        input_data_frames_by_periods = dataframe_by_periods,
        tax_benefit_system = base.france_data_tax_benefit_system,
        year = year,
        )
    return survey_scenario


def test_aggregates(year = 2009):
    survey_scenario = create_survey_scenario(year)
    aggregates = Aggregates(survey_scenario = survey_scenario)
    aggregates.compute_aggregates()
    #aggregates.compute_specific_variables()
    return aggregates.base_data_frame


if __name__ == '__main__':
    import logging
    log = logging.getLogger(__name__)
    import sys
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)
    df = test_aggregates()
    print df