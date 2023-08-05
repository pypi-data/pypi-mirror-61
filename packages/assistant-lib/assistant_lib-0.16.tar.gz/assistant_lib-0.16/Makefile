
MKFILE_PATH := $(abspath $(lastword $(MAKEFILE_LIST)))
MKFILE_DIR := $(dir $(MKFILE_PATH))

BIN_DIR=$(MKFILE_DIR)/dist

# Clean, test and build
all: clean test build

### Make entries

# Help
help:
	@awk '/^#/{c=substr($$0,3);next}c&&/^[[:alpha:]][[:alnum:]_-]+:/{print substr($$1,1,index($$1,":")),c}1{c=0}' $(MAKEFILE_LIST) | column -s: -t

# Build
build: 
	@echo "############################################"
	@echo "# Build"
	@echo "############################################"

	python3 -m pip install --user --upgrade setuptools wheel
	python3 setup.py sdist bdist_wheel

	@echo "End with success :)"

# Execute the tests
test: 
	@echo "############################################"
	@echo "# Test"
	@echo "############################################"
	
	#tox
	@echo "No tests defined for now"


# Clean all builded files
clean: 
	@echo "############################################"
	@echo "# Clean"
	@echo "############################################"

	rm -Rf $(MKFILE_DIR)/dist
	rm -Rf $(MKFILE_DIR)/build
	rm -Rf $(MKFILE_DIR)/assistant_lib.egg-info
	rm -Rf $(MKFILE_DIR)/.eggs

