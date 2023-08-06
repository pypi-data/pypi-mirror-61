# A* Search Algorithm.
Anyone of you can use this library to do A* search
[Github Open Source](https://github.com/Mrrobi/astarSearch)

## Existing methods
* feed(self,heuristic_value_list,adjacency_matrix,node_name_dictionary)
* path() - Show the solved path with lowest cost


## using process

### 1st need to add the library
```python
pip install astarRobi
```
## 2nd You must need to implement neccessary list and dictionary like this ->
```python

node_dict = {
    0:"S",
    1:'A',
    2:'B',
    3:'C',
    4:'D'
}

adj_node = [ [-1,1,4,-1,-1],
 [-1,-1,2,5,12],
 [-1,-1,-1,2,-1],
 [-1,-1,-1,-1,3],
 [-1,-1,-1,-1,-1]]

h_val = [7,2,6,1,0] #here heuristic value 0 denotes the goal node.

```
### 3rd import aster and feed the data into it
```python
import astarRobi as astar

test = astar.feed(h_val,adj_node,node_dict) #feeding the algorithm neccessary data

test.path() #Showing the computed result :)

```

## N.B: part 2 is customizable you could feed any graph you want here a demo data is given. :) 


