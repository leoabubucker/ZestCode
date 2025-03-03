################################################################################
######################### User configurable parameters #########################
# VEX SDK version
SDK_VERSION:=V5_20240802_15_00_00 

# filename extensions
CEXTS:=c
ASMEXTS:=s S
CXXEXTS:=cpp c++ cc

# probably shouldn't modify these, but you may need them below
ROOT=.
FWDIR:=$(ROOT)/firmware
BINDIR=$(ROOT)/bin
SRCDIR=$(ROOT)/src
INCDIR=$(ROOT)/include
EXTRA_INCDIR=$(FWDIR)/libv5rt/sdk/vexv5/patched_include

# Directories to be excluded from all builds
EXCLUDE_SRCDIRS+=$(SRCDIR)/tests

C_STANDARD=gnu2x
CXX_STANDARD=gnu++23

WARNFLAGS+=-Wall -Wpedantic
EXTRA_CFLAGS=
EXTRA_CXXFLAGS=

.DEFAULT_GOAL=quick
USE_PACKAGE:=0

# object files to keep in libv5rt.a
RETAIN_OBJECTS:= v5_fstubs.c.obj v5_util.c.obj v5_apijump.c.obj v5_apiuser.c.obj v5_apigraphics.c.obj v5_apiversions.c.obj

# Set this to 1 to add additional rules to compile your project as a PROS library template
IS_LIBRARY:=1
LIBNAME:=libpros
VERSION=$(shell cat $(ROOT)/version)
# EXCLUDE_SRC_FROM_LIB= $(SRCDIR)/unpublishedfile.c
EXCLUDE_SRC_FROM_LIB+=$(EXCLUDE_SRCDIRS)
# this line excludes opcontrol.c and similar files
EXCLUDE_SRC_FROM_LIB+=$(foreach file, $(SRCDIR)/main,$(foreach cext,$(CEXTS),$(file).$(cext)) $(foreach cxxext,$(CXXEXTS),$(file).$(cxxext)))

# files that get distributed to every user (beyond your source archive) - add
# whatever files you want here. This line is configured to add all header files
# that are in the the include directory get exported
TEMPLATE_FILES=$(ROOT)/common.mk $(FWDIR)/v5.ld $(FWDIR)/v5-common.ld $(FWDIR)/v5-hot.ld
TEMPLATE_FILES+=$(FWDIR)/libc.a $(FWDIR)/libm.a
TEMPLATE_FILES+= $(INCDIR)/api.h $(INCDIR)/main.h $(INCDIR)/pros/*.* 
TEMPLATE_FILES+= $(SRCDIR)/main.cpp
TEMPLATE_FILES+= $(ROOT)/template-gitignore

PATCHED_SDK=$(FWDIR)/libv5rt/sdk/vexv5/libv5rt.patched.a

EXTRA_LIB_DEPS=$(INCDIR)/api.h $(PATCHED_SDK)

################################################################################
################################################################################
########## Nothing below this line should be edited by typical users ###########
-include ./common.mk

.PHONY: download_sdk patch_sdk_headers clean

download_sdk: scripts/get_libv5rt.py
	@echo "Downloading SDK"
	$(VV)python3 scripts/get_libv5rt.py $(SDK_VERSION)

patch_sdk_headers: download_sdk scripts/patch_headers.py
	@echo "Patching SDK headers"
	$(VV)python3 scripts/patch_headers.py

# Override clean, necessary to remove patched sdk on clean
clean::
	@echo "Cleaning SDK"
	@rm -rf $(EXTRA_INCDIR)
	@rm -rf $(FWDIR)/libv5rt

$(PATCHED_SDK): $(FWDIR)/libv5rt/sdk/vexv5/libv5rt.a
	$(call test_output_2,Stripping unwanted symbols from libv5rt.a ,$(STRIP) $^ @scripts/libv5rt-strip-options.txt -o $@, $(DONE_STRING))

CREATE_TEMPLATE_ARGS=--system "./**/*"
CREATE_TEMPLATE_ARGS+=--user "src/main.{cpp,c,cc}" --user "include/main.{hpp,h,hh}" --user "Makefile" --user ".gitignore"
CREATE_TEMPLATE_ARGS+=--target v5
CREATE_TEMPLATE_ARGS+=--output bin/monolith.bin --cold_output bin/cold.package.bin --hot_output bin/hot.package.bin --cold_addr 58720256 --hot_addr 125829120

template:: patch_sdk_headers clean-template library
	$(VV)mkdir -p $(TEMPLATE_DIR)
	@echo "Moving template files to $(TEMPLATE_DIR)"
	$Dif [ $(shell uname -s) == "Darwin" ]; then \
		rsync -R $(TEMPLATE_FILES) $(TEMPLATE_DIR); \
	else \
		cp --parents -r $(TEMPLATE_FILES) $(TEMPLATE_DIR); \
	fi
	$(VV)mkdir -p $(TEMPLATE_DIR)/firmware
	$Dcp $(LIBAR) $(TEMPLATE_DIR)/firmware
	$Dcp $(ROOT)/template-Makefile $(TEMPLATE_DIR)/Makefile
	$Dmv $(TEMPLATE_DIR)/template-gitignore $(TEMPLATE_DIR)/.gitignore
	@echo "Creating template"
	$Dpros c create-template $(TEMPLATE_DIR) kernel $(shell cat $(ROOT)/version) $(CREATE_TEMPLATE_ARGS)

libv5rt_EXTRACTION_DIR=$(BINDIR)/libv5rt
$(LIBAR): patch_sdk_headers $(call GETALLOBJ,$(EXCLUDE_SRC_FROM_LIB)) $(EXTRA_LIB_DEPS)
	$(VV)mkdir -p $(libv5rt_EXTRACTION_DIR)
	$(call test_output_2,Extracting libv5rt, cd $(libv5rt_EXTRACTION_DIR) && $(AR) x ../../$(PATCHED_SDK), $(DONE_STRING))

	$(eval libv5rt_OBJECTS := $(shell $(AR) t $(PATCHED_SDK)))
	$(eval libv5rt_OBJECTS := $(filter $(RETAIN_OBJECTS),$(libv5rt_OBJECTS)))
	
	-$Drm -f $@
	$(call test_output_2,Creating $@, $(AR) rcs $@ $(addprefix $(libv5rt_EXTRACTION_DIR)/, $(libv5rt_OBJECTS)) $(call GETALLOBJ,$(EXCLUDE_SRC_FROM_LIB)), $(DONE_STRING))


# @echo -n "Stripping non-public symbols "
# $(call test_output,$D$(OBJCOPY) -S -D -g --strip-unneeded --keep-symbols public_symbols.txt $@,$(DONE_STRING))