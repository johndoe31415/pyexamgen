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

import struct
import hashlib

class PRNG():
	def __init__(self, seed: bytes):
		self._seed = seed
		self._buffer = bytearray()
		self._counter = 0

	def _fill_until(self, length: int):
		while len(self._buffer) < length:
			self._buffer += self._nextblock()

	def _nextblock(self):
		data = hashlib.md5(self._seed + struct.pack("Q", self._counter)).digest()
		self._counter += 1
		return data

	def get_bytes(self, length: int):
		self._fill_until(length)
		(return_value, self._buffer) = (self._buffer[:length], self._buffer[length:])
		return return_value

	def _get_byte_int(self, length: int):
		return int.from_bytes(self.get_bytes(length), byteorder = "little")

	def randrange(self, max_value_exclusive: int):
		assert(max_value_exclusive > 0)
		if max_value_exclusive == 1:
			return 0

		min_bits = (max_value_exclusive - 1).bit_length()
		min_bytes = (min_bits + 7) // 8
		mask = (1 << min_bits) - 1

		while True:
			value = self._get_byte_int(min_bytes) & mask
			if value < max_value_exclusive:
				return value

	def randint(self, min_value_inclusive: int, max_value_inclusive: int):
		return min_value_inclusive + self.randrange(max_value_inclusive - min_value_inclusive + 1)

	def shuffle(self, shuffle_obj: list):
		n = len(shuffle_obj)
		for i in range(n - 1):
			j = self.randint(i, n - 1)
			(shuffle_obj[i], shuffle_obj[j]) = (shuffle_obj[j], shuffle_obj[i])

	def k_of_n(self, k: int, n: int):
		assert(k <= n)
		values = list(range(n))
		self.shuffle(values)
		return set(values[:k])

if __name__ == "__main__":
	prng = PRNG(b"foobar")
#	print(prng.get_bytes(3))
#	print(prng.get_bytes(2))

	for i in range(1000000):
		print(prng.k_of_n(2, 4))
