# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright (C) 2018-2019 GEM Foundation
#
# OpenQuake is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# OpenQuake is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with OpenQuake. If not, see <http://www.gnu.org/licenses/>.
import sys
from openquake.baselib import sap
from openquake.commonlib import readinput
from openquake.calculators import base
from openquake.hazardlib import nrml
from openquake.risklib import read_nrml  # this is necessary


@sap.script
def check_input(job_ini_or_zip_or_nrml):
    if job_ini_or_zip_or_nrml.endswith('.xml'):
        try:
            print(nrml.to_python(job_ini_or_zip_or_nrml))
        except Exception as exc:
            sys.exit(exc)
    else:
        calc = base.calculators(readinput.get_oqparam(job_ini_or_zip_or_nrml))
        calc.read_inputs()


check_input.arg('job_ini_or_zip_or_nrml', 'Check the input')
