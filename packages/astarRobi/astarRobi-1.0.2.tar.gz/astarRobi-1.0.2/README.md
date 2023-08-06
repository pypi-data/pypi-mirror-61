# A* Search Algorithm.
Anyone of you can use this library to do A* search
[Github Open Source](https://github.com/Mrrobi/astarSearch)

## using process
### First need to add the library

```python
pip install astarRobi
```

### Then you need to import the A* Search specific queue from the library
```python
import asterRobi as Q

minQ = Q.PriorityQueue() #Creating an object of PriorityQueue class of the library
minQ.insert(yournodeObj) #inserting your node object into the Queue
minQ.delete() # popping your node object from the priority queue

```

##Existing methods
* insert() - insert node object.
* delete() - pop min element and return it.
* isEmpty() - return true if queue is empty.
* size() - it returns length of the queue.

## N.B: You must need to declare a variable name "total_cost" the priority is prioritized based on this

