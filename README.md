# SlowDelete
Slow to delete larger or many files Apply to background processing



``` python
a = SlowDelete(u'tests\\big.file')
a.set_speed(1024*1024*5) # Delete Speed:5.0MB/s
a.start()

output:
2.0%, Delete Speed:5.0MB/s 
5.0%, Delete Speed:5.0MB/s 
7.0%, Delete Speed:5.0MB/s 
10.0%, Delete Speed:5.0MB/s 
12.0%, Delete Speed:5.0MB/s 
15.0%, Delete Speed:5.0MB/s 

```

``` python
b = SlowDeleteThread(u'tests\\big.file')
b.set_speed(1024*1024*0.1) # Speed:1024.0KB/s
b.start()
b.join()

output:
0.0%, Delete Speed:102.4KB/s 
0.0%, Delete Speed:102.4KB/s 
0.0%, Delete Speed:102.4KB/s 
0.0%, Delete Speed:102.4KB/s 
```