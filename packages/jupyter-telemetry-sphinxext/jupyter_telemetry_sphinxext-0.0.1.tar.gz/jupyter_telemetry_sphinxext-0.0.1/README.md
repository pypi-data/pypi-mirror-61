# Jupyter Telemetry Sphinx Extension

*Sphinx extension for auto-generating Jupyter Telemetry schema documentation.*

To activate this extension, add `jupyter_telemetry_sphinxext` to your ``conf.py`` file
and set the following configuration values:

```python
# config.py file.
# Add jupyter_telemetry_sphinxext to the extensions list.
extensions = [
    'jupyter_telemetry_sphinxext',
    ...
]

# Jupyter telemetry configuration values.
jupyter_telemetry_schema_source = "path/to/schemas/source/directory"   # Path is relative to conf.py
jupyter_telemetry_schema_output = "path/to/output/directory"           # Path is relative to conf.py
jupyter_telemetry_index_title = "Example Event Schemas"                # Title of the index page that lists all found schemas.
```