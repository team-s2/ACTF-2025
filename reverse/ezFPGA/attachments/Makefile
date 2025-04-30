DIR_BUILD		?= $(CURDIR)/build
DIR_SIM			?= $(CURDIR)/sim
DIR_SRC			?= $(CURDIR)/src

VERILATOR_TOP		:= Testbench
VERILATOR_SRCS		=  $(shell find $(DIR_SIM) -name "*.v" -o -name "*.sv") \
					   $(shell find $(DIR_SRC) -name "*.v" -o -name "*.sv")

VERILATOR_TFLAGS	:= -Wno-STMTDLY --timescale 1ns/10ps --trace --trace-depth 1
VERILATOR_FLAGS		:= --cc --exe  --main --timing\
						--Mdir $(DIR_BUILD) --top-module $(VERILATOR_TOP) -o $(VERILATOR_TOP)

.PHONY: verilate

verilate:$(VERILATOR_TOP)
	cd $(DIR_BUILD); ./$(VERILATOR_TOP)
	make clean

$(VERILATOR_TOP):$(VERILATOR_SRCS)
	mkdir -p $(DIR_BUILD)
	verilator $(VERILATOR_TFLAGS) $(VERILATOR_FLAGS) $(VERILATOR_SRCS)
	make -C $(DIR_BUILD) -f V$(VERILATOR_TOP).mk $(VERILATOR_TOP)

wave:
	gtkwave $(VERILATOR_TOP).vcd

clean:
	rm -rf $(DIR_BUILD)