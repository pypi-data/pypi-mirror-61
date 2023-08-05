#Fourier Transform Textural Ordination in Python

Freely adapted from https://github.com/CaussesCevennes/FOTO.py

Usage

```python
from foto2.foto import Foto

if __name__ == '__main__': 

  foto = Foto("path/to/your/image", method='BLOCK')
  foto.run(window_size=11, progress_bar=True)
```
