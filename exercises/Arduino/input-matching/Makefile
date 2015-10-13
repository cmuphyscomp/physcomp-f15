# Compile the diagram if needed.  This requires a graphviz installation.

input_matching_state_transition_diagram.png: input_matching_state_transition_diagram.dot
	dot -T png -o $@ $< 

clean:
	-rm input_matching_state_transition_diagram.png
