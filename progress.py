import time
# t = 1260
# print("**************带时间的进度条**************")
# start = time.perf_counter()
# for i in range(t + 1):
#     finsh = "▓" * i
#     need_do = "-" * (t - i)
#     progress = (i / t) * 100
#     dur = time.perf_counter() - start
#     print("\r{:^3.0f}%[{}->{}]{:.2f}s".format(progress, finsh, need_do, dur), end="")
#     time.sleep(0.05)
import progressbar
p = progressbar.ProgressBar()
# # 假设需要执行100个任务，放到ProgressBar()中
for i in p(range(1260)):
    """
    代码
    """
    # 假设这代码部分需要0.05s
    time.sleep(0.05)