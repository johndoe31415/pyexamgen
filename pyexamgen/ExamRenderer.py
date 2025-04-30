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

import os
import sys
import json
import math
import tempfile
import subprocess
import shutil
import mako.lookup
from .RendererHelper import RendererHelper
from .PRNG import PRNG
from .WorkDir import WorkDir

class ExamRenderer():
	def __init__(self, definition_filename: str, output_tex: bool = False, verbose: int = 0):
		self._definition_filename = definition_filename
		self._output_tex = output_tex
		self._verbose = verbose
		with open(definition_filename) as f:
			self._defs = json.load(f)
		self._frozen_data = None
		self._rendered = { }

	@property
	def template_dir(self):
		return f"{os.path.dirname(__file__)}/templates/{self._defs['locale']}"

	@property
	def basename(self):
		return os.path.splitext(os.path.basename(self._definition_filename))[0]

	@property
	def output_filename_exam(self):
		return f"{self.basename}.tex" if self._output_tex else f"{self.basename}.pdf"

	@property
	def output_filename_solution(self):
		return f"{self.basename}_solution.tex" if self._output_tex else f"{self.basename}_solution.pdf"

	@property
	def definition_directory(self):
		return os.path.dirname(self._definition_filename)

	def _render(self, render_input_filename, render_hook):
		if render_input_filename not in self._rendered:
			render_output_filename = f"{self._tempdir}/{len(self._rendered)}.pdf"
			render_hook(render_input_filename, render_output_filename)
			self._rendered[render_input_filename] = render_output_filename
		return self._rendered[render_input_filename]

	def _store_rendered(self, input_filename: str, output_suffix: str, data: bytes):
		output_filename = f"{len(self._rendered)}{output_suffix}"
		self._rendered[input_filename] = (output_filename, data)
		return output_filename

	def render_svg(self, svg_filename: str):
		full_svg_filename = self._current_source_dir + "/" + svg_filename
		if full_svg_filename not in self._rendered:
			with tempfile.NamedTemporaryFile(prefix = "exam_renderer_", suffix = ".pdf") as tmpfile:
				subprocess.check_call([ "inkscape", "-o", tmpfile.name, full_svg_filename ])
				self._store_rendered(full_svg_filename, ".pdf", tmpfile.read())
		return self._rendered[full_svg_filename][0]

	def render_gnuplot(self, gpl_filename: str):
		full_gpl_filename = self._current_source_dir + "/" + gpl_filename
		if full_gpl_filename not in self._rendered:
			rendered = subprocess.check_output([ "gnuplot", full_gpl_filename ])
			self._store_rendered(full_gpl_filename, ".pdf", rendered)
		return self._rendered[full_gpl_filename][0]

	def _render_fragment(self, fragment_definition: dict, template_vars: dict):
		prng_seed = self._defs.get("prng", "") + "::" + fragment_definition["name"] + "::" + fragment_definition.get("prng", "")

		if self._verbose >= 3:
			print(f"Rendering fragment {fragment_definition['name']} with PRNG seed \"{prng_seed}\"")
		fragment_directory = self.definition_directory + "/" + fragment_definition["name"]
		lookup = mako.lookup.TemplateLookup([ fragment_directory, self.template_dir ], strict_undefined = True)
		template = lookup.get_template("task.tex")
		template_vars = dict(template_vars)
		template_vars.update({
			"prng": PRNG(prng_seed.encode("utf-8")),
			"math": math,
		})
		rendered = template.render(**template_vars)
		return rendered

	def _do_render(self, extra_template_vars: dict):
		if self._verbose >= 2:
			print(f"Rendering pass with variables: {extra_template_vars}")

		template_vars = dict(self._defs["variables"])
		template_vars.update(extra_template_vars)
		if self._frozen_data is None:
			# On first pass, we need to make something up so the templates
			# render cleanly.
			template_vars.update(template_vars["h"].freeze())
		else:
			template_vars.update(self._frozen_data)
		chunks = [ ]
		for fragment in self._defs["sources"]:
			self._current_source_dir = self.definition_directory + "/" + fragment["name"]
			chunks.append(self._render_fragment(fragment, template_vars))
		return chunks

	def _tex_to_pdf(self, tex_input: str, output_filename_pdf: str):
		with tempfile.TemporaryDirectory() as tmpdir:
			with open(tmpdir + "/document.tex", "w") as f:
				f.write(tex_input)
			with WorkDir(tmpdir):
				for (src_filename, (dst_filename, content)) in self._rendered.items():
					with open(dst_filename, "wb") as f:
						f.write(content)
				for texrun in range(2):
					try:
						if self._verbose >= 1:
							print(f"Rendering TeX: {tmpdir}/document.tex")
						subprocess.check_call([ "pdflatex", "-halt-on-error", "-shell-escape", "document.tex" ], stdout = subprocess.DEVNULL if self._verbose < 2 else None, stderr = subprocess.DEVNULL if self._verbose < 2 else None)
					except subprocess.CalledProcessError:
						print(f"Fatal error: TeX rendering failed. TeX source: {tmpdir}/document.tex", file = sys.stderr)
						if self._verbose >= 2:
							input("Press RETURN to continue...")
			shutil.move(f"{tmpdir}/document.pdf", output_filename_pdf)

	def _render(self, template_vars: dict, output_filename: str):
		template_vars = dict(template_vars)
		template_vars["h"] = RendererHelper(self)
		if self._frozen_data is None:
			if self._verbose >= 2:
				print(f"First rendering pass to determine number of points/tasks.")
			# First pass to get number of points, etc
			self._do_render(template_vars)

			# After the first pass, we freeze the values we got.
			self._frozen_data = template_vars["h"].freeze()
			template_vars["h"] = RendererHelper(self)
		chunks = self._do_render(template_vars)

		# Now render final TeX document
		lookup = mako.lookup.TemplateLookup([ self.definition_directory, self.template_dir ], strict_undefined = True)
		template = lookup.get_template("base.tex")
		template_vars = {
			"chunks": chunks,
		}
		if "local_includes" in self._defs:
			with open(self.definition_directory + "/" + self._defs["local_includes"]) as f:
				template_vars["local_includes"] = f.read()
		else:
			template_vars["local_includes"] = ""
		tex_result = template.render(**template_vars)

		if self._output_tex:
			with open(output_filename, "w") as f:
				f.write(tex_result)
		else:
			self._tex_to_pdf(tex_result, output_filename)

	def render_exam(self):
		self._render({
			"solution":		False,
		}, self.output_filename_exam)

	def render_solution(self):
		self._render({
			"solution":		True,
		}, self.output_filename_solution)
