# Yosys Nangate45 gate synthesis (TCL script, run with -c)
set design $env(YOSYS_DESIGN)
set rtl_dir "../rtl/${design}"
set lib "/usr/local/share/yosys/NangateOpenCellLibrary_typical.lib"

# Read all RTL files
foreach f [glob -nocomplain ${rtl_dir}/*.v] {
    yosys read_verilog -I${rtl_dir} $f
}

# Map design name to top module
if {[string equal $design "rs232"]} {
    set top "uart"
} else {
    set top $design
}

yosys hierarchy -check -top $top
yosys proc; yosys opt; yosys fsm; yosys opt; yosys memory; yosys opt
yosys techmap; yosys opt
yosys dfflibmap -liberty $lib
yosys abc -liberty $lib
yosys clean -purge
yosys write_verilog ../netlist/gate/${design}_gate.v
