#!/bin/bash

# 循环运行Python脚本十次
for ((i=1; i<=10; i++))
do
    # 传递命令行参数给Python脚本
    python3 ../ClientTest.py ./test01 &
done

wait