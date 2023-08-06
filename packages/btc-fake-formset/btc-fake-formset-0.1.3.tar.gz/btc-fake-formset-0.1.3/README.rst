===================================================
BTC Fake Formset
===================================================

Fake Formset designed to display data of one form field (separated by characters) as a set of fields.
Adding / editing / deleting field's data parts also is possible.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "fake_formset" to your INSTALLED_APPS setting like this::

      INSTALLED_APPS = (
          ...
          'fake_formset',
      )

2. Add static files css/js::

    <link type="text/css" rel="stylesheet" href="{% static 'fake_formset/css/fake_formset.css' %}">
    <script src="{% static 'fake_formset/js/fake_formset.js' %}"></script>

3. Setup form field, wrap field into following containers::

    <div class="fake-formset-field-group-container js-fake-formset_field_group_container">
        <div class="fake-formset-field_wrapper js-fake_formset_field_wrapper">
            {{ form.my_field }}
        </div>
    </div>

4. In form setup field like this::

    'my_field': forms.TextInput(attrs={
        'data-fake-formset-id': 'my_field',      - unique identifier
        'data-fake-formset-max-fields': 3,       - fake field max number
        'data-fake-formset-split-symbol': '-/'   - split symbol for storing value in database (1-/2-/3-/), "," by default.
    })

5. Setup js-handler::

    const fake_formset = new FakeFormset();
    fake_formset.add_button_text = 'Add row';
    fake_formset.delete_button_text = 'Remove';
    fake_formset.initSignals();

    $(document).on('fake-formset:fake-field:added', function (event, fake_field, field, formset_id) {
        if (formset_id === 'my_field') {
            fake_field.mask('+7 (999) 999-99-99');  - here you can bind other handlers.
        }
    })
    $(document).on('fake-formset:fake-field:deleted', function (event, base_field) {
        // callback on field delete.
    })
    $(document).on('fake-formset:target-field:recalculated', function (event, field) {
        // callback after base hidden field recalculating.
    })

Example:

.. image:: https://user-images.githubusercontent.com/33987296/74908431-e3e09e00-53c6-11ea-8140-ead1018018d1.png

.. image:: https://user-images.githubusercontent.com/33987296/74908633-741ee300-53c7-11ea-9b3d-ca43d3018259.png
