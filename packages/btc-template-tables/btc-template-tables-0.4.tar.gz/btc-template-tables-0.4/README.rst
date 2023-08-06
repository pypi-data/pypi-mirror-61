===================================================
BTC Template Tables
===================================================

Some classes for for describing tables with an auto-generated template.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "template_tables" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
          ...
          'template_tables',
      )

2. Create table class::

    class MyTable(BaseTemplateTable):

        css_classes = ['template-tables', 'mdl-data-table', 'mdl-js-data-table']
        empty_table_text = 'Нет данных'

        def get_header_rows(self) -> List[TableRowType]:
            [TR([
                TH(''),
                MDLNonNumericTH('Уч.', ordering='section'),
                MDLNonNumericTH('Документ', ordering='invoices__unique_num'),
                MDLNonNumericTH('КПТП', ordering='process_map__unique_number'),
                MDLNonNumericTH('Артикул ДСЕ', ordering='invoices__product__vendor_code'),
                MDLNonNumericTH('Наименование', ordering='invoices__product__name'),
                TH('Кол-во (шт.)', ordering='invoices__product__count'),
                TH('Вес (кг)', ordering='invoices__product__weight'),
                MDLNonNumericTH('Место', ordering='invoices__product__storage__name'),
            ])]

        def get_body_row(self, index: int, data_item: Any) -> TableRowType:
            invoice = data_item.get_invoice()
            product = safety_get_attribute(invoice, 'product')
            invoice_unique_number = f'{invoice.get_document_type_display()}-{invoice.unique_num}' if invoice else None

            transition_btn = ARSimpleLink(
                icon=ARMaterialIcon('chevron_right'),
                css_classes=['table-transition-btn'],
                html_params=dict(href=reverse('dispatcher:task_details:selected-products', kwargs=dict(pk=data_item.pk)))
            )

            return TR([
                MDLNonNumericTD(transition_btn),
                MDLNonNumericTD(data_item.section),
                MDLNonNumericTD(invoice_unique_number),
                MDLNonNumericTD(safety_get_attribute(data_item, 'process_map')),
                MDLNonNumericTD(safety_get_attribute(product, 'vendor_code')),
                MDLNonNumericTD(safety_get_attribute(product, 'name')),
                TD(safety_get_attribute(product, 'count')),
                TD(safety_get_attribute(product, 'weight')),
                MDLNonNumericTD(safety_get_attribute(product, 'storage__name')),
            ])

3. Define view - `ListView` or `FilterView`::

    class MyTableView(TemplateTableViewMixin, FilterView):

        model = MyModel
        filterset_class = MyTableFilter
        table_class = MyTable
        template_name = 'tables/template_table_base.html'

        def get_queryset(self):
            return super().get_queryset().get_pretty_qs()

    # For ordering and searching, the django-filter package is used.
    # Order filter:

    _base_task_table_searching_fields = [
        'section',
        'invoices__unique_num',
        'process_map__unique_number',
        'invoices__product__vendor_code',
        'invoices__product__name',
        'invoices__product__count',
        'invoices__product__weight',
        'invoices__product__storage__name'
    ]

    class MyTableFilter(FilterSet):

        ordering = OrderingFilter(
            fields=tuple(
                (field_name, field_name) for field_name in _base_task_table_searching_fields
            )
        )

4. In template::

    <!--
    tables/template_table_base.html

    That example uses btc-flex-forms for filters rendering
    -->

    <div>
        <div>{{ filter.form.as_flex }}</div>
        <div>{{ table.render }}</div>
        <div>{{ pagination.render }}</div>
    </div>

    <!-- Note: To transform table to ajax-table just you simple js-handler for link click events -->

Example:

.. image:: https://user-images.githubusercontent.com/33987296/74619321-2cd5ef80-5146-11ea-8e7b-28ddf929541d.png