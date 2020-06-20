#!/bin/bash

exec 1>/output/stdout.log 2>/output/stderr.log

# TODO: Create MODEL variable
FACEDETECTIONMODEL=$1
LANDMARKDETECTIONMODEL=$2
HEADPOSEESTIMATIONMODEL=$3
GAZEESTIMATIONMODEL=$4
DEVICE=$5
VIDEO=$6
OUTPUT=$7
FLAGS=$8
PROBABILITY=$9

mkdir -p $7

if echo "$DEVICE" | grep -q "FPGA"; then # if device passed in is FPGA, load bitstream to program FPGA
    #Environment variables and compilation for edge compute nodes with FPGAs
    export AOCL_BOARD_PACKAGE_ROOT=/opt/intel/openvino/bitstreams/a10_vision_design_sg2_bitstreams/BSP/a10_1150_sg2

    source /opt/altera/aocl-pro-rte/aclrte-linux64/init_opencl.sh
    aocl program acl0 /opt/intel/openvino/bitstreams/a10_vision_design_sg2_bitstreams/2020-2_PL2_FP16_MobileNet_Clamp.aocx

    export CL_CONTEXT_COMPILER_MODE_INTELFPGA=3
fi

python main.py -fd ${FACEDETECTIONMODEL} \
              -lr ${LANDMARKDETECTIONMODEL} \
              -hp ${HEADPOSEESTIMATIONMODEL} \
              -ge ${GAZEESTIMATIONMODEL} \
              -d ${DEVICE} \
              -i ${VIDEO} \
              -o ${OUTPUT} \
              -flags ${FLAGS} \
              -prob ${PROBABILITY} \

cd /output

tar zcvf output.tgz *