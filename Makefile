PY=python3

# Unit tests
ut:
	$(PY) -m unittest discover -p 'test*.py'

# Acceptance tests
acc: ut
	$(PY) acctest.py

tags:
	ctags *.py

1ut:
	$(PY) test_syllable.py TestLetter.test_latex

.PHONY: test tags run ut acc
