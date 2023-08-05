This script updates module, class, and function docs in a `README.md` file,
based on their corresponding docstrings (so that documentation does not need to
be manually written in two places).

# Install

```shell script
pip3 install readme-md-docstrings
```

# Use

```python
import readme_md_docstrings
readme_md_docstrings.update('./README.md')
```

```shell script
python3 -m readme_md_docstrings ./README.md
```