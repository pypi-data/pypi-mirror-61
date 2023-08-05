// Client form validator

function FormValidator(formObj){

    const self = this;

    this.dateFormat = 'DD-MM-YYYY';
    this.dateTimeFormat = 'DD-MM-YYYY HH:mm';
    this.timeFormat = 'HH:mm';

    this.dateMin = moment().subtract(1, 'years').startOf('year').format(self.dateFormat);
    this.dateMax = moment().endOf('year').format(self.dateFormat);

    this.silent_field_class = 'js-silent';
    this.valid_input_class = 'is-valid';
    this.invalid_input_class = 'is-invalid';
    this.keep_feedback_on_validation_flag_class = 'js-keep_feedback_on_validation';

    this.no_validation_selector = '.js-no_validation';
    this.input_wrapper_selector = '.js-input_wrapper';
    this.valid_feedback_container_selector = '.js-valid_feedback';
    this.invalid_feedback_container_selector = '.js-invalid_feedback';
    this.input_has_error_selector = '.js-has_error';
    this.elements_to_control_selector = 'button[type="submit"]';

    this.elements_to_validate = 'input, select, textarea';
    this.valid_input_data_attr = 'is-valid';
    this.elements_disable_attr = 'disabled';
    this.input_events = 'keyup change blur';
    this.csrf_token_selector = '[name="csrfmiddlewaretoken"]';
    this.data_attr_for_validator_choose = 'type';

    this.MESSAGES = {
        ERROR_MESSAGES: {
            INVALID_DATE: 'Неверный формат даты',
            INVALID_DATETIME: 'Неверный формат даты и времени',
            INVALID_TIME: 'Неверный формат времени',
            INVALID_DATE_RANGE: 'Дата вне диапазона: ' + self.dateMin + ' - ' + self.dateMax,
            REQUIRED_FIELD: 'Поле обязательно для заполнения',
            MAX_NUM_REQUIRED: 'Необходимое число символов: ',
            SERVER_ERROR: 'Ошибка сервера!'
        },
        SUCCESS_MESSAGES: {
            VALID_FIELD: 'Данные введены верно'
        }
    };

    this.inputs = formObj.find(self.elements_to_validate).not(self.csrf_token_selector).not(self.no_validation_selector);
    this.elements_to_control = formObj.find(self.elements_to_control_selector);

    this.listenInputsEvents = function() {
        // tracking for inputs changes.
        $.each(self.inputs, function () {
            let thisInput = $(this);

            thisInput.on(self.input_events, function () {
                thisInput.data(self.valid_input_data_attr, true);
                thisInput.removeClass(self.silent_field_class);
                self.validateInput(thisInput);

                // Additional operations.
                self.addOperations(thisInput);
            });
        });
    };

    this.addOperations = function(input) {
        // pass
    };

    this.clearStatesForDisabledInputs = function () {
        $.each(self.inputs, function () {
            let thisInput = $(this);

            if(thisInput.attr('disabled')){
                self.clearInputState(thisInput);
            }
        });
    };

    this.initInputs = function() {
        // inputs first initialization.
        $.each(self.inputs, function () {
            let thisInput = $(this);

            self.addRequiredLabel(thisInput);
            thisInput.val() ?
                self.silentProcessInput(thisInput):
                self.checkRequired(thisInput);
        });
    };

    this.silentProcessInput = function(input) {
        // block error display on empty form.
        input.addClass(self.silent_field_class);
        self.validateInput(input);
    };

    this.clearForm = function() {
        formObj.find('.' + self.valid_input_class).removeClass(self.valid_input_class);
        formObj.find('.' + self.invalid_input_class).removeClass(self.invalid_input_class);
        self.inputs.removeData(self.valid_input_data_attr);
        self.inputs.val('');
    };

    this.addRequiredLabel = function(input) {
        input.attr('required') ?
            input.closest(self.input_wrapper_selector).find('label').append(' *'):
            {};
    };

    this.addValidators = function (input) {
     // pass
    };

    this.validateInput = function(input) {
        // validators
        switch (input.data(self.data_attr_for_validator_choose)) {
            case 'date':
                input.val() ?
                    self.validateDate(input, self.dateMin, self.dateMax):
                    self.simpleValidate(input);
                break;
            case 'dateTime':
                input.val() ?
                    self.validateDateTime(input):
                    self.simpleValidate(input);
                break;
            case 'time':
                input.val() ?
                    self.validateTime(input):
                    self.simpleValidate(input);
                break;
            default:
                self.simpleValidate(input);
        }

        self.addValidators(input);
        self.controlElements();
    };

    this.checkFormForValid = function() {
        let formIsValid = true;

        $.each(self.inputs, function() {
            return formIsValid = $(this).data(self.valid_input_data_attr);
        });

        return formIsValid;
    };

    this.controlElements = function() {
        // block elements on errors
        self.checkFormForValid() ?
            self.elements_to_control.attr(self.elements_disable_attr, false) :
            self.elements_to_control.attr(self.elements_disable_attr, true).focus();
    };

    this.setInputValid = function(input, message=null) {
        if(!input.hasClass(self.silent_field_class)){
            input.removeClass(self.valid_input_class + ' ' + self.invalid_input_class).addClass(self.valid_input_class);
        }

        if(message){
            input.closest(self.input_wrapper_selector).find(self.valid_feedback_container_selector)
                .css('display', 'block')
                .text(message);
        }

        input.closest(self.input_wrapper_selector).find(self.invalid_feedback_container_selector).css('display', 'none');
        input.data(self.valid_input_data_attr, true);
    };

    this.setInputInvalid = function(input, message=null) {
        input.removeClass(self.valid_input_class + ' ' + self.invalid_input_class).addClass(self.invalid_input_class);
        if(message){
            let feedbackBlock = input.closest(self.input_wrapper_selector).find(self.invalid_feedback_container_selector);

            feedbackBlock.css('display', 'block');
            feedbackBlock.text(message);
        }

        input.closest(self.input_wrapper_selector).find(self.valid_feedback_container_selector).css('display', 'none');
        input.data(self.valid_input_data_attr, false);
    };

    // Built-in validators

    this.validateCheckbox = function(input) {
        let checkboxValue = input[0].checked;

        input.attr('required') && checkboxValue ?
            self.setInputValid(input) :
            self.setInputInvalid(input);
    };

    this.validateDate = function(input, dateMin, dateMax) {
        let dateValue = input.val();
        let momentDateValue = moment(dateValue, self.dateFormat);
        let momentDateValueStart = moment(dateMin, self.dateFormat);
        let momentDateValueEnd = moment(dateMax, self.dateFormat);

        if(!momentDateValue.isBetween(momentDateValueStart, momentDateValueEnd) && momentDateValue.isValid()){
            self.setInputInvalid(input, self.MESSAGES.ERROR_MESSAGES.INVALID_DATE_RANGE);
        }
        else{
            momentDateValue.isValid() ?
                self.setInputValid(input) :
                self.setInputInvalid(input, self.MESSAGES.ERROR_MESSAGES.INVALID_DATE);
        }
    };

    this.validateDateTime = function(input) {
        let dateValue = input.val();

        moment(dateValue, self.dateTimeFormat).isValid() ?
            self.setInputValid(input) :
            self.setInputInvalid(input, self.MESSAGES.ERROR_MESSAGES.INVALID_DATETIME);
    };

    this.validateTime = function(input) {
        let dateValue = input.val();

        moment(dateValue, self.timeFormat).isValid() ?
            self.setInputValid(input) :
            self.setInputInvalid(input, self.MESSAGES.ERROR_MESSAGES.INVALID_TIME);
    };

    this.checkRequired = function(input) {
        let inputValue = input.val();

        inputValue || !input.attr('required') ?
            input.data(self.valid_input_data_attr, true):
            input.data(self.valid_input_data_attr, false)
    };

    this.simpleValidate = function(input) {
        let inputValue = input.val();

        inputValue || !input.attr('required') ?
            self.setInputValid(input) :
            self.setInputInvalid(input, self.MESSAGES.ERROR_MESSAGES.REQUIRED_FIELD);
    };

    this.validateMaxLength = function(input, maxNum) {
        let length = input.val().length;

        length < maxNum ?
            self.setInputInvalid(input, self.MESSAGES.ERROR_MESSAGES.MAX_NUM_REQUIRED + maxNum):
            self.setInputValid(input);
    };

    this.showFormBackendErrors = function() {
        if (formObj.has(self.input_has_error_selector).length > 0) {
            $(self.input_has_error_selector).find(self.elements_to_validate).not('[type="hidden"]')
                .addClass(self.invalid_input_class)
                .data(self.valid_input_data_attr, false);

            formObj.find(self.invalid_feedback_container_selector).show()
        }
    };

    this.clearInputState = function (input){
        input.removeClass(self.valid_input_class + ' ' + self.invalid_input_class);
        if(!input.hasClass(self.keep_feedback_on_validation_flag_class)){
            input.closest(self.input_wrapper_selector).find(self.valid_feedback_container_selector).text('');
            input.closest(self.input_wrapper_selector).find(self.invalid_feedback_container_selector).text('');
        }
        input.data(self.valid_input_data_attr, true);
    };

    this.init = function() {
        self.initInputs();
        self.showFormBackendErrors();
        self.controlElements();
        self.listenInputsEvents();
    };
}