# 📦 Installation

RubiFlow is distributed through PyPI and can be installed in any Python 3.9+ environment.

---

## 1. Installing from PyPI (Recommended)

```bash
pip install rubiflow
```

To upgrade an existing installation to the latest release:

```bash
pip install --upgrade rubiflow
```

---

## 2. Installing from Source (GitHub)

If you wish to use the cutting-edge version directly from the repository:

```bash
git clone https://github.com/iliasync/rubiflow.git
cd rubiflow
pip install -e .
```

---

## 3. Verifying Installation

Verify that RubiFlow is correctly installed and view its version:

```python
import rubiflow

print("RubiFlow version:", rubiflow.__version__)
```

---

## 4. Dependencies

RubiFlow requires the following high-performance packages:
- **`aiohttp` (>= 3.9.0):** Asynchronous HTTP client with connection pooling.
- **`cryptography` (>= 41.0.0):** C-accelerated cryptographic engine for AES-256 and RSA-SHA256 signatures.

These are automatically resolved and installed by `pip`.
