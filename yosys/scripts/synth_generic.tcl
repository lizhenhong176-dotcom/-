# Yosys generic synthesis — no tech mapping (TCL script, run with -c)
set design $env(YOSYS_DESIGN)
set rtl_dir "../rtl/${design}"

foreach f [glob -nocomplain ${rtl_dir}/*.v] {
    yosys read_verilog -I${rtl_dir} $f
}

if {[string equal $design "rs232"]} {
    set top "uart"
} else {
    set top $design
}

yosys hierarchy -check -top $top
yosys proc; yosys opt; yosys fsm; yosys opt; yosys memory; yosys opt
yosys write_verilog ../netlist/generic/${design}_generic.v
