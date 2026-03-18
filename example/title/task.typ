#set text(size: 11pt)

#set page(
	header: context {
		let pageno = counter(page).get().first()
		if pageno > 1 [
			#move(dy: 0cm)[
				#grid(
					columns: (75%, 20%),
					column-gutter: 0.6cm,
					align: (left, right),
%if not solution:
					[#smallcaps[${name} ${date}]],
					%else:
					[#smallcaps[Musterlösung -- nicht kopieren!]],
%endif
					[#counter(page).display() von #counter(page).final().first()],
				)
				#v(-0.25cm)
				#line(length: 100%, stroke: 0.5pt)
			]
		]
	},
)

#set page(margin: 2cm)

%if not solution:
#place(top + right, dx: 0cm, dy: 0cm)[#image("${h.render("logo.svg")}", width: 3.5cm)]

#place(top + left, dx: 0cm, dy: 1cm)[#text(size: 14pt, weight: "bold")[Modul: ${name}]]
#place(top + left, dx: 0cm, dy: 1.75cm)[#text(size: 12pt)[Fakultät für Technik]]
#place(top + left, dx: 0cm, dy: 3cm)[#text(size: 10pt)[Studiengang: ${subject}]]
#place(top + right, dx: 0cm, dy: 3cm)[#text(size: 10pt)[Datum: ${date}]]

#v(4cm)
#line(length: 100%, stroke: 0.5pt)

#table(
	columns: (4cm, 6cm, 4cm, 4cm),
	stroke: none,
	inset: 8pt,
	[*Matrikelnummer:*], [..........................................], [Semester:], [${semester}],
	[Dozent:], [${lecturer}], [Kurs:], [${year}],
	[Hilfsmittel:], [
	%for supply in supplies:
		- ${supply}
	%endfor
	], [Bearbeitungszeit:], [${time}],
	[Max. Punktzahl:], [${total_number_points}], [], [],
	[Anmerkungen:], [], [], [],
)
#line(length: 100%, stroke: 0.5pt)

#table(
	columns: (5cm, 5cm, 5cm),
	stroke: 0.5pt,
	inset: 6pt,
	[*Aufgabennummer*], [*Maximale Punktzahl*], [*Bemerkung*],
%for no in range(1, total_number_tasks + 1):
	[${no}], [${points_of[no]}], [ ],
%endfor
)

#v(1.2cm)
#set par(justify: true)

Es sind grundsätzlich *alle Rechenwege* anzugeben und die Klausur ist dokumentenecht ohne Verwendung der Farben rot/grün auszufüllen. Diese Klausur besteht aus *#context[#counter(page).final().first()] Seiten*. Stellen Sie vor Beginn der Bearbeitung sicher, dass Sie alle Seiten vollständig erhalten haben. Wenn die Tackerung der Seiten entfernt wird, muss auf jedem getrennten Blatt die Matrikelnummer vermerkt werden, andernfalls wird das getrennte Blatt nicht gewertet. Ein programmierbarer Taschenrechner oder ein Taschenrechner mit CAS stellt ein *unzulässiges Hilfsmittel* dar und die Verwendung wird als Unterschleif gewertet. Viel Erfolg.
%else:
#place(
	center + horizon,
	dx: 0pt,
	dy: 0pt,
	[
		#align(center)[	
			#text(size: 36pt, weight: "bold")[#smallcaps[Musterlösung]]

			#text(size: 24pt)[#smallcaps[Nicht kopieren]]

			${name}
			
			${lecturer}

			${date}
		]
	]
)
%endif


#set page(margin: (
	top: 3.5cm,
	bottom: 2cm,
	left: 2cm,
	right: 2cm,
))
