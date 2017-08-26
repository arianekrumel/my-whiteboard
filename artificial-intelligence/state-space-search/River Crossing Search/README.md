# river-crossing
## River Crossing
Ariane Krumel

### Allowed states (10)
- State 0:    0000
- State 1:    0001
- State 2:    0010
- State 3:    0100
- State 4:    0101
- State 5:    1010
- State 6:    1011
- State 7:    1101
- State 8:    1110
- State 9:    1111


### Transition Table
{0=[5], 1=[6, 7], 2=[5, 6, 8], 3=[7, 8], 4=[7, 9], 5=[0, 2], 6=[1, 2], 7=[1, 3, 4], 8=[2, 3]}


### Heuristic Function
h(n) = {0=4, 1=3, 2=3, 3=3, 4=2, 5=2, 6=1, 7=1, 8=1, 9=0}


### Breadth-first Search
step 0: f w s c | _ _ _ _ 
step 1: _ w _ c | f _ s _ 
step 2: f w _ c | _ _ s _ 
step 3: _ _ _ c | f w s _ 
step 4: f _ s c | _ w _ _ 
step 5: _ _ s _ | f w _ c 
step 6: f _ s _ | _ w _ c 
step 7: _ _ _ _ | f w s c 


### A Search
step 0: f w s c | _ _ _ _ 
step 1: _ w _ c | f _ s _ 
step 2: f w _ c | _ _ s _ 
step 3: _ _ _ c | f w s _ 
step 4: f _ s c | _ w _ _ 
step 5: _ _ s _ | f w _ c 
step 6: f _ s _ | _ w _ c 
step 7: _ _ _ _ | f w s c 
