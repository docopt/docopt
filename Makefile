help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  cleandist       remove temporary files created by build tools"
	@echo "  cleanegg        remove folders created by sdist command"
	@echo "  cleantox        remove folders created by tox"
	@echo "  cleanpy         remove python temporary files"
	@echo "  cleanall        all the above + tmp files from development tools"

cleandist:
	-rm -rf dist/
	-rm -rf build/

cleanegg:
	-rm -rf docopt.egg-info/

cleantox:
	-rm -rf .tox

cleanpy:
	-find . -type f -name "*.pyc" -exec rm -f "{}" \;
	-find . -type d -name "__pycache__" -exec rm -rf "{}" \;

cleanall: cleandist cleanegg cleantox cleanpy
