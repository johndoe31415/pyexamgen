<%namespace file="common.typ" name="common" import="*"/>
<%common:task text="Gatter">
Gegeben sei folgende Schaltung:

//\includegraphics[width=8cm]{${h.render("example_gatter.svg")}}
	<%common:question pts="1">
        Handelt es sich bei der Schaltung um ein Schaltnetz oder ein Schaltwerk? Begründen Sie Ihre Antwort.
		<%common:answer>
		Lösung für Aufgabe 1
		</%common:answer>
	</%common:question>

	<%common:question pts="1">
        Nennen Sie einen Booleschen Ausdruck, der $Y$ in Abhängigkeit von $A, B, C$ beschreibt.
		<%common:answer>
		Lösung für Aufgabe 2
		</%common:answer>
	</%common:question>

	<%common:question pts="1">
		// digtick parse -f typst-tech 'A !C + (B ^ C) + !<A + !<!B + C>>'
        Zeichnen Sie den Ausdruck
		$ upright(A) overline(upright(C)) or (upright(B) xor upright(C)) or overline(upright(A) or overline(overline(upright(B)) or upright(C))) $
		also
		// digtick parse -f typst-math 'A !C + (B ^ C) + !<A + !<!B + C>>'
		$ upright(A) not upright(C) or (upright(B) xor upright(C)) or not (upright(A) or not (not upright(B) or upright(C))) $
		als elektronische Schaltung.
		<%common:answer>
		Lösung für Aufgabe 3
		</%common:answer>
	</%common:question>
</%common:task>
