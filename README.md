# Exposure

## configuring

file input and ouptut is controlled through a yaml file by default this loaded from the 

```yaml

# this can be file or directory containing files
input: 'testing/input.jpg'

# likewise this can be a file or directory,
# the type is determined by the input type
output: 'testing/tmp/output.jpg'

styles:
  frame: 
    # hex color code
    background: '#000000'
    width: 1000
    height: 1000
  image:
    width: 1000
    top: 0
    left: 0


```