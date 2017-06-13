#!/usr/bin/python3

# Copyright 2017 Francisco Pina Martins <f.pinamartins@gmail.com>
# This file is part of structure_threader.
# structure_threader is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# structure_threader is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with structure_threader. If not, see <http://www.gnu.org/licenses/>.

import os
import logging

try:
    import colorer.colorer as colorer
except ImportError:
    import structure_threader.colorer.colorer as colorer


def mav_cli_generator(arg, k_val):
    """
    Generates and returns the command line to run MavericK.
    """
    # MavericK requires a trailing "/" (or "\" if on windows)
    output_dir = os.path.join(arg.outpath, "mav_K" + str(k_val)) + os.path.sep
    try:
        os.mkdir(output_dir)
    except FileExistsError:
        pass
    if os.name == "nt":
        root_dir = ""
    else:
        root_dir = "/"
    cli = [arg.external_prog, "-Kmin", str(k_val), "-Kmax", str(k_val), "-data",
           arg.infile, "-outputRoot", output_dir, "-masterRoot",
           root_dir, "-parameters", arg.params]
    if arg.notests is True:
        cli += ["-thermodynamic_on", "f"]

    return cli


def mav_params_parser(arg):
    """
    Parses MavericK's parameter file and switches some options if necessary.
    """
    param_file = open(arg.params, "r")
    for lines in param_file:
        if lines.startswith("thermodynamic_on"):
            ti_status = lines.split()[1].lower()
            if ti_status in ("f", "false", "0"):
                arg.no_tests = True
                logging.error("Thermodynamic integration is turned OFF."
                              "BestK tests will be skipped.")

    param_file.close()
