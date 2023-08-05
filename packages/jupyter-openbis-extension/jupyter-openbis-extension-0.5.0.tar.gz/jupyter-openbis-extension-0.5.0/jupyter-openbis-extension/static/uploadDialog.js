define([
        "base/js/dialog",
        "base/js/utils",
        "jquery",
        "./state",
        "./common",
        "./entitySearcher"
    ],
    function (dialog, utils, $, state, common, entitySearcher) {
        var errorElements = { }
        function createErrorElement(name) {
            var element = document.createElement("STRONG")
            element.textContent = ""
            element.style.marginLeft = "8px"
            element.style.color = "red"
            errorElements[name.toLowerCase()] = element
            return element
        }
        function cleanErrors() {
            Object.keys(errorElements).forEach(key => errorElements[key].textContent="")
        }

        var spinner = document.createElement("IMG")
        spinner.className="openbis-feedback"
        spinner.src=""
        function showSpinner(env) {
            var userName = window.location.pathname.split("/")[2];
            spinner.src = '/user/' + userName+ '/nbextensions/jupyter-openbis-extension/spinner.gif'
        }
        function hideSpinner(env) {
            spinner.src=""
        }

        function get_file_list(env, container, path) {
            // get the file list (relative to the notebook) using the existing jupyter api
            var url = env.notebook.base_url + 'api/contents'
            if (path !== "") {
                url = url + '/' + path
            }

            fetch(url)
                .then( function(response) {
                    if (response.ok) {
                        response.json()
                            .then(function(data){
                                createFileTable(env, data, container, state)
                                //state.fileCheckboxes = createFileTable(env, data, container, state.selectedFiles)
                            })
                    }
                    else {
                        console.error(response.status)
                    }
                })
        }

        function get_dataset_list(env, container) {
            var datasets = env.notebook.metadata.datasets
            if (datasets != null) {
                var values = Object.keys(datasets)
                values.sort()
                state.datasetCheckboxes = createSelectTable(values, container, true, state.unselectedDatasets)
            }
        }

        function getOpenBISHistoryId() {
            // Default empty history id
            var resultDatasetHistoryId = "";
            // Search for the history id on the metadata, new format, hidden from the user
            if(Jupyter && 
                Jupyter.notebook && 
                Jupyter.notebook.metadata && 
                Jupyter.notebook.metadata.openbisHistoryId) {
                resultDatasetHistoryId = Jupyter.notebook.metadata.openbisHistoryId;
            }
            // Search for the history id on the cells, older format
            if (!resultDatasetHistoryId) {
                var resultDatasetHistoryIdIdx = 0;
                while(Jupyter.notebook.get_cell(resultDatasetHistoryIdIdx) != null) {
                    var cell = Jupyter.notebook.get_cell(resultDatasetHistoryIdIdx);
                    var cellText = cell.get_text();
                    if(cell.get_text().startsWith("resultDatasetHistoryId='")) {
                        var firstIndexOf = cell.get_text().indexOf("'");
                        var lastIndexOf = cell.get_text().indexOf("'", firstIndexOf + 1);
                        resultDatasetHistoryId = cell.get_text().substring(firstIndexOf + 1, lastIndexOf);
                    }
                    resultDatasetHistoryIdIdx++;
                }
            }
            return resultDatasetHistoryId; // We always return at least the empty one
        }

        function getDatasetTypes(env, connection_name, dataset_types, input_fields) {
            // get all DatasetTypes of a given connection

            var url = env.notebook.base_url + 'openbis/datasetTypes/' + connection_name
            fetch(url)
                .then(function (response) {
                    if (response.ok) {
                        response.json()
                            .then(function (data) {
                                var change_input_fields = function () {
                                    hideSpinner(env)
                                    cleanErrors()

                                    var oldType = state.uploadDataSetType
                                    if (oldType != null && !(oldType in state.uploadDataSetTypes)) {
                                        state.uploadDataSetTypes[oldType] = {}
                                    }

                                    state.uploadDataSetType = dataset_types.options[dataset_types.selectedIndex].value

                                    // remove existing input fields
                                    while (input_fields.firstChild) {
                                        var element = input_fields.firstChild

                                        if (element.nodeName === "INPUT" && state.uploadDataSetType != null) {
                                            state.uploadDataSetTypes[oldType][element.name] = element.value
                                        }

                                        input_fields.removeChild(element)
                                    }

                                    // for every property assignment, create an input field.
                                    for (pa of dts[dataset_types.selectedIndex].propertyAssignments) {
                                        var input_title = document.createElement("STRONG")
                                        input_title.textContent = pa.mandatory ? pa.label + " (mandatory)" : pa.label
                                        var input_error = createErrorElement('prop.'+pa.code)

                                        var input_field = document.createElement("INPUT")
                                        input_field.type = "text"
                                        input_field.name = pa.code
                                        input_field.placeholder = pa.description ? pa.description : pa.label
                                        input_field.size = 90
                                        input_field.style.width="100%"

                                        var mem = state.uploadDataSetTypes[dts[dataset_types.selectedIndex].code]
                                        if (mem == null) {
                                            mem = {
                                                "$HISTORY_ID" : getOpenBISHistoryId() // History Id should get automatically populated if available
                                            }
                                        }
                                        input_field.value = pa.code in mem ? mem[pa.code] : ""

                                        input_fields.appendChild(input_title)
                                        input_fields.appendChild(input_error)
                                        input_fields.appendChild(input_field)
                                        input_fields.appendChild(document.createElement("BR"))
                                    }
                                }
                                dataset_types.onchange = change_input_fields

                                // remove the old and add the new dataset-types
                                dts = data.dataSetTypes
                                while (dataset_types.firstChild) {
                                    dataset_types.removeChild(dataset_types.firstChild);
                                }
                                var index = 0
                                var selectedIndex = -1
                                for (dt of dts) {
                                    var option = document.createElement("OPTION")
                                    option.value = dt.code
                                    option.textContent = dt.description ? dt.code + ": " + dt.description : dt.code
                                    dataset_types.appendChild(option)

                                    if (dt.code === state.uploadDataSetType) {
                                        selectedIndex = index
                                    }
                                    index++
                                }

                                dataset_types.selectedIndex = selectedIndex === -1 ? 0 : selectedIndex
                                // change the input fields, since we just received new datasetTypes
                                change_input_fields()

                            })
                            .catch(function (error) {
                                console.error("Error while parsing dataset types", error)
                            })

                    }
                    else {
                        // ! response.ok
                        errorElements.main.textContent = "Network problem: please check your connection first."
                        while (dataset_types.firstChild) {
                            dataset_types.removeChild(dataset_types.firstChild);
                        }
                    }
                })
                .catch(function (error) {
                    console.error("Error while fetching dataset types:", error)
                })

        }

        function createSelectTable(values, container, checked, overrides) {

            var table = document.createElement("TABLE")
            table.className = 'table-bordered table-striped table-condensed'
            table.style.width = "100%"
            
            var body = table.createTBody()

            var checkboxes = []
            values.forEach( value => {
                var row = body.insertRow()
                var checkbox = document.createElement("INPUT")
                checkbox.type = "checkbox"
                checkbox.value = value
                checkbox.checked = overrides.includes(value) ? !checked :  checked
                checkboxes.push(checkbox)
                row.insertCell().appendChild(checkbox)
                var valueCell = row.insertCell()
                valueCell.textContent = value
                valueCell.style.width = "100%"
            })
            container.appendChild(table)

            return checkboxes
        }

        function createFileTable(env, data, container, state) {
            // list of files that will be uploaded as a dataSet.

            var table = document.createElement("TABLE")
            table.className = 'table-bordered table-striped table-condensed'
            table.style.width = "100%"

            var body = table.createTBody()
            if (data.path !== "") {
                var row = body.insertRow()
                row.insertCell()
                var iconCell = row.insertCell()
                iconCell.className = "item_icon folder_icon icon-fixed-width"
                var filenameCell = row.insertCell()
                filenameCell.textContent = ".."
                filenameCell.style.width = "80%"
                filenameCell.style.cursor = "pointer"
                filenameCell.onclick = function(){
                    var elems = data.path.split('/')
                    elems.pop()
                    get_file_list(env, container, elems.join('/'))
                }

                var sizeCell = row.insertCell()
                sizeCell.style.textAlign = "right"
                sizeCell.style.width = "15%"
            }

            var registerFile = function () {
                if (this.checked) {
                    // add file to state
                    state.selectedFiles.push(this.value)
                }
                else {
                    // remove file from state
                    state.selectedFiles.splice(state.selectedFiles.indexOf(this.value), 1)
                }
            }

            var checkboxes = []
            data.content.sort( (a, b) => a.name.localeCompare(b.name, undefined, {sensitivity: 'base'}) ).forEach( file => {

                var row = body.insertRow()
                var checkboxCell = row.insertCell()
                checkboxCell.style.width="5%"
                var iconCell = row.insertCell()
                var filenameCell = row.insertCell()

                filenameCell.textContent = file.name
                filenameCell.style.width = "100%"
                filenameCell.style.cursor = "pointer"

                var checkbox = document.createElement("INPUT")
                checkbox.type = "checkbox"
                checkbox.value = file.path
                checkbox.checked = state.selectedFiles.includes(file.path) ? true: false
                checkbox.onclick = registerFile
                checkboxes.push(checkbox)
                checkboxCell.appendChild(checkbox)

                if (file.type === "directory") {
                    iconCell.className = "item_icon folder_icon icon-fixed-width"
                    filenameCell.onclick = function () {
                        get_file_list(env, container, file.path)
                    }
                    iconCell.onclick = function () {
                        checkbox.checked = !checkbox.checked
                        registerFile.call(checkbox)
                    }
                }
                else {

                    if (file.type === "notebook") {
                        iconCell.className = "item_icon notebook_icon icon-fixed-width"
                    }
                    else {
                        iconCell.className = "item_icon file_icon icon-fixed-width"
                    }
                    filenameCell.onclick = function () {
                        checkbox.checked = !checkbox.checked
                        registerFile.call(checkbox)
                    }
                }

                var sizeCell = row.insertCell()
                sizeCell.textContent = file.size
                sizeCell.style.textAlign = "right"
                sizeCell.style.width = "15%"

            })
            container.innerHTML = ""
            container.appendChild(table)
            return checkboxes
        }

        return {
            help: 'upload Notebook and Data to openBIS',
            icon: 'fa-upload',
            help_index: '',
            handler: function (env) {

                var main_error = createErrorElement('main')

                var dst_title = document.createElement("STRONG")
                dst_title.textContent = "choose a dataSet type"
                var dataset_types = document.createElement("SELECT")
                dataset_types.id = "dataset_type"
                dataset_types.className = "form-control select-xs"
                dataset_types.style.marginLeft = 0
                dataset_types.style.padding = 0

                var input_fields = document.createElement("DIV")
                input_fields.setAttribute("id", "upload-input-fields");

                getDatasetTypes(env, state.connection.name, dataset_types, input_fields)

                var sample_title = document.createElement("STRONG")
                sample_title.textContent = "enter a sample/experiment identifier to attach this dataSet to:"

                var sample_error = createErrorElement('entityIdentifier')

                //var entityIdentifier = entitySearcher.getEntitySearcherForUpload(state)
                var entityIdentifier = document.createElement("INPUT")
                entityIdentifier.type = "text"
                entityIdentifier.name = "entityIdentifier"
                entityIdentifier.size = 40
                entityIdentifier.placeholder = "Sample or Experiment identifier/permId"
                entityIdentifier.value = state.entityIdentifier ? state.entityIdentifier : ""

                var ds_title = document.createElement("STRONG")

                var dataSetListContainer = document.createElement("DIV")
                if (env.notebook.metadata.datasets) {
                    ds_title.textContent = "Parent DataSets"
                    dataSetListContainer.style.maxHeight="150px"
                    dataSetListContainer.style.overflow="auto"
                    get_dataset_list(env, dataSetListContainer)
                }

                var files_title = document.createElement("STRONG")
                files_title.textContent = "Files to upload"
                var fileListContainer = document.createElement("DIV")
                fileListContainer.style.height="200px"
                fileListContainer.style.overflow="auto"
                // get the relative path
                let re = new RegExp(env.notebook.notebook_name+"$")
                rel_path = env.notebook.notebook_path.replace(re, "")
                get_file_list(env, fileListContainer, rel_path)
                
                var inputs = document.createElement("DIV")
                inputs.style.marginTop = '10px'
                inputs.appendChild(main_error)
                inputs.appendChild(spinner)
                inputs.appendChild(document.createElement("BR"))
                inputs.appendChild(dst_title)
                inputs.appendChild(dataset_types)
                inputs.appendChild(input_fields)
                inputs.appendChild(sample_title)
                inputs.appendChild(document.createElement('BR'))
                inputs.appendChild(sample_error)
                inputs.appendChild(entityIdentifier)
                inputs.appendChild(document.createElement('BR'))
                inputs.appendChild(ds_title)
                inputs.appendChild(document.createElement('BR'))
                inputs.appendChild(dataSetListContainer)
                inputs.appendChild(files_title)
                inputs.appendChild(fileListContainer)

                var uploadDialogBox = $('<div/>').append(inputs)

                function saveState() {
                    state.uploadDataSetTypes[state.uploadDataSetType] = {}
                    for (element of input_fields.children) {
                        if (element.nodeName === "INPUT" && state.uploadDataSetType != null) {
                            state.uploadDataSetTypes[state.uploadDataSetType][element.name] = element.value
                        }
                    }
                    state.unselectedDatasets = state.datasetCheckboxes.filter(cb => !cb.checked).map(cb => cb.value)
                    //state.selectedFiles = state.fileCheckboxes.filter(cb => cb.checked).map(cb => cb.value)
                }

                function onOk() {
                    var connection_name = state.connection.name

                    if (!connection_name) {
                        alert("No connection selected")
                        return false
                    }

                    var uploadUrl = env.notebook.base_url + 'openbis/dataset/' + connection_name

                    // add this notebook to the list of files
                    var files = state.selectedFiles
                    if (! files.includes(env.notebook.notebook_path)) {
                        files.push(env.notebook.notebook_path)
                    }
                    //console.log(files)

                    var props = {}
                    for (input of $('#upload-input-fields').find('input')) {
                        props[input.name] = input.value
                    }

                    var dataSetInfo = {
                        "type": dataset_types.value,
                        "files": files,
                        "parents": state.datasetCheckboxes.filter(cb => cb.checked).map(cb => cb.value),
                        "entityIdentifier": entityIdentifier.value,
                        "props": props
                    }
                    console.log(dataSetInfo);

                    var settings = {
                        url: uploadUrl,
                        processData: false,
                        type: 'POST',
                        dataType: 'json',
                        data: JSON.stringify(dataSetInfo),
                        contentType: 'application/json',
                        success: function (data) {
                            saveState()
                            $('div.modal').remove()
                            $('div.modal-backdrop').remove()
                            common.createFeedback('success', data.statusText)

                            // write statusText from returned data to notebooks metadata
                            if (typeof env.notebook.metadata.openbis === 'undefined') {
                                env.notebook.metadata.openbis = {}
                            }
                            if (typeof env.notebook.metadata.openbis.permIds === 'undefined') {
                                env.notebook.metadata.openbis.permIds = {}
                            }
                            if (data.permId) {
                                env.notebook.metadata.openbis.permIds[data.permId] = data.statusText
                            }
                        },
                        error: function (data) {
                            hideSpinner()

                            if ("errors" in data.responseJSON) {
                                var errors = data.responseJSON.errors
                                for (error of errors) {
                                    let key, value
                                    Object.keys(error).forEach(k => {
                                        key = k.toLowerCase()
                                        value = error[k]
                                    })
                                    errorElements[key in errorElements ? key : "main"].textContent = value
                                }
                            } else {
                                errorElements["main"].textContent = "Server error"
                            }
                        }
                    }

                    showSpinner(env)
                    cleanErrors()
                    utils.ajax(settings)
                    return false
                }

                function onCancel() {
                    saveState()
                    return true
                }
                dialog_params = {
                    body: uploadDialogBox,
                    title: 'Upload openBIS DataSet',
                    buttons: {
                        'Cancel': {
                            click: onCancel
                        },
                        'Upload': {
                            class: 'btn-primary btn-large',
                            click: onOk
                        }
                    },
                    notebook: env.notebook,
                    keyboard_manager: env.notebook.keyboard_manager
                }

                var notebook = IPython.notebook

                var code_for_requirements = ""
                var requirements_filename = ""
                var code_for_runtime = ""
                var runtime_filename = ""
                if (notebook.metadata.kernelspec.language == "python") {
                    code_for_requirements = "import pkg_resources; print(\"\\n\".join([\"{}=={}\".format(i.key, i.version) for i in pkg_resources.working_set]))"
                    code_for_runtime = "import sys; print('python-' + str(sys.version_info[0]) + '.' + str(sys.version_info[1]))"
                    requirements_filename = "requirements.txt"
                    runtime_filename = "runtime.txt"
                }
                else if (notebook.metadata.kernelspec.language == "R") {
                    code_for_requirements = ""
                    requirements_filename = "runtime.txt"
                }
                function save_requirements(data) {
                    notebook.metadata.language_info.requirements_list = data
                    notebook.metadata.language_info.requirements_filename = requirements_filename
                    state.requirements_list = data
                    state.requirements_filename = requirements_filename
                }
                function save_runtime(data) {
                    notebook.metadata.language_info.runtime = data
                    notebook.metadata.language_info.runtime_filename = runtime_filename
                    state.runtime = data
                    state.runtime_filename = runtime_filename
                }
                var req_callback = {
                    iopub: {
                        output: (data) => save_requirements(data.content.text.trim())
                    }
                };
                var rt_callback = {
                    iopub: {
                        output: (data) => save_runtime(data.content.text.trim())
                    }
                };

                var kernel = IPython.notebook.kernel
                kernel.execute(code_for_requirements, req_callback)
                kernel.execute(code_for_runtime, rt_callback)


                function send_runtime_requirements(state) {
                    var endpoint = env.notebook.base_url + 'requirements'
                    var notebook_path = IPython.notebook.notebook_path

                    body = {
                        "notebook_path": notebook_path,
                        "requirements_list": state.requirements_list,
                        "requirements_filename": state.requirements_filename,
                        "runtime": state.runtime,
                        "runtime_filename": state.runtime_filename
                    }

                    var xsrf_token = common.getCookie('_xsrf')
                    fetch(endpoint, {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                            "X-XSRFToken": xsrf_token,
                            "credentials": "same-origin",
                        },
                        body: JSON.stringify(body)
                    })
                        .then(function (response) {
                            if (response.ok) {
                                //alert(response.status)
                            }
                            else {
                                //alert(response.status)
                            }

                        })
                        .catch(
                            error => console.error(
                                "Error while attempting to write requirement files: ", error
                            )
                        )
                }
                send_runtime_requirements(state)

                if (env.notebook.dirty === true) {
                    env.notebook.save_notebook()
                        .then(function () {
                            dialog.modal(dialog_params)
                        })
                        .catch(function (error) {
                            dialog.modal({
                                body: error,
                                title: 'Error saving the notebook',
                                buttons: {
                                    'Back': {}
                                },
                                notebook: env.notebook,
                                keyboard_manager: env.notebook.keyboard_manager
                            })
                        })
                }
                else {
                    dialog.modal(dialog_params)
                }
            }
        }
    }
)
