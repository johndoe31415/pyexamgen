#	pyexamgen - Generate LaTeX exams using advanced Mako templates
#	Copyright (C) 2023-2025 Johannes Bauer
#
#	This file is part of pyexamgen.
#
#	pyexamgen is free software; you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation; this program is ONLY licensed under
#	version 3 of the License, later versions are explicitly excluded.
#
#	pyexamgen is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with pyexamgen; if not, write to the Free Software
#	Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#	Johannes Bauer <JohannesBauer@gmx.de>

import sys
from .ExamRenderer import ExamRenderer
from .FriendlyArgumentParser import FriendlyArgumentParser

def main():
	parser = FriendlyArgumentParser(description = "Render an JSON exam file to PDF.")
	parser.add_argument("-t", "--tex", action = "store_true", help = "Instead of PDFs, just generate raw TeX. Useful for debugging.")
	parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increases verbosity. Can be specified multiple times to increase.")
	parser.add_argument("definition_json", help = "JSON file that defines what parts to include in the exam.")
	args = parser.parse_args(sys.argv[1:])

	renderer = ExamRenderer(args.definition_json, output_tex = args.tex, verbose = args.verbose)
	renderer.render_exam()
	renderer.render_solution()
