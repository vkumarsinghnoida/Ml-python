#!/usr/bin/python3

import math 

moprt = ['+','-','/','*','%', '^']
trigop = ['tan', 'sin', 'cos' , 'cot' , 'sec', 'cosec']
while True:
    oprt = input('What operation do you want to perform ? ')
    
    if oprt in moprt:
        num1 = input('Enter the first number ')
        num2 = input('Enter the second number ')
    elif oprt in trigop:
        theta = input('Enter theta ')

    out = 'Not possible'

    if oprt == '+':
        out = float(num1) + float(num2)
    elif oprt == '-':
        out = float(num1) - float(num2)
    elif oprt == '/':
        try:
            out = float(num1) / float(num2)
        except:
            pass
    elif oprt == '^':
        try:
            out = float(num1) ** float(num2)
        except:
            pass
    elif oprt == '*':
        out = float(num1) * float(num2)
    elif oprt == '%':
        out = float(num1) % float(num2)
    elif oprt == 'tan':
        try:
            out = math.tan(float(theta))
        except:
            pass
    elif oprt == 'sin':
        try:
            out = math.sin(float(theta))
        except:
            pass
    elif oprt == 'cos':
        try:
            out = math.cos(float(theta))
        except:
            pass
    elif oprt == 'cosec':
        try:
            out = math.asin(float(theta))
        except:
            pass
    elif oprt == 'cot':
        try:
            out = math.atan(float(theta))
        except:
            pass
    elif oprt == 'sec':
        try:
            out = math.acos(float(theta))
        except:
            pass
    elif oprt == 'exit':
        break
    else:
        pass



    print(out)


