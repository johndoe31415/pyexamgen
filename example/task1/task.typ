<%namespace file="common.typ" name="common" import="*"/>
<%common:task text="Codes">
	<%common:question pts="1">
		<%
			value = prng.randint(2**10, 2**14)
		%>\
		Wandeln Sie die Zahl $${h.spacestr_ra(f'{value:b}', 4)}_2$ in das Hexadezimalsystem um.
		<%common:answer>
		$${f'{value:b}'}_2 = ${f'{value:x}'}_16$
		</%common:answer>
	</%common:question>

	<%common:question pts="1.5">
		<%
			value = prng.randint(2**3, 2**10)
			states = math.ceil(math.log(value, 2))
		%>\
		Wie viele Bit werden mindestens benötigt, um ${value} diskrete Zustände zu kodieren? Zeigen Sie Ihren Rechenweg.
		<%common:answer>
		$ceil(log_2 ${value}) = ${states}$
		</%common:answer>
	</%common:question>

	<%common:question pts="2">
		<%
			bit = prng.randint(8, 12)
			unused = prng.randint(8, 200)
			codes = (2 ** bit) - unused
		%>\
		Es werden ${codes} distinkte Codes in ${bit} Bit kodiert. Wie viele Bitmuster werden nicht von Codewörtern verwendet?
		<%common:answer>
		In ${bit} Bit lassen sich ${2 ** bit} Codewörter abspeichern. Demnach sind $${2 ** bit} - ${codes} = ${unused}$ Codewörter ungenutzt.
		</%common:answer>
	</%common:question>

	<%common:question pts="1">
		Gegeben sei folgender Code:
		#table(
			columns: (auto, auto),
			stroke: 0.5pt,
			inset: 4pt,
			[*Code*], [*Codewort*],
			[0], [1],
			[1], [00],
			[2], [011010],
			[3], [011110],
			[4], [011011],
			[5], [0111101],
		)
		Ist der hier gezeigte Code präfixfrei? Begründen Sie Ihre Antwort.
		<%common:answer>
		Nein, denn Codewort 3 ist ein Präfix von Codewort 5.
		</%common:answer>
	</%common:question>
</%common:task>
