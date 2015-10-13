# Compile the diagram if needed.  This requires a graphviz installation.

input_hysteresis_state_transition_diagram.png: input_hysteresis_state_transition_diagram.dot
	dot -T png -o $@ $< 

clean:
	-rm input_hysteresis_state_transition_diagram.png
