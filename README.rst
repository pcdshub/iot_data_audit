===============================
iot_data_audit
===============================

.. image:: https://github.com/pcdshub/iot_data_audit/actions/workflows/standard.yml/badge.svg
        :target: https://github.com/pcdshub/iot_data_audit/actions/workflows/standard.yml

.. image:: https://img.shields.io/pypi/v/iot_data_audit.svg
        :target: https://pypi.python.org/pypi/iot_data_audit


`Documentation <https://pcdshub.github.io/iot_data_audit/>`_

This application generates a report for the quarterly DoE IoT Data Audit. It does this with the following steps:

1. Gets a data dump from netconfig
2. Takes filters from google sheets and applies them to the dataset.
3. Pings hostnames in the filtered dataset and generates a list of active/alive devices.
4. Takes the netconfig dataset containing all filtered and active/alive devices and merges the relevant data from google sheets to generate an IoT Asset Inventory spreadsheet.

Instructions
------------
This program requires two files. The files contain metadata for all active IoT devices (so I omitted them from this public repo).

1. A csv download of the CIO FISMA Metrics Data Call Template. A copy of this file is located in my folder at ``~/git/iot_data_audit/iot_data_audit/google_sheets.csv``. Be sure to put this file in ``/iot_data_audit/iot_data_audit/``.
2. The DoE Asset Inventory Template renamed as ``iot_template.xlsx``. A copy of this file is located at ``~/git/iot_data_audit/iot_data_audit/iot_data_audit.xlsx``. Be sure to put this file in ``/iot_data_audit/iot_data_audit/``.

To run this program navigate to the top-level directory ``iot_data_audit`` and run ``./iot_data_audit.sh``. This app takes about 3-4 minutes to run and should ask for the user's password only once.

A generated DoE report is output to the top-level directory as an Excel file called ``iot_asset_inventory.xlsx``.

Requirements
------------

* Python 3.9+

Installation
------------

::

  $ pip install .

Running the Tests
-----------------
::

  $ pytest -v
