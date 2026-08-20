# Jupyter Preprocessing Template

Generate a clean teaching notebook for the common image preprocessing exercise:

- flatten image tensors
- normalize pixel values
- implement sigmoid
- run basic shape and value checks

## Usage

```powershell
python .\src\make_preprocessing_notebook.py --output .\flatten_normalize_sigmoid.ipynb
```

Then execute it with Jupyter or nbconvert:

```powershell
jupyter nbconvert --to notebook --execute .\flatten_normalize_sigmoid.ipynb --output .\flatten_normalize_sigmoid_executed.ipynb
```

## Test

```powershell
python -m pytest tests -q
```

## License

MIT
