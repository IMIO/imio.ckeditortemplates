#!/usr/bin/make
all: run

bin/pip:
	if [ -f /usr/bin/virtualenv-2.7 ] ; then virtualenv-2.7 .;else virtualenv -p python2.7 .;fi

bin/buildout: bin/pip
	./bin/pip install -r requirements.txt

.PHONY: buildout
buildout: bin/buildout
	bin/buildout -t 7

.PHONY: test
test: buildout
	bin/test

.PHONY: run
run: buildout
	bin/instance1 fg

.PHONY: cleanall
cleanall:
	rm -fr develop-eggs downloads eggs parts .installed.cfg lib include bin .mr.developer.cfg
