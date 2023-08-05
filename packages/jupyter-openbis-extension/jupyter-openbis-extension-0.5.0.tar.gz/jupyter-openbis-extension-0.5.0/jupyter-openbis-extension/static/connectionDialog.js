define(
    [
        "base/js/dialog",
        "jquery",
        "./state",
        "./connections"
    ],
    function (dialog, $, state, connections) {

        let currentDownloadPath = null;

        function show_available_connections(env, data, conn_table) {

            if (!currentDownloadPath) {
                currentDownloadPath = data.cwd
            }

            let table = document.createElement("TABLE");
            table.className = 'table-bordered table-striped table-condensed'
            let thead = table.createTHead();
            let thead_row = thead.insertRow(0)
            let titles = ['', 'Name', 'URL', 'Status', 'Username / Password']
            for (title of titles) {
                thead_row.insertCell().textContent = title
            }

            tbody = table.createTBody()

            let getConnectionByName = function (name) {
                for (connection of data.connections) {
                    if (connection.name === name) {
                        return connection;
                    }
                }
            };

            for (connection of data.connections) {
                let conn = document.createElement("INPUT")
                conn.type = "radio"
                conn.name = "connection_name"
                conn.value = connection.name
                conn.setAttribute("url", connection.url)

                conn.checked = connection.name === state.connection.candidateName;
                conn.onclick = function () {
                	state.connection.candidateName = this.value
                	state.connection.candidateDTO = getConnectionByName(state.connection.candidateName);
                }

                let row = tbody.insertRow()
                row.insertCell().appendChild(conn)
                let nameCell = row.insertCell()
                nameCell.textContent = connection.name
                nameCell.onclick = function () {
                    let radio = this.parentElement.firstElementChild.firstElementChild
                    radio.checked = 1
                    state.connection.candidateName = radio.value
                    state.connection.candidateDTO = getConnectionByName(state.connection.candidateName);
                }
                let urlCell = row.insertCell()
                urlCell.textContent = connection.url
                urlCell.onclick = function () {
                    let radio = this.parentElement.firstElementChild.firstElementChild
                    radio.checked = 1
                    state.connection.candidateName = radio.value
                    state.connection.candidateDTO = getConnectionByName(state.connection.candidateName);
                }

                let status_cell = row.insertCell()

                let status_badge = document.createElement("SPAN")
                status_badge.id = connection.name + "-badge"
                status_badge.textContent = connection.status
                if (connection.status === "connected") {
                    status_badge.className = "label label-success"
                } else {
                    status_badge.className = "label label-danger"
                }
                status_cell.appendChild(status_badge)

                let username = document.createElement("INPUT")
                username.type = "text"
                username.name = "username"
                username.autocomplete = "on"
                username.value = connection.username
                username.setAttribute("form", connection.name)

                let password = document.createElement("INPUT")
                password.type = "password"
                password.name = "password"
                password.autocomplete = "current-password"
                password.value = connection.password
                password.setAttribute("form", connection.name)


                // Username / Password form
                let pwform = document.createElement("FORM")
                pwform.id = connection.name
                pwform.onsubmit = function (event) {
                    let form_data = new FormData(this)
                    let status_badge = document.getElementById(this.id + "-badge")
                    status_badge.textContent = "connecting..."
                    status_badge.className = "label label-warning"
                    connections.connect(env, this.id,
                            form_data.get("username"), form_data.get("password")
                        )
                        .then(function (response) {
                            if (status_badge.nextElementSibling !== null) {
                                status_badge.parentNode.removeChild(status_badge.nextElementSibling)
                            }
                            if (response.ok) {
                                status_badge.textContent = "connected"
                                status_badge.className = "label label-success"
                            } else {
                                status_badge.textContent = "not connected"
                                status_badge.className = "label label-danger"
                                message = document.createElement("p")
                                if (response.status === 401) {
                                    message.textContent = "username/password incorrect"
                                } else if (response.status === 500) {
                                    message.textContent = "Connection error"
                                } else {
                                    message.textContent = "General error"
                                }
                                status_badge.parentNode.insertBefore(message, status_badge.nextSibling)
                            }
                        })
                        .catch(error => console.error("Error while attempting to reconnect: ", error))

                    return false
                }


                let connect_button = document.createElement("BUTTON")
                connect_button.className = "btn btn-primary btn-xs"
                connect_button.textContent = "connect"

                pwform.appendChild(username)
                pwform.appendChild(password)
                pwform.appendChild(connect_button)

                let pwCell = row.insertCell()
                pwCell.appendChild(pwform)

                pwCell.onclick = function () {
                    let radio = this.parentElement.firstElementChild.firstElementChild
                    radio.checked = 1
                    state.connection.candidateName = radio.value
                    state.connection.candidateDTO = getConnectionByName(state.connection.candidateName);
                }
            }

            // add row for new connection
            let row = tbody.insertRow()

            let conn_form = document.createElement("FORM")
            conn_form.id = "new_connection"
            conn_form.onsubmit = function (event) {
                let inputs = document.querySelectorAll("input[form=new_connection]")

                data = {}
                for (input of inputs) {
                    data[input.name] = input.value
                }
                for (missing of ['connection_name', 'url', 'username', 'password']) {
                    if (data[missing] === "") {
                        alert("Please provide: " + missing)
                        return false
                    }
                }
                connections.create(env, data.connection_name, data.url, data.username, data.password)
                    .then(function (response) {
                        if (response.ok) {
                            response.json()
                                .then(function (data) {
                                    show_available_connections(env, data, conn_table)
                                })
                        }
                    })
                return false
            }
            let conn_name = document.createElement("INPUT")
            conn_name.type = "input"
            conn_name.name = "connection_name"
            conn_name.setAttribute("form", conn_form.id)
            conn_name.placeholder = "openBIS instance name"
            row.insertCell().appendChild(conn_form)
            row.insertCell().appendChild(conn_name)

            let conn_url = document.createElement("INPUT")
            conn_url.type = "input"
            conn_url.name = "url"
            conn_url.setAttribute("form", conn_form.id)
            conn_url.placeholder = "https://openbis.domain:port"
            row.insertCell().appendChild(conn_url)
            row.insertCell()

            let username = document.createElement("INPUT")
            username.autocomplete = "off"
            username.type = "text"
            username.name = "username"
            username.setAttribute("form", conn_form.id)
            username.placeholder = "username"
            let password = document.createElement("INPUT")
            password.type = "password"
            password.name = "password"
            password.autocomplete = "new-password"
            password.setAttribute("form", conn_form.id)
            let create_btn = document.createElement("BUTTON")
            create_btn.setAttribute("form", conn_form.id)
            create_btn.textContent = "create"
            let uname_pw_cell = row.insertCell()
            uname_pw_cell.appendChild(username)
            uname_pw_cell.appendChild(password)
            uname_pw_cell.appendChild(create_btn)

            conn_table.innerHTML = ""
            let table_title = document.createElement("STRONG")
            table_title.textContent = "Please choose a connection"

            let working_dir_title = document.createElement("STRONG")
            working_dir_title.textContent = "Your working directory "
            let working_dir_in = document.createElement("INPUT")
            working_dir_in.type = "text"
            working_dir_in.name = "working_dir"
            working_dir_in.autocomplete = "on"
            working_dir_in.style.width = "100%"


            // calculate the default working directory
            // by combining the notebook_dir (from the jupyter configuration) and the relative notebook_path
            let re = new RegExp(env.notebook.notebook_name+"$")
            rel_path = env.notebook.notebook_path.replace(re, "")
            let default_working_dir = ""
            if (data.notebook_dir.endsWith('/')) {
                default_working_dir = data.notebook_dir + rel_path
            }
            else {
                default_working_dir = data.notebook_dir + "/" + rel_path
            }

            working_dir_in.value = state.working_dir ? state.working_dir : default_working_dir
            state.working_dir_element = working_dir_in

            let working_dir_reset = document.createElement("A")
            working_dir_reset.className = "btn"
            working_dir_reset.innerText = "reset to default"
            working_dir_reset.onclick = function() {
                working_dir_in.value = default_working_dir
            }

            conn_table.appendChild(table_title)
            conn_table.appendChild(table)

            conn_table.appendChild(working_dir_title)
            conn_table.appendChild(working_dir_reset)
            conn_table.appendChild(document.createElement("BR"))
            conn_table.append(working_dir_in)

        }

        return {
            help: 'configure openBIS connections',
            icon: 'fa-sliders',
            help_index: '',
            handler: function (env) {
                conn_table = document.createElement("DIV")
                let dst_title = document.createElement("STRONG")
                dst_title.textContent = "DataSet type"
                let dataset_types = document.createElement("SELECT")
                dataset_types.id = "dataset_type"
                dataset_types.className = "form-control select-xs"

                conn_table.id = "openbis_connections"

                connections.list(env)
                    .done(function (data) {
                        show_available_connections(env, data, conn_table)
                    })
                    .fail(function (data) {
                        alert(data.status)
                    })

                let uploadDialogBox = $('<div/>').append(conn_table)

                function onOk() {
                    state.connection.name = state.connection.candidateName
                    state.connection.dto = state.connection.candidateDTO
                    state.working_dir = state.working_dir_element.value
                }

                function onCancel() {
                    state.connection.candidateName = state.connection.name
                    state.connection.candidateDTO = state.connection.dto
                }

                dialog.modal({
                    body: uploadDialogBox,
                    title: 'Choose openBIS connection',
                    buttons: {
                        'Cancel': {
                            click: onCancel
                        },
                        'Choose connection': {
                            class: 'btn-primary btn-large',
                            click: onOk
                        }
                    },
                    notebook: env.notebook,
                    keyboard_manager: env.notebook.keyboard_manager
                })
            }
        }
    }
)
