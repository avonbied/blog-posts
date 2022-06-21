# Asynchronous Execution with Python (Pt. 2)

### Mixed Timing
call|start|finish|finish order
:---:|----:|----:|-----
1 | 0s | ~8s | 2 
2 | 0s |  8s | 1
3 | 8s | 10s | 3
