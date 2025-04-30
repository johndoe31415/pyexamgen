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

import json
import collections

class RendererHelper():
	def __init__(self, exam_renderer: "ExamRenderer"):
		self._exam_renderer = exam_renderer
		self._task_count = 0
		self._points_count = 0
		self._points_of = collections.defaultdict(int)

	@property
	def task_count(self):
		return self._task_count

	@property
	def points_count(self):
		return self._points_count

	@property
	def points_of(self):
		return self._points_of

	@property
	def current_task_no(self):
		return self._task_count

	def freeze(self):
		return {
			"points_of": dict(self.points_of),
			"total_number_tasks": self.task_count,
			"total_number_points": self.points_count,
		}

	def next_task_no(self):
		self._task_count += 1
		return self._task_count

	def count_points(self, pts: str):
		pts = self.parse_points(pts)
		self._points_count += pts
		self._points_of[self.current_task_no] += pts

	def parse_points(self, pts: str):
		if pts.isdigit():
			return int(pts)
		else:
			return float(pts)

	def render(self, filename):
		if filename.endswith(".svg"):
			return self._exam_renderer.render_svg(filename)
		elif filename.endswith(".gpl"):
			return self._exam_renderer.render_gnuplot(filename)
		else:
			raise ValueError(f"Do not know how to render this file: {filename}")

	def spacestr_la(self, string: str, group_len: int):
		"""Left-align a string in a spaced fashion."""
		pieces = [ string[i : i + group_len ] for i in range(0, len(string), group_len) ]
		return " ".join(pieces)

	def spacestr_ra(self, string: str, group_len: int):
		"""Right-align a string in a spaced fashion."""
		m = len(string) % group_len
		if m == 0:
			return self.spacestr_la(string, group_len)
		else:
			return string[:m] + " " + self.spacestr_la(string[m:], group_len)
