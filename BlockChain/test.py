#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:janvn
# datetime:18-8-5 上午8:45
# software:PyCharm

from hashlib import sha256

x=5
y=0

while sha256(f'{x*y}'.encode()).hexdigest()[-1] != "0":
    y += 1

print(f'The solution is y={y}')