#Installation :

` pip install FlowMagic`


# Usage :

```
import FlowMagic
```

### Denote 'main' function
Contains the code the app executes
```python
import FlowMagic

@FlowMagic.main
def process_invoice():
    #...magically processing invoice
    pass

# To call the main function
FlowMagic.start()
```
**Note**: Don't call the function directly. Use `Flowmagic.start()`

** To read base input path **
```
input_path = FlowMagic.input_path("key_name") 
```



** To read base output path **
```
output_path = FlowMagic.output_path("key_name")
```

** To get config JSON data **
```
data = FlowMagic.configJsonFile()
```

** To get system env values **
```
key = FlowMagic.getSystemValue(key)
```

** To get list of multiple input path **
```
multi_path = input_tree_path( json_obj , "/" , [] )
```


## Training
```python
import FlowMagic

@FlowMagic.train_main
def train_invoice_processor():
    #...magically training invoice processor
    pass

# To call the train function
FlowMagic.train()
```

### Training Helper Functions
**Only available while training** 


**To get training data directories**
```python
import FlowMagic

train_dirs: List[pathlib.Path] = FlowMagic.get_train_dirs()
```


**To get testing data directories**
```python
import FlowMagic

train_dirs: List[pathlib.Path] = FlowMagic.get_test_dirs()
```

**To write metrics**
```python
import FlowMagic

FlowMagic.write_metrics({'accuracy': 0.9, 'loss': 0.003})
```

**To get path of previous model**
```python
import FlowMagic

previous_model_path: pathlib.Path = FlowMagic.get_previous_model()
```

**To get newly trained model output path**

Write the newly generated h5 file here
```python
import FlowMagic

dest: pathlib.Path = FlowMagic.get_model_destination()
```
