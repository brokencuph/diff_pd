#!/bin/bash
docker run -it \
    --gpus all \
    -v $PWD:/diff_pd \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -e DISPLAY diff_pd