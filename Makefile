test:
	python3 -m pytest

validate:
	python3 schema/validate.py

demo:
	python3 examples/demo-run/run_demo.py

.PHONY: test validate demo
