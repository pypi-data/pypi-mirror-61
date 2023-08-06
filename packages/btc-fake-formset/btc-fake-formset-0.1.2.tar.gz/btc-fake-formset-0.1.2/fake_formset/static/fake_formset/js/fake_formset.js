/* Fake Formset JS handler
*
* Usage: wrap field into following containers:
*
* <div class="fake-formset-field-group-container js-fake-formset_field_group_container">
*    <div class="fake-formset-field_wrapper js-fake_formset_field_wrapper">
*        {{ form.my_field }}
*   </div>
* </div>
*
* In form setup field like this:
*
* 'my_field': forms.TextInput(attrs={
*    'data-fake-formset-id': 'my_field',      - unique identifier
*    'data-fake-formset-max-fields': 3,       - fake field max number
*    'data-fake-formset-split-symbol': '-/'   - split symbol for storing value in database (1-/2-/3-/), "," by default.
*  }),
*
* In scripts:
*
* const fake_formset = new FakeFormset();
* fake_formset.add_button_text = 'Добавить';
* fake_formset.delete_button_text = 'Удалить';
* fake_formset.initSignals();
*
* $(document).on('fake-formset:fake-field:added', function (event, fake_field, field, formset_id) {
*     if (formset_id === 'my_field') {
*         fake_field.mask('+7 (999) 999-99-99');  - here you can bind other handlers.
*     }
* })
* $(document).on('fake-formset:fake-field:deleted', function (event, base_field) {
*     // callback on field delete.
* })
* $(document).on('fake-formset:target-field:recalculated', function (event, field) {
*     // callback after base hidden field recalculating.
* })
* */


let fake_formset_handler = null;
FakeFormset = function () {

    const self = this;

    fake_formset_handler = self;

    this.target_fields_selector = 'data-fake-formset-id';
    this.split_symbol_attr_name = 'data-fake-formset-split-symbol';
    this.fields_max_num_attr_name = 'data-fake-formset-max-fields';
    this.field_group_container_class = 'js-fake-formset_field_group_container';
    this.field_wrapper_class = 'js-fake_formset_field_wrapper';
    this.add_button_text = 'Add';
    this.delete_button_text = 'Delete';

    this.field_base_type_attr_name = 'data-fake-formset-field-base-type';
    this.delete_button_attr_name = 'data-fake-formset-delete-field';
    this.add_button_attr_name = 'data-fake-formset-add-field';
    this.fake_field_postfix = '-fake';
    this.fake_field_bound_attr_name = 'data-fake-formset-bound-field';

    this.add_button_html = '<button type="button">' + self.add_button_text + '</button>';
    this.delete_button_html = '<button type="button">' + self.delete_button_text + '</button>';

    this.initFormsets = function () {
        const fields = $('[' + self.target_fields_selector + ']');

        $.each(fields, function () {
            const field = $(this);

            self.cloneFieldByValue(field);
            self.controlAddButton(field);
        });
    };

    this.addDeleteButton = function (container, field_name) {
        const button = $(self.delete_button_html).attr(self.delete_button_attr_name, field_name);

        button.html(self.delete_button_text);
        container.append(button);
    };

    this.addButton = function (field) {
        const container = field.closest('.' + self.field_group_container_class);
        const button = $(self.add_button_html);

        button.html(self.add_button_text);
        button.attr(self.add_button_attr_name, field.attr('name'));
        container.append(button);
    };

    this.cloneFieldByValue = function (field) {
        const split_symbol = self.getSeparator(field);
        const splitted_val = field.val().split(split_symbol);

        $.each(splitted_val, function (index, val) {
            self.cloneField(field, val, index, index !== 0);
        });

        self.hideField(field);
    };

    this.getSeparator = function (field) {
        return field.attr(self.split_symbol_attr_name) || ','
    };

    this.cloneField = function (field, field_val, additional_postfix='', can_delete=true) {
        const field_name = field.attr('name');
        const container_for_clone = field.closest('.' + self.field_wrapper_class);
        const cloned_container = $(container_for_clone.clone());
        const fake_field = cloned_container.find('[name=' + field_name + ']');
        const fake_field_name = field_name + self.fake_field_postfix + '-' + additional_postfix;
        const formset_id = field.attr(self.target_fields_selector);

        fake_field.attr('name', fake_field_name);
        fake_field.attr(self.fake_field_bound_attr_name, field_name);
        fake_field.attr('value', field_val);
        fake_field.removeAttr(self.target_fields_selector);
        fake_field.removeAttr('id');
        fake_field.val(field_val);

        if (can_delete) {
            self.addDeleteButton(cloned_container, fake_field_name);
        }
        container_for_clone.parent().append(cloned_container);

        $(document).trigger('fake-formset:fake-field:added', [fake_field, field, formset_id]);

        return fake_field;
    };

    this.deleteFakeField = function (fake_field) {
        const base_field = $('[name=' + fake_field.attr(self.fake_field_bound_attr_name) + ']');

        fake_field.closest('.' + self.field_wrapper_class).remove();
        self.calcValue(base_field);

        $(document).trigger('fake-formset:fake-field:deleted', [base_field]);
    };

    this.hideField = function (field) {
        field.attr(self.field_base_type_attr_name, field.attr('type'));
        field.attr('type', 'hidden');
    };

    this.showField = function (field) {
        if (field.attr('type') === 'hidden') {
            field.attr('type', field.attr(self.field_base_type_attr_name));
        }
    };

    this.controlAddButton = function (base_field) {
        const base_field_name = base_field.attr('name');
        const max_fields_count = parseInt(base_field.attr(self.fields_max_num_attr_name));

        if (max_fields_count) {
            const fake_fields_count = $('[' + self.fake_field_bound_attr_name + '=' + base_field_name + ']').length;
            const button = $('button[' + self.add_button_attr_name + '=' + base_field_name + ']');

            if (max_fields_count <= fake_fields_count && button.length) {
                button.remove()
            } else if (max_fields_count > fake_fields_count && !button.length) {
                self.addButton(base_field);
            }
        }
    };

    this.calcValue = function (field) {
        const fake_fields = $('[' + self.fake_field_bound_attr_name + '=' + field.attr('name') + ']');
        let val_array = [];

        $.each(fake_fields, function () {
            const val = $(this).val();
            if (val) {
                val_array.push(val);
            }
        });

        field.val(val_array.join(self.getSeparator(field)));

        $(document).trigger('fake-formset:target-field:recalculated', [field]);
    };

    this.moveButtonToEnd = function (button) {
        $(button.closest('.' + self.field_group_container_class)).append(button.detach());
    };

    this.initSignals = function () {
        $(document).on('change', '[' + self.fake_field_bound_attr_name + ']', function (event) {
            const fake_field = $(this);
            const target_field_name = fake_field.attr(self.fake_field_bound_attr_name);
            const target_field = $('[name=' + target_field_name + ']');

            self.calcValue(target_field);
        });
        $(document).on('click', '[' + self.add_button_attr_name + ']', function (event) {
            const button = $(this);
            const target_field_name = button.attr(self.add_button_attr_name);
            const target_field = $('[name=' + target_field_name + ']');
            const fake_fields_count = $('[' + self.fake_field_bound_attr_name + '=' + target_field_name + ']').length;
            const fake_field = self.cloneField(target_field, '', fake_fields_count);

            self.showField(fake_field);
            self.moveButtonToEnd(button);
            self.controlAddButton(target_field);

        });
        $(document).on('click', '[' + self.delete_button_attr_name + ']', function (event) {
            const button = $(this);
            const fake_field_name = button.attr(self.delete_button_attr_name);
            const fake_field = $('[name=' + fake_field_name + ']');
            const base_field = $('[name=' + fake_field.attr(self.fake_field_bound_attr_name) + ']');

            self.deleteFakeField(fake_field);
            self.controlAddButton(base_field);
        });
    }

};