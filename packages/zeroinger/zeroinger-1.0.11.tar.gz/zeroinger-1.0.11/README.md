# zeroinger
提升编码效率，有效延长程序猿寿命的小工具集
## 目录
* 安装
  * 依赖条件
  * pip3安装
* 使用方法
    * 时间相关
    * Excel/CSV读写
    * 配置文件读取
    * 文本文件读写
* 更新日志
## 安装
### 依赖条件
* python>=3.6.0
* logzero==1.5.0
### pip3安装
```
pip3 install --upgrade zeroinger
```
## 使用方法
### 时间相关
#### StopWatch
```
from zeroinger.time.stopwatch import StopWatch
import time
# 创建实例
timer = StopWatch.create_instance()
time.sleep(1)
# 获取从开始到现在的耗时
print('当前耗时',timer.duration())
# 添加一个计时快照
cost = timer.add_snapshot()
print('快照1时间点', cost)
time.sleep(1)
cost = timer.add_snapshot()
print('快照2时间点', cost)
snapshot_list = timer.list_snapshot()
print('所有快照时间点', snapshot_list)
# 重置计时器
timer.reset()
#--------------------------------
当前耗时 1004
快照1时间点 1005
快照2时间点 2006
所有快照时间点 [1005, 2006]
```
### Excel/CSV相关
#### XLSX
##### 读取excel
```
from zeroinger.excel.xlsx import XLSX
test_read_file_path = os.path.join(os.path.dirname(__file__), 'read_test_file.xlsx')
data = XLSX.read_dict_sheet(test_read_file_path, 0)
print(data)
#--------------
[{'列1': 1, '列2': 4, '列3': 7}, {'列1': 2, '列2': 5, '列3': 8}, {'列1': 3, '列2': 6, '列3': 9}]
```
##### 写入excel
```
from zeroinger.excel.xlsx import XLSX
golden = [{'列1': 1, '列2': 4, '列3': 7}, {'列1': 2, '列2': 5, '列3': 8}, {'列1': 3, '列2': 6, '列3': 9}]
test_write_file_path = os.path.join(os.path.dirname(__file__), 'write_test_file.xlsx')
XLSX.write_dict_sheet(test_write_file_path, golden)
```

### 压缩文件读写
## 更新日志
- 2020/01/06 新增压缩文件读取方法