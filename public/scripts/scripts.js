var config = {
    final_task_selected_count: 1,
    task_expires: true,
    task_expires_in_seconds: 150 * 10,
    stopCountDown: false,
    api_url: "http://127.0.0.1:5000/",
    endpoints: {
        events: "events/",
        choicesets: "choicesets/",
        recommendations: "recommendations/",
        final_set: "final_sets/",
        performances: "performances/",
        questions: "questions/",
    },
    events : {
        task_creation: 1,
        timer_started: 2,
        timer_finished: 3,
        sort_by_column: 4,
        hide_column: 5,
        selected: 6,
        questionnaire_started: 7,
        question_answered: 8,
        task_finish: 13
    }
};

var locals = {
    dev_tools_messages: {
        title: 'Restricted action',
        message: 'Unfortunately, you can not finish task. </br>\n' +
            'Thank you for your attendance.'
    },
    timeout: {
        title: 'Timeout',
        message: 'Unfortunately, your time run out </br>\n' +
                'Thank you for your attendance.'
    },
    task_completed: {

    }
}

var groupConfigurations = {
    1: {
        "hide_buttons": false,
        "sort_tables": false
    },
    2: {
        "hide_buttons": false,
        "sort_tables": true
    },
    3: {
        "hide_buttons": true,
        "sort_tables": true
    },
    4: {
        "hide_buttons": true,
        "sort_tables": false
    },
};

var dataTablesOptions = {
    "bFilter": false,
    "bPaginate": false,
    "lengthChange": false,
    "info": false,
    "ordering": true,
    "order": []
};

var dataTables = {
    columns: {},
    tables: {
        taskRecommendationDt: null,
        taskDt: null
    },
    hideColumnEvent: false
};

var dataStorage = {
    setObject: function (key, value) {
        localStorage.setItem(key, JSON.stringify(value));
    },
    getObject: function (key) {
        var value = localStorage.getItem(key);
        return value && JSON.parse(value);
    }
};

let requestHandler = {
    sendRequest: function (url, requestData, successCallback, errorCallback) {
        $.ajaxSetup({
            scriptCharset: "utf-8", //or "ISO-8859-1"
            contentType: "application/json; charset=utf-8"
        });
        return $.ajax({
            type: "POST",
            url: url,
            dataType: 'json',
            crossOrigin: true,
            header: {
                "Access-Control-Allow-Origin": "*"
            },
            data: JSON.stringify(requestData),
            success: successCallback
        });
    },

    sendGetRequest: function (url, successCallback, errorCallback) {
        $.ajaxSetup({
            scriptCharset: "utf-8", //or "ISO-8859-1"
            contentType: "application/json; charset=utf-8"
        });
        return $.ajax({
            type: "GET",
            url: url,
            dataType: 'json',
            crossOrigin: true,
            header: {
                "Access-Control-Allow-Origin": "*"
            },
            success: successCallback
        });
    }
}

RegExp.quote = function(str) {
    return str.replace(/([.?*+^$[\]\\(){}|-])/g, "\\$1");
};

String.prototype.replaceArray = function(find, replace) {
    var replaceString = this;
    var regex;
    for (var i = 0; i < find.length; i++) {
        regex = new RegExp(RegExp.quote(find[i]), "g");
        replaceString = replaceString.replace(regex, replace[i]);
    }
    return replaceString;
};

QuestionAnswer = {
    cleanAnswers: function (answersStringArray) {
        let answersCollection = [];
        let answers = answersStringArray.slice(1).slice(0, answersStringArray.length - 2).split("], ");
        for (let i = 0; i < answers.length; i++) {
            let cleanAnswerFirst = answers[i].replaceArray(['[', ']', "'"], ['', '', '']).split(', ');
            answersCollection.push({id: cleanAnswerFirst[0], answer: cleanAnswerFirst[1]});
        }
        return answersCollection;
    }
};
// ToDo: Fix! When console is open code can not detect it.
var isTaskCreated = false;
var devtools = function () {
};
devtools.toString = function () {
    console.log(isTaskCreated);
    if (isTaskCreated === true && !this.opened) {
        localStorage.clear();
        let eventsUrl = config.api_url + config.endpoints.events;
        requestHandler.sendRequest(eventsUrl, {
            task_id: localStorage.getItem('task_id') !== null ? localStorage.getItem('task_id') : data.task_id,
            treatment_group: localStorage.getItem('group') !== null ? localStorage.getItem('task_id') : data.treatment_group,
            event_type: config.events.task_finish,
            data: {status: 'task_finish', reason: "DevTools is opened"}
        });
        document.getElementsByTagName('html')[0].innerHTML = tmpl('kickout-tmpl', {
            title: locals.dev_tools_messages.title,
            message: locals.dev_tools_messages.message
        });
    }
    this.opened = true;
}
console.log('%c', devtools);
window.onbeforeunload = function() {
 return "Leaving this page will reset the task";
};

// ToDo: What to do with performance - peff. bu oldu amma bu ola bilerdi. - Your performance / Maximum performance / Your remuneration (?) / Your reward is:
// ToDo: Message to user: Do not loose your code
// ToDo: Send all user actions to backend as event
var myStorage = window.localStorage;
var currentTab = 0;

$(document).ready(function () {

    $(".start-button").click(function () {
        isTaskStarted = true;
        localStorage.clear();
        let createTaskUrl = config.api_url + config.endpoints.events;
        requestHandler.sendRequest(createTaskUrl, {"event_type": config.events.task_creation}, createTask);
    });

    $(document).on('click', '.proceed-button', function () {
        if (confirm('Do you really want to complete task and proceed to questionnaire?')) {
            config.stopCountDown = true;
            finishTask();
        }
    });

    $(document).on('change', '.hide-column', function (e) {
        // Prevent sending event request for order recommendation table because of redraw table
        dataTables.hideColumnEvent = true;
        let checkboxId = $(this).attr('id');
        let hideColumnCheckboxes = $('.hide-column');
        let notCheckedColumns = $(document).find('.hide-column:not(:checked)');
        if ($(document).find('.hide-column:checked').length >= 3) {
            notCheckedColumns.prop("disabled", true);
        } else {
            notCheckedColumns.prop("disabled", false);
        }
        hideColumns(checkboxId, hideColumnCheckboxes.length, $(this).is(':checked'));

        if (notCheckedColumns.length > 4) {
            updateRecommendationDataTable({}, true);
        } else {
            let uncheckedValues = [];
            notCheckedColumns.each(function (key, val) {
                uncheckedValues[key] = $(this).val();
            });

            var recommendationUrl = config.api_url + config.endpoints.recommendations;
            requestHandler.sendRequest(recommendationUrl, {
                "task_id": localStorage.getItem('task_id'),
                "columns_to_use": uncheckedValues.join(' ')
            }, updateRecommendationDataTable);
            // $(this).val()
        }
        eventHideColumns($(this).val(), $(this).is(':checked') ? "True" : "False");
    });

    $('.task-data-table').on( 'order.dt', function () {
        // This will show: "Ordering on column 1 (asc)", for example
        var order = table.order();
    } );

    $(document).on('change', '.check-final', function () {
        checkUncheckRow($(this));
    });

    $(document).on('click', '.choicesets-remove', function () {
        removeRowFromDataTable($(this).data('id'));
        let choiceSetRowCheckbox = $('#data-choicesets-' + $(this).data('id'));
        choiceSetRowCheckbox.trigger('click');
    });

    function format(minutes, seconds) {
        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;
        $(document).find('#time').html(minutes + ':' + seconds);
    }

    function createTask(data) {
        localStorage.setItem('task_id', data.task_id);
        localStorage.setItem('group', data.treatment_group);
        let choicesetsUrl = config.api_url + config.endpoints.choicesets;
        isTaskCreated = true;
        requestHandler.sendRequest(choicesetsUrl, {"task_id": data.task_id}, createTaskDataTable);
        if (config.task_expires === true) {
            let timer = new CountDownTimer(config.task_expires_in_seconds),
                timeObj = CountDownTimer.parse(config.task_expires_in_seconds);

            format(timeObj.minutes, timeObj.seconds);
            timer.onTick(format);
            timer.start(function () {
                // finish experiment
                if ($(document).find('.task-final-data-table tbody tr').length == config.final_task_selected_count) {
                    finishTask();
                } else {
                    document.getElementsByTagName('html')[0].innerHTML = tmpl('kickout-tmpl', {
                        title: locals.timeout.title,
                        message: locals.timeout.message
                    });
                    let eventsUrl = config.api_url + config.endpoints.events;
                    requestHandler.sendRequest(eventsUrl, {
                        task_id: localStorage.getItem('task_id'),
                        treatment_group: localStorage.getItem('group'),
                        event_type: config.events.task_finish,
                        data: {status: 'task_finish', reason: "Timeout"}
                    });
                }
            });
        }
    }

    function finishTask() {
        // Send summirized request
        let finalSets = $('.task-final-data-table').find('.selected-choiceset')
        if (finalSets.length === config.final_task_selected_count) {
            let eventsEndpoint = config.api_url + config.endpoints.final_set;
            let selected = [];
            finalSets.each(function (k,v) {
                selected.push(parseInt($(this).val()));
            });

            requestHandler.sendRequest(eventsEndpoint, {
                "task_id": localStorage.getItem('task_id'),
                "ids": selected,
                "recommendation_id" : localStorage.getItem('current_recommendation_id')
            }, function () {
                // request & show performance & go to questionnaire
                requestHandler.sendRequest(config.api_url + config.endpoints.performances, {
                    "task_id": localStorage.getItem('task_id'),
                    "recommendation_id": localStorage.getItem('current_recommendation_id'),
                    "treatment_group": localStorage.getItem('group')
                }, function () {
                    // ToDo: What to do with performance

                    requestHandler.sendGetRequest(config.api_url + config.endpoints.questions, function (data) {
                        document.getElementById('container').innerHTML = tmpl('questionnaire-tmpl', {questions: data[0], questionProperty: QuestionAnswer});
                        showTab(currentTab); // Display the current tab
                    });
                });
            });
        }
    }

    function getDataTablesColumns(columns) {
        var collection = [{
            'title': '',
            'data': 'checkbox'
        }];
        for (var i = 0; i < columns.length; i++) {
            collection[i + 1] = {
                "title": columns[i],
                "data": columns[i]
            };
        }
        return collection;
    }

    function getDataTableContent(tableType, data) {
        let collection = [];
        if (data) {
            if (data[0].recommendation_id) {
                localStorage.setItem('current_recommendation_id', data[0].recommendation_id);
            }
            for (let i = 0; i < data.length; i++) {
                let recommendationAttribute = '',
                    checkboxId = tableType == 'choicesets' ? data[i].id : data[i].choice_id;
                if (tableType == 'recommendation') {
                    recommendationAttribute = 'data-recommendation="' + data[i].recommendation_id + '"';
                }
                collection[i] = {'checkbox': '<input type="checkbox" value="' + checkboxId + '" ' + recommendationAttribute + ' data-id="' + checkboxId + '" data-type="' + tableType + '" id="data-' + tableType + '-' + checkboxId + '" class="check-final" />'};
                for (const [key, value] of Object.entries(data[i])) {
                    $.extend(collection[i], data[i]);
                }
            }
        }
        return collection;
    }

    function eventChoicesetTableSorted(event){
        let table = dataTables.tables.taskDt.order();
        eventTableSorted(event, table, "choiceset");
    }

    function eventRecommendationTableSorted(event){
        let table = dataTables.tables.taskDt.order();
        eventTableSorted(event, table, "recommendation");
    }

    function eventTableSorted(event, table, tableName = "choiceset") {
        if (event.type !== 'order') {
            return;
        }
        let hiddenColumns = [];
        $(".hide-column:checked").each(function() {
            hiddenColumns.push($(this).val());
        });
        let eventData = {
            "task_id": localStorage.getItem('task_id'),
            "treatment_group": localStorage.getItem('group'),
            "event_type": config.events.sort_by_column,
            "data" : {
                "column" : dataStorage.getObject('columns')[(table[0][0]-1)],
                "direction" : table[0][1].toUpperCase(),
                "table" : tableName,
                "hidden_columns" : hiddenColumns.join(" ")
            }
        };
        let tableSortedEvent = config.api_url + config.endpoints.events;
        requestHandler.sendRequest(tableSortedEvent, eventData, function (data) {

        });
    }

    function eventHideColumns(column, hideState, table = "choiceset") {
        let eventData = {
            "task_id": localStorage.getItem('task_id'),
            "treatment_group": localStorage.getItem('group'),
            "event_type": config.events.hide_column,
            "data" : {
                "column" : column,
                "state" : hideState,
                "table" : table
            }
        };
        let tableSortedEvent = config.api_url + config.endpoints.events;
        requestHandler.sendRequest(tableSortedEvent, eventData, function (data) {

        });
    }

    function getGroupConfigurations(){
        return groupConfigurations[localStorage.getItem('group')];
    }

    function getCommonDataTableConfigurations(tableColumns) {
        let commonDtOptions = {};
        $.extend(commonDtOptions, dataTablesOptions, {
            "columns": tableColumns,
            "ordering": getGroupConfigurations().sort_tables,
            "columnDefs": [
                {"orderable": false, "targets": 0}
            ]
        });
        return commonDtOptions;
    }

    // Building achoice sets data tables
    function createTaskDataTable(choiceSetData) {
        storeDataInLocalStorage('choice_set', choiceSetData.choice_set);
        choiceSetData.task_description = ">The description of the task";
        choiceSetData.disable_hide_column = getGroupConfigurations().hide_buttons;
        choiceSetData.task_expires = config.task_expires;
        document.getElementById('container').innerHTML = tmpl('tmpl-demo', choiceSetData)
        dataTables.columns = getDataTablesColumns(choiceSetData.columns);
        dataStorage.setObject('columns', choiceSetData.columns)
        var recommendationUrl = config.api_url + config.endpoints.recommendations;
        requestHandler.sendRequest(recommendationUrl, {
            "task_id": localStorage.getItem('task_id'),
            "columns_to_use": choiceSetData.columns.join(" ")
        }, createRecommendationDataTable);

        var taskDtOptions = {};
        var commonDataTableConfigurations = getCommonDataTableConfigurations(dataTables.columns);
        $.extend(taskDtOptions, commonDataTableConfigurations, {
            "scrollY": "524px",
            "scrollCollapse": true,
        });

        dataTables.tables.taskDt = $('.task-data-table').DataTable(taskDtOptions);
        dataTables.tables.taskDt.rows.add(getDataTableContent('choicesets', choiceSetData.choice_set)).draw();
        dataTables.tables.taskFinalDt = $('.task-final-data-table').DataTable($.extend(commonDataTableConfigurations, {
            "scrollY": "160px",
        }));
        $('.task-data-table').on('order.dt', function (event) {
            eventChoicesetTableSorted(event);
        });
    }

    // Building a recommendations data tables
    function createRecommendationDataTable(recommendationsData, initial = false) {
        if (initial) {
            storeDataInLocalStorage('recommendations', recommendationsData.message);
        }
        var recommendedDtOptions = {};
        $.extend(recommendedDtOptions, getCommonDataTableConfigurations(dataTables.columns));
        dataTables.tables.taskRecommendationDt = $('.task-recommendation-data-table').DataTable(recommendedDtOptions);
        dataTables.tables.taskRecommendationDt.rows.add(getDataTableContent('recommendation', recommendationsData.message)).draw();
        $('.task-recommendation-data-table').on('order.dt', function (event) {
            if (dataTables.hideColumnEvent !== true) {
                eventRecommendationTableSorted(event);
            }
        });
    }

    // Update a recommendations data tables
    function updateRecommendationDataTable(recommendationsResponse, showInitial = false) {
        let recommendationsData;
        if (showInitial === true) {
            recommendationsData = dataStorage.getObject('recommendations');
        } else {
            recommendationsData = recommendationsResponse.message;
        }

        let dataTableRows = getDataTableContent('recommendation', recommendationsData);
        dataTables.tables.taskRecommendationDt.clear();
        dataTables.tables.taskRecommendationDt.rows.add(dataTableRows).draw();

        $('.task-data-table .check-final:checked').each(function (key, value) {
            let recommendationCheckbox = $('#data-recommendation-' + $(value).val());
            recommendationCheckbox.prop("checked", true);
            changeSelectedRowColor(recommendationCheckbox);
        });
        // Disable all recommendation inputs if 5 item is already selected/checked
        if ($('.task-final-data-table tbody tr').length === config.final_task_selected_count || $('.task-data-table .check-final:checked').length === config.final_task_selected_count) {
            $('.task-recommendation-data-table .check-final:not(:checked)').prop("disabled", true);
        }
        dataTables.hideColumnEvent = false;
    }

    function storeDataInLocalStorage(key, data) {
        dataStorage.setObject(key, data);
    }

    // Add row to the final data tables
    function addRowToDataTable(selectedRowData) {
        var row = {
            'checkbox': '<button type="button" id="data-item-' + selectedRowData.id + '" data-id="' + selectedRowData.id + '" class="choicesets-remove">x</button>' +
                '<input type="hidden" value="' + selectedRowData.id + '" id="data-item-' + selectedRowData.id + '" class="selected-choiceset" />'
        };
        $.extend(row, selectedRowData);
        let table = dataTables.tables.taskFinalDt;
        table.row.add(row).node().id = 'tr-final-' + selectedRowData.id;
        table.draw();
        addSelectedStorageList(selectedRowData.id);
    }

    function addSelectedStorageList(selectedId) {
        let selected_ids = dataStorage.getObject('selected_ids');
        let currentList = selected_ids ? selected_ids : [];
        if (currentList.length <= 0) {
            currentList = [selectedId];
            dataStorage.setObject('selected_ids', currentList);
            return;
        }
        if (currentList.length > 0 && currentList.includes(selectedId) === false) {
            currentList.push(selectedId);
            dataStorage.setObject('selected_ids', currentList);
        }
    }

    function removeSelectedStorageList(unSelectedId){
        const id = parseInt(unSelectedId);
        let currentList = dataStorage.getObject('selected_ids');
        if (!currentList) {
            return;
        }
        if (currentList.length > 0 && currentList.includes(id) !== false) {
            const index = currentList.indexOf(id);
            if (index > -1) {
                currentList.splice(index, 1);
            }
            dataStorage.setObject('selected_ids', currentList);
        }
    }

    // Remove row to the final data tables
    function removeRowFromDataTable(id) {
        dataTables.tables.taskFinalDt.row('#tr-final-' + id).remove();
        $('.task-final-data-table tbody tr#tr-final-' + id).remove();
        removeSelectedStorageList(id);
    }

    function checkUncheckRow($this) {
        syncCheck($this);
        if ($this.is(':checked')) {
            let findRow;
            let choiceSets = dataStorage.getObject('choice_set');
            findRow = choiceSets.find(x => x.id == $this.val());
            addRowToDataTable(findRow);
        } else {
            removeRowFromDataTable($this.val());
        }
        let totalCheckedTask = $('.task-data-table').find('.check-final:checked').length;
        let totalFinalTableItems = $('.task-final-data-table').find('.selected-choiceset').length;
        $('.total-selected').html(totalCheckedTask);
        if (totalCheckedTask <= config.final_task_selected_count || totalFinalTableItems <= config.final_task_selected_count) {
            // Change color synchronously
            changeSelectedRowColor($this);
            if (totalCheckedTask == config.final_task_selected_count) {
                $('.task-data-table .check-final:not(:checked), .task-recommendation-data-table .check-final:not(:checked)').prop("disabled", true);
                $('.proceed-button').prop("disabled", false);
            } else {
                $('.task-data-table .check-final:not(:checked), .task-recommendation-data-table .check-final:not(:checked)').removeAttr('disabled');
                $('.proceed-button').prop("disabled", true);
            }
        }
    }

    function syncCheck($this) {
        let tableType = $this.data('type'),
            syncTableClassName,
            syncCheckId;
        if (tableType == 'recommendation') {
            syncTableClassName = 'task-data-table';
            syncCheckId = 'data-choicesets-' + $this.val();
        } else {
            syncTableClassName = 'task-recommendation-data-table';
            syncCheckId = 'data-recommendation-' + $this.val();
        }
        let syncCheckboxSelector = '.' + syncTableClassName + ' .check-final#' + syncCheckId;
        let synCheckbox = $(syncCheckboxSelector);
        // If choiceset checked then check if recommended exists on table or not
        if (synCheckbox.length <= 0 && tableType == 'choicesets') {
            return;
        }
        synCheckbox.prop("checked", $this.prop('checked'));
        // Change color synchronously
        changeSelectedRowColor(synCheckbox);
    }

    function changeSelectedRowColor($this) {
        if ($this.prop('checked')) {
            $this.closest("tr").css('background-color', '#b1e01f');
        } else {
            $this.closest("tr").removeAttr('style');
        }
    }

    function hideColumns(checkboxId, hideButtonsLength = 5, isChecked) {
        for (var i = 1; i <= hideButtonsLength; i++) {
            if (checkboxId == 'hide-column-' + i) {
                dataTables.tables.taskDt.columns(i).visible(!isChecked);
                dataTables.tables.taskRecommendationDt.columns(i).visible(!isChecked);
                dataTables.tables.taskFinalDt.columns(i).visible(!isChecked);
            }
        }
    }
});

function CountDownTimer(duration, granularity) {
    this.duration = duration;
    this.granularity = granularity || 1000;
    this.tickFtns = [];
    this.running = false;
}

CountDownTimer.prototype.start = function (callback) {
    if (this.running) {
        return;
    }
    this.running = true;
    var start = Date.now(),
        that = this,
        diff, obj;

    (function timer() {
        diff = that.duration - (((Date.now() - start) / 1000) | 0);

        if (config.stopCountDown) {
            return;
        }

        if (diff > 0) {
            setTimeout(timer, that.granularity);
        } else {
            diff = 0;
            that.running = false;
            if (typeof callback === 'function') {
                callback();
            }
        }

        obj = CountDownTimer.parse(diff);
        that.tickFtns.forEach(function (ftn) {
            ftn.call(this, obj.minutes, obj.seconds);
        }, that);
    }());
};

CountDownTimer.prototype.onTick = function (ftn) {
    if (typeof ftn === 'function') {
        this.tickFtns.push(ftn);
    }
    return this;
};

CountDownTimer.prototype.expired = function (callback) {
    return !this.running;
};

CountDownTimer.parse = function (seconds) {
    return {
        'minutes': (seconds / 60) | 0,
        'seconds': (seconds % 60) | 0
    };
};

function showTab(n) {
    // This function will display the specified tab of the form ...
    let x = document.getElementsByClassName("tab");
    x[n].style.display = "block";
    // ... and fix the Previous/Next buttons:
    if (n == 0) {
        document.getElementById("prevBtn").style.display = "none";
    } else {
        document.getElementById("prevBtn").style.display = "inline";
    }
    if (n == (x.length - 1)) {
        document.getElementById("nextBtn").style.display = "none";
        document.getElementById("submitBtn").style.display = "inline";
    } else {
        document.getElementById("nextBtn").display = "inline";
        document.getElementById("submitBtn").style.display = "none";
    }
    // ... and run a function that displays the correct step indicator:
    fixStepIndicator(n)
}

function nextPrev(n) {
    // This function will figure out which tab to display
    var x = document.getElementsByClassName("tab");
    // Exit the function if any field in the current tab is invalid:
    if (n == 1 && !validateForm()) return false;
    // Hide the current tab:
    x[currentTab].style.display = "none";
    // Increase or decrease the current tab by 1:
    currentTab = currentTab + n;
    // if you have reached the end of the form... :
    if (currentTab >= x.length) {
        //...the form gets submitted:
        document.getElementById("regForm").submit();
        return false;
    }
    // Otherwise, display the correct tab:
    showTab(currentTab);
}

function validateForm() {
    var currentTabElm, input, select, i, answered = 0, valid = true;
    let questionGroupsCount = document.getElementById('question-groups-count-' + (currentTab + 1));
    for (let questionsCount = 0; questionsCount < questionGroupsCount.value; questionsCount++) {
        const answeredQuestions = [];
        let questionId = 'group-id-' + (currentTab + 1) + '-question-' + questionsCount;
        let question = document.getElementById(questionId);
        input = question.getElementsByTagName("input");
        select = question.getElementsByTagName("select");
        if (input != null && input.length > 0) {
            for (i = 0; i < input.length; i++) {
                if (input[i].type == 'radio' && input[i].checked == true) {
                    answered++;
                    answeredQuestions.push(questionId)
                    break;
                }
                if (input[i].type == "text" && input[i].value != '') {
                    answered++;
                    answeredQuestions.push(questionId)
                    break;
                }
            }
            for (let i = 0; i < input.length; i++) {
                if (false === answeredQuestions.includes(input[i].parentElement.parentElement.id)) {
                    if (input[i].type == 'radio' && input[i].checked == false) {
                        // Set is-invalid class to all inputs in current question
                        input[i].nextElementSibling.className += " is-invalid";
                        // Waiting for click, if radio button clicked remove is-invalid class from all inputs under parent question
                        input[i].addEventListener("click", function () {
                            for (let i = 0; i < question.children.length; i++) {
                                question.children[i].getElementsByTagName('label')[0].classList.remove("is-invalid")
                            }
                        });
                    }
                    if (input[i].type == 'text' && input[i].value == '') {
                        // Set is-invalid class to all inputs in current question
                        input[i].className += " is-invalid";
                        // Waiting for click, if radio button clicked remove is-invalid class from all inputs under parent question
                        input[i].addEventListener("change", function (elm) {
                            elm.target.classList.remove("is-invalid")
                        });
                    }
                }
            }
        }

        if (select && select.length > 0) {
            for (let i = 0; i < select.length; i++) {
                if (select[i].value === '') {
                    select[i].className += " is-invalid";
                    select[i].addEventListener("change", function (elm) {
                        elm.target.classList.remove("is-invalid");
                    });
                } else {
                    answered++;
                }
            }
        }
    }
    if (questionGroupsCount.value > answered) {
        valid = false;
    }

    // If the valid status is true, mark the step as finished and valid:
    if (valid) {
        document.getElementsByClassName("step")[currentTab].className += " finish";
    }
    return valid; // return the valid status
}

function fixStepIndicator(n) {
    // This function removes the "active" class of all steps...
    var i, x = document.getElementsByClassName("step");
    for (i = 0; i < x.length; i++) {
        x[i].className = x[i].className.replace(" active", "");
    }
    //... and adds the "active" class to the current step:
    x[n].className += " active";
}

function submitAnswers(){
    requestHandler.sendRequest(recommendationUrl, {
        "task_id": localStorage.getItem('task_id'),
        "columns_to_use": choiceSetData.columns.join(" ")
    }, createRecommendationDataTable);
}