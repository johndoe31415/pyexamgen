#	pyexamgen - Generate LaTeX/Typst exams using advanced Mako templates
#	Copyright (C) 2023-2026 Johannes Bauer
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
import os
from .ExamRenderer import ExamRenderer
from .FriendlyArgumentParser import FriendlyArgumentParser

def main():
	parser = FriendlyArgumentParser(description = "Render an JSON exam file to PDF.")
	parser.add_argument("-d", "--draft-mode", action = "store_true", help = "Produce document as quickly as possible, e.g., by skipping two-pass rendering. This may lead to broken cross-references in the final file, but will render more quickly.")
	parser.add_argument("-s", "--output-source-doc", action = "store_true", help = "Instead of PDFs, just generate raw TeX or Typst. Useful for debugging.")
	parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increases verbosity. Can be specified multiple times to increase.")
	group = parser.add_mutually_exclusive_group()
	group.add_argument("--only-exam", action = "store_true", help = "Only generate the exam, skip generation of the solution.")
	group.add_argument("--only-solution", action = "store_true", help = "Only generate the solution, skip generation of the exam.")
	parser.add_argument("-R", "--randomize-task-seed", metavar = "name", action = "append", default = [ ], help = "Randomize the seed of this sheet name. Can be given multiple times. Keyword 'root' randomizes the main seed.")
	parser.add_argument("-r", "--randomize-all-task-seeds", action = "store_true", help = "Where no explicit task seed is given, randomize it for every single task.")
	parser.add_argument("-l", "--loop", action = "store_true", help = "Repeatedly generate output. Useful for example when randomizing task seeds.")
	parser.add_argument("definition_json", help = "JSON file that defines what parts to include in the exam.")
	args = parser.parse_args(sys.argv[1:])

	while True:
		seed_overrides = { name: os.urandom(8).hex() for name in args.randomize_task_seed }
		if len(seed_overrides) > 0:
			print(f"Randomized seeds: {', '.join(f'{name} = {value}' for (name, value) in sorted(seed_overrides.items()))}")

		renderer = ExamRenderer(args.definition_json, output_source_doc = args.output_source_doc, seed_overrides = seed_overrides, draft_mode = args.draft_mode, randomize_all_task_seeds = args.randomize_all_task_seeds, verbose = args.verbose)
		if not args.only_solution:
			renderer.render_exam()
		if not args.only_exam:
			renderer.render_solution()
		if not args.loop:
			break
		else:
			input("Press ENTER to regenerate...")
