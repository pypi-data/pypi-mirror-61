===================================================
BTC Weasy PDF
===================================================

View mixin and template filters for PDF creation from the HTML-template.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "weasy_pdf" to your INSTALLED_APPS setting like this::

      INSTALLED_APPS = (
          ...
          'weasy_pdf',
      )

2. Help functions: `safety_get_attribute()`, `safety_parse_dict()`, `format_date()` (see utils.py)

3. Create data-object. When using the `safety_get_attribute()` function do not forget to join the related tables
   (prefetch_related, select_related)::

    class PDFDataObject:

        def __init__(self, data_obj: MyModel):
            get = safety_get_attribute
            self.data_obj = data_obj

            self.first_name = get(data_obj, 'first_name')
            ...

4. Prepare PDF template. Use built-in template filters: `times`, `parse_dict`::

    <!doctype html>
    <html lang="en">
        <head>
            <meta charset="utf-8">

            {% load static %}
            {% load weasy_pdf %}

            <link rel="stylesheet" href="{% static '/styles/pdf.css' %}">

            <title>Title</title>
            <meta name="description" content="Description">
            <meta name="author" content="Author">

        </head>
        <body>
            <span>{{ data_object.first_name }}</span>
            ...
        </body>
    </html>

    <!-- Filters usage:

    {% for i in 8|times %}
        <td colspan="2"></td>
    {% endfor %}

    <td colspan="5">{{ data_object|parse_dict:'0__NAME' }}</td>
     -->

5. Prepare view::

    class PDFView(WeasyPDFViewMixin):

        template_name = 'pdf.html'
        file_name = 'my_pdf.pdf'

        def get_object(self) -> Any:
            passport = get_object_or_404(Passport, pk=self.kwargs.get('pk'))
            return PDFDataObject(passport)

Example

.. image:: https://user-images.githubusercontent.com/33987296/74111631-3e981f80-4ba7-11ea-874f-9509ba101c2d.png