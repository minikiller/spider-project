# import re
# string1 = "go_baojia('A61FC431667610A6DC2BD4225A623D295C3671AD2D256322','3','GJ202207007476','','','')"
# string2 = "fafafasfasdfasdf"
# pattern = re.compile(r"'(\w+)'")
# str_re1 = pattern.findall(string1)
# # data=str_re1[0].split(",")
# print(str_re1)  # 提取到的数据是个列表
# print(str_re1[0])  # 提取单引号内的数据
# print(str_re1[1])  # 提取单引号内的数据
# print(str_re1[2])  # 提取单引号内的数据

# from multiprocessing import Process


# def print_func(continent='Asia'):
#     print('The name of continent is : ', continent)


# if __name__ == "__main__":  # confirms that the code is under main function
#     names = ['America', 'Europe', 'Africa']
#     procs = []
#     proc = Process(target=print_func)  # instantiating without any argument
#     procs.append(proc)
#     proc.start()

#     # instantiating process with arguments
#     for name in names:
#         # print(name)
#         proc = Process(target=print_func, args=(name,))
#         procs.append(proc)
#         proc.start()

#     # complete the processes
#     for proc in procs:
#         proc.join()

import sys
print(sys.argv[1])
