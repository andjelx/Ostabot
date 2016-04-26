#!/bin/bash

NEURALDIR="/home/bsod/neural-style/"
OUTDIR="/home/bsod/ostabot/out/"

if [ $# -eq 0 ]
  then
    echo "No arguments supplied"
    exit
fi

ARG1=$(readlink -f $1)
ARG2=$(readlink -f $2)
ARG4=${4:-out.png}
ARG3=${3:-1000}

#echo ${ARG1} ${ARG2} 

cd ${NEURALDIR}
th neural_style.lua -gpu -1 -style_image ${ARG1} -content_image ${ARG2} \
    -output_image ${OUTDIR}${ARG4} -model_file models/nin_imagenet_conv.caffemodel \
    -proto_file models/train_val.prototxt -num_iterations ${ARG3} -seed 123 \
    -content_layers relu0,relu3,relu7,relu12 -style_layers relu0,relu3,relu7,relu12 \
    -content_weight 10 -style_weight 1000 -image_size 256 -optimizer adam \
    -print_iter 10

rm ${ARG1}
rm ${ARG2}
