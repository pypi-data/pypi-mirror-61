Inscribe.ai
===========

-  API wrapper for `Inscribe`_

For more information, please read our `documentation`_.

Installation
------------

-  ``pip install inscribe``

Usage
-----

.. code:: python

   import inscribe
   import json

   # API Authentication
   api = inscribe.Client(api_key="YOUR_API_KEY", user_id="YOUR_USER_ID")

   # Create customer folder
   customer = api.create_customer(customer_name="new")
   customer_id = customer['data']['id']

   # Upload document
   doc_obj = open("YOUR_FILE.pdf", "rb")
   document = api.upload_document(customer_id=customer_id, document=doc_obj)
   document_id = document['result_urls'][0]['document_id']

   # Check document
   result = api.retrieve_document_results(customer_id=customer_id, document_id=document_id)
   print(json.dumps(result, indent=2))

.. _Inscribe: https://inscribe.ai
.. _documentation: https://docs.inscribe.ai/#introduction