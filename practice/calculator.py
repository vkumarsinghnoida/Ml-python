#!/usr/bin/python3

import math 

moprt = ['+','-','/','*','%']
trigop = ['tan', 'sin', 'cos' , 'cot' , 'sec', 'cosec']
while True:
    oprt = input('What operation do you want to perform ? ')
    
    if oprt in moprt:
        num1 = input('Enter the first number ')
        num2 = input('Enter the second number ')
    elif oprt in trigop:
        theta = input('Enter theta ')

    out = None
    if oprt == '+':
        out = float(num1) + float(num2)
    elif oprt == '-':
        out = float(num1) - float(num2)
    elif oprt == '/':
        out = float(num1) / float(num2)
    elif oprt == '*':
        out = float(num1) * float(num2)
    elif oprt == '%':
        out = float(num1) % float(num2)
    elif oprt == 'tan':
        out = math.tan(float(theta))
    elif oprt == 'sin':
        out = math.sin(float(theta))
    elif oprt == 'cos':
        out = math.cos(float(theta))
    elif oprt == 'cosec':
        out = math.asin(float(theta))
    elif oprt == 'cot':
        out = math.atan(float(theta))
    elif oprt == 'sec':
        out = math.acos(float(theta))
   
    else:
        pass



    print(out)


