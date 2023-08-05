===================================================
Django Flex Forms
===================================================

Some form mixins, styles and scripts for fast form development.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "flex_forms" to your INSTALLED_APPS setting like this::

      INSTALLED_APPS = (
          ...
          'flex_forms',
      )

2. Add static files css::

    <link type="text/css" rel="stylesheet" href="{% static 'flex_forms/css/default.css' %}">

3. Classes for usage: `StaticFlexForm` designed for rendering only static fieldsets::

    class CustomStaticFieldset(StaticFieldset):
        ...
        field_1 = StaticFlexField(
            data='',
            label='Name',
            help_text='Please enter a valid name',
            field_group_class='icon-right',
            icon=mark_safe('<i class="material-icons">landscape</i>')
        )

        def __init__(*args, **kwargs)
            self.user = kwargs.pop('user', None)
            super().__init__(*args, **kwargs)
            self.static_fields['field_1'].data = self.user.username or 'anonymous'
        ...

4. `FlexForm`, `FlexModelForm` designed for rendering good known django forms - `Form`, `ModelForm` with flex layout::

    class CustomFlexForm(FlexForm):
        ...
        field_1 = forms.MultipleChoiceField(
            label='Fruits?',
            choices=(('0', 'Apple'), ('1', 'Mango')),
            widget=forms.CheckboxSelectMultiple(attrs={
                'field_group_class': 'checkbox-as-button checkbox-as-row',
            })
        )
        field_2 = StaticFlexField(
            data='Example', label='Example', help_text='Example')
        )
        field_3 = StaticFlexField(data='Example', label='Example')
        button = FlexButton(BaseButton('Submit'))
        ...

5. `FlexFormset`, `FlexModelFormset`, `FlexInlineFormset` - respectively implementation of
   `BaseFormSet`, `BaseModelFormSet`, `BaseInlineFormSet`::

    class CustomFormSet(FlexFormset):
        ...
        form_css_classes = ['flex-form']  # set this css class for default forms styling
        ...

    formset = formset_factory(CustomFlexForm, CustomFormSet, extra=4)

6. Grid: to locate fields you must specify them in `form_grid` variable as shown below. The Dict key is a row title
   that allows you to horizontally split field rows. If the title is not needed, it must starts with `_` symbol::

    form_grid = {
        'User Info': ['field_1', 'field_2'],
        '_1': ['field_3', ['field_4', 'field_5'], 'field_6'],
        '_2': ['field_7', 'field_8'],
        '_3': ['field_9', 'field_10', 'field_14'],
        '_4': ['field_11'],
        '_5': ['field_12'],
        '_6': ['button'],
    }

7. Template tags::

    {% load flex_forms %}

    {% as_flex form_object %}  # use this tag for rendering form or formset
    {% flex_form_grid form %}  # use this tag for rendering form body generated with form_grid (visible fields)
    {% complex_flex_field field %}  # use this tag for rendering a single flex field of the form


Example

.. image:: https://user-images.githubusercontent.com/33987296/73204264-b7cb5780-414f-11ea-859a-356aecdfd5c7.png