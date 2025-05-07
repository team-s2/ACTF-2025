## 前言

出题思路来自于2024年我们在Hexacon的议题，其中介绍了一个Virtio设备DMA重入导致的信息泄漏

## 程序分析

QEMU版本为8.2，并且加载了两个设备，一个virtio-blk和一个readflag。virtio-blk是原设备，未作改动。readflag是修改的edu设备，有两个功能：

1. 将flag通过mallocl-read-free的方式存留在已释放的内存堆中。
2. 有一个8字节寄存器的mmio读写功能。

通过分析可知是需要一个信息泄漏漏洞将内存中的flag读出来。将virtio-blk，info leak，DMA等关键词进行搜索可以发现CVE-2024-8612

![image](https://s1.imagehub.cc/images/2025/05/07/5eae8e161a80b205cb1a8f353531e531.png)

## 漏洞

CVE-2024-8612是一个DMA重入导致的信息泄漏漏洞，当virtio ring中的GPA为非直接访问的地址（如设备mmio地址）时会首先通过malloc一块内存（bounce buffer），然后在设备处理结束后，将该地址上的内容写会原先的GPA中，如果原先的GPA是设备mmio地址就会触发一次mmio write。然后由于bounce buffer中的内村在malloc之后为清空，就有可能将未初始化数据写入设备寄存器中，导致信息泄漏。

## 利用

1. 调用readflag将flag喷到内存中
2. 使用CVE-2024-8612将flag写到readflag设备的8字节寄存器中
3. 将readflag设备8字节寄存器的内容读出来

## 写在最后

这道题应该是ACTF2023 EasyVirtio的续题，EasyVirtio主要考察virtio的交互，因此EasyDMA未将virtio的交互纳入考察范围，但是通过调查发现不少选手卡在交互这里。同时恭喜也感谢天枢的选手拿到这道题的唯一解。

## 彩蛋

ACTF2026也许也会有需要virtio进行通信的题目，大家赶紧去学起来。
