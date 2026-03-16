<%namespace file="common.typ" name="common" import="*"/>
<%common:task text="Arithmetik">
	<% tasks = prng.k_of_n(2, 3) %>
	%if 0 in tasks:
	<%common:question pts="1">
        Repräsentieren Sie die Zahl -42 als 8-Bit Zahl im Zweierkomplement. Zeigen Sie Ihren Rechenweg.
		<%common:answer>
		Lösung für Aufgabe 1
		</%common:answer>
	</%common:question>
	%endif

	%if 1 in tasks:
	<%common:question pts="1">
        Welche Zahl stellt die 5-Bit Zahl $10101_2$ dar, wenn sie intern im Zweierkomplement dargestellt wird? Zeigen Sie Ihren Rechenweg.
		<%common:answer>
		Lösung für Aufgabe 2
		</%common:answer>
	</%common:question>
	%endif

	%if 2 in tasks:
	<%common:question pts="1">
        Berechnen Sie auf einer 8-Bit Maschine, die das Zweierkomplement verwendet, die Rechnung $99 - 123$; beschreiben Sie den Rechenweg vollständig.
		<%common:answer>
		Lösung für Aufgabe 3
		</%common:answer>
	</%common:question>
	%endif
</%common:task>
