# sqlstate
Super simple state manager for Python3

## Usage
### Define state
```python
import sqlstate
state = sqlstate.State('dog.tmp') # This creates a file called dog.tmp where your state will be saved.
```
### Store
```python
dogs = [{'name': 'Michael Clayton', 'breed': 'Labrador'}]
state.store(key='dogs', payload=dogs)
```
### Get
```python
dogs = state.get(key='dogs')
```
# sqlstate
