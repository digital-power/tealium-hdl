Tealium Hosted Data Layer - Read Me

How to start:

Step 1 : Make sure that are you able to use a Notebook Application:
  Option A:
  - Download Python and install Python & Pip: (https://www.python.org/downloads/ & https://www.liquidweb.com/kb/install-pip-windows)
  - !pip install jupyter notebook (in cmd/ terminal)
  - Install jupyter notebook

  Option B:
  - Install Anaconda Navigator and use jupyter notebook from there. (https://docs.anaconda.com/anaconda/navigator/)
  - Note: This costs more hard disk space then option A!

Step 2 : Download Tealium HDL files from this repository.
  - Download "notebook_use_tealium_hdl.ipynb"
  - Download "tealium_hdl_prod.py"
  - Place files in python directory
  
Step 3 : Use model and upload JSON files
  - Load "notebook_use_tealium_hdl.ipynb" in Notebook Application
  - Use model to upload files to Tealium HDL.
  - Make sure that your file names of the uploaded Tealium HDL files are matching a variable / HTML data on your web pages.
  
Step 4 : Use Tealium HDL output.
- Get example JS query from "get_hdl_data_and_merge_with_utag.js" in this repository.
- Add your code in Tealium iQ.
- Load a Tealium HDL file by hdl_lookup id and merge that data with the JS code in your utag_data object.
