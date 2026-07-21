#!/bin/bash
# Yosys 综合运行脚本
# 用法: ./run_yosys.sh <design_name> [generic|gate]
# 示例: ./run_yosys.sh rs232 gate

set -e
DESIGN=${1:?"Usage: $0 <design_name> [generic|gate]"}
MODE=${2:-gate}

RTL_DIR="../rtl/${DESIGN}"

if [ ! -d "$RTL_DIR" ]; then
    echo "Error: RTL directory not found: $RTL_DIR"
    exit 1
fi

V_COUNT=$(ls "$RTL_DIR"/*.v 2>/dev/null | wc -l)
echo "Design:  ${DESIGN}"
echo "RTL dir: ${RTL_DIR} (${V_COUNT} .v files)"

case $MODE in
    generic)
        echo "Running generic synthesis..."
        YOSYS_DESIGN="$DESIGN" yosys -Q -T -c scripts/synth_generic.tcl
        echo "Output: ../netlist/generic/${DESIGN}_generic.v"
        ;;
    gate)
        echo "Running Nangate45 gate synthesis..."
        YOSYS_DESIGN="$DESIGN" yosys -Q -T -c scripts/synth_nangate45.tcl
        echo "Output: ../netlist/gate/${DESIGN}_gate.v"
        ;;
    *)
        echo "Unknown mode: $MODE (use 'generic' or 'gate')"
        exit 1
        ;;
esac

echo "Done."
