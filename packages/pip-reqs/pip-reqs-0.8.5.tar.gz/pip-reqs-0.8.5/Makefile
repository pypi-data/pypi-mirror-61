ptest:
	tox -e $$(tox -l | grep test | paste -s -d,) -p all
	tox -e lint
	tox -e coverage

test:
	tox
