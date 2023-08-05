# cxnetwork
Experimental library to process and analyze complex networks

## Requirements
- C11 compatible compiler (GCC, CLANG)

## Compiling
run `pip install cxnetwork` on the project directory.

## Usage
```python
import cxnetwork as cx

cx.randomSeedDev();

edges =  [(0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(7,8),(8,9),(9,10),(10,0)]
edges += [(0,2),(1,3),(2,4),(3,5),(4,6),(5,7),(6,8),(7,9),(8,10),(9,0),(10,1)]

rewiredEdges = cx.rewire(edges,11,0.5);

print(rewiredEdges);

```