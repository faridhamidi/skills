# Retry recovery fixture

`ProfileStore.replace_many()` represents a storage boundary that can fail after a
partial write. `update_profile()` may retry that operation.

The required behavior is:

- A successful update changes every requested field.
- A transient failure may be retried and must eventually produce the complete update.
- If every attempt fails, the original profile must remain completely unchanged.

Run the public tests with:

```bash
python3 -m unittest discover -s tests -v
```
