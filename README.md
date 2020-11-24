# Tealium Hosted Data Layer UI - Read Me

This is a graphical interface in a jupyter notebook to interact with the Tealium Hosted Datalayer API. Features include uploading new datalayers, downloading existing datalayers & deleting datalayers.

See [this page](https://community.tealiumiq.com/t5/iQ-Tag-Management/About-Hosted-Data-Layer/ta-p/17572) for more general info about the Tealium Hosted Datalayer.

- [Tealium Hosted Data Layer UI - Read Me](#tealium-hosted-data-layer-ui---read-me)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Tealium API Key](#tealium-api-key)
  - [Examples](#examples)
  - [Anaconda](#anaconda)

---

## Requirements

- Python
- Pip
- Virtualenv
- Tealium API Key

---

## Installation

Create virtualenv folder:

```bash
python3 -m venv .venv
```

Activate virtual enviroment:

```bash
.\.venv\Scripts\activate
```

Install required packages:

```bash
pip install -r requirements.txt
```

---

## Usage

Start Jupyter notebook by running the below command, and run the first cell in the 'tealium_hdl_ui.ipynb' notebook

```bash
jupyter notebook
```

---

## Tealium API Key

Get your API key from Tealium iQ under Edit/View User Settings.
See this [tealium page](https://community.tealiumiq.com/t5/iQ-Tag-Management/Managing-and-Generating-API-Keys/ta-p/21205) for more info about generating these keys.

---

## Examples

- [Hosted datalayer file](./examples/datalayer-page-1.json)
- [Hosted datalayer usage in tealium](./examples/enrich_utag_data.js)

---

## Anaconda

It is possible to run the notebook in this repository through jupyter notebook provided by Anaconda. The only requirement missing in the Anaconda Base environment is `diff-match-patch`, so make sure to run below command in a jupyter notebook cell to make it work:

```python
!pip install diff-match-patch
```
