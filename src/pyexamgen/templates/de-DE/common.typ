<%def name="task(text)">
	#pagebreak()

	#text(size: 14pt, weight: "bold")[Aufgabe ${h.next_task_no()}: ${text}]
	${caller.body()}
	%if not solution:
	#pagebreak()
	#text(size: 14pt, weight: "bold")[Lösung zur Aufgabe ${h.current_task_no}: ${text}]
	%endif

<%
	h.reset_question_counter()
%>
</%def>

<%def name="show_points(pts)">\
<% pts = h.parse_points(pts) %>\
%if isinstance(pts, int):
%if pts == 1:
1 Punkt\
%else:
${pts} Punkte\
%endif
%else:
${f'{pts:.1f}'} Punkte\
%endif
</%def>

<%def name="question(pts)">
<%
	h.count_points(pts)
	h.advance_question()
%>
	
	*Frage ${h.current_task_no}.${h.current_question_no}:* ${show_points(pts)}
	#pad(left: 1cm)[
		${caller.body()}
	]
	#v(0.5cm)
</%def>

<%def name="answer()">
%if solution:
_Lösung_: ${caller.body()}
%endif
</%def>

