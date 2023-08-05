define(["jquery", "./jquery-select2/js/select2.min"],
    function($, select2) {
        return {
            loadResource(pathToResource, jsOrCss, onLoad) {
                var resource = null

                if (jsOrCss === 'js') {
                    resource = document.createElement('script')
                    resource.type = 'text/javascript'
                    resource.src = pathToResource
                }

                if (jsOrCss === 'css') {
                    resource = document.createElement('link')
                    resource.type = 'text/css'
                    resource.rel = 'stylesheet'
                    resource.href = pathToResource
                }

                resource.onload = onLoad
                resource.onreadystatechange = function() {
                    if (this.readyState == 'complete') {
                        onLoad()
                    }
                }

                var head = document.getElementsByTagName('head')[0]
                head.appendChild(resource)
            },
            getRequireJSV3Config(baseURL) {
                return {
                    baseUrl: baseURL + "/openbis/resources/api/v3",
                    paths: {
                        "stjs": "lib/stjs/js/stjs",
                        "underscore": "lib/underscore/js/underscore",
                        "moment": "lib/moment/js/moment"
                    },
                    shim: {
                        "stjs": {
                            exports: "stjs",
                            deps: ["underscore"]
                        },
                        "underscore": {
                            exports: "_"
                        }
                    }
                }
            },
            getEntitySearcherForDownload(state) {
                return this.getEntitySearcher(state, false)
            },
            getEntitySearcherForUpload(state) {
                return this.getEntitySearcher(state, true)
            },
            getEntitySearcher(state, upload) {
                var _this = this
                var connection_name = state.connection.name
                if (!connection_name) {
                    alert('Please choose a connection')
                    return false
                }

                var element = document.createElement("SPAN")
                element.innerHTML = "<span style='color:orange;margin:5px'>loading...</span>"
                if (!state.openbisService) {
                    require.config(this.getRequireJSV3Config(state.connection.dto.url))
                    require(["openbis", "as/dto/experiment/search/ExperimentSearchCriteria",
                        "as/dto/experiment/fetchoptions/ExperimentFetchOptions",
                        "as/dto/sample/search/SampleSearchCriteria",
                        "as/dto/sample/fetchoptions/SampleFetchOptions"],

                        function (openbis) {
                        var apiUrl = state.connection.dto.url + "/openbis/openbis/rmi-application-server-v3.json"
                        var v3 = new openbis(apiUrl)
                        v3.login(state.connection.dto.username, state.connection.dto.password)
                            .done(function (sessionToken) {
                                console.log("sessionToken heisst:");
                                console.log(sessionToken);
                                state.openbisService = v3
                                var userName = window.location.pathname.split("/")[2];
                                //_this.loadResource('/user/' + userName+ '/nbextensions/jupyter-openbis-extension/jquery-select2/css/select2.min.css', 'css', function() {
                                _this.createDropdown(element, state, upload)
                                //})
                            })
                            .fail(function (result) {
                                alert('openbis v3 service login failed for ' + apiUrl
                                + " : property 'trusted-cross-origin-domains' is probably not set in service.properties.")
                        })
                    },
                    function (err){
                        alert('failed to load required libraries')
                    })
                }
                else {
                    _this.createDropdown(element, state, upload)
                }

                return element
            },
            createDropdown(container, state, upload) {
                var _this = this
                var $select = $("<select>", {class : 'form-control'})
                $select.attr("multiple", "multiple")
                $select.attr("required", "required")

                container.innerHTML = null
                $select.each(function() {
                    container.appendChild(this)
                })
                $select.select2({
                    width: upload ? '100%' : '80%', 
                    maximumSelectionLength: 1,
                    minimumInputLength: 2,
                    placeholder : "Entity identifier/permId",
                    ajax: {
                        delay: 1000,
                        processResults: function (data) {
                            var results = []

                            for(var dIdx = 0; dIdx < data.length; dIdx++) {
                                var group = {
                                        text: data[dIdx].type, 
                                        children : []
                                }

                                var entities = data[dIdx].objects
                                for (var eIdx = 0; eIdx < entities.length; eIdx++) {
                                    group.children.push({
                                        id : entities[eIdx].permId.permId,
                                        text : _this.getDisplayName(entities[eIdx]),
                                        data : {
                                            id : entities[eIdx].permId.permId,
                                            text : _this.getDisplayName(entities[eIdx]),
                                            data : entities[eIdx]
                                        }
                                    })
                                }

                                if (entities.length > 0) {
                                    results.push(group)
                                }
                            }

                            return {
                                "results": results,
                                "pagination": {
                                    "more": false
                                }
                            }
                        },
                        transport: function (params, success, failure) {
                            var searchResults = []
                            _this.searchExperiments(state, params, function(result) {
                                searchResults.push(result)
                                _this.searchSamples(state, params, function(result) {
                                    searchResults.push(result)
                                    success(searchResults)
                                })
                            })
                            return {
                                abort : function () { /* Not implemented */ }
                            }
                        }
                    }
                })
                $select.on("select2:select", function() {
                    if (upload) {
                        state.uploadEntity = _this.getSelected($select)[0]
                    } else {
                        state.entity = _this.getSelected($select)[0]
                    }
                })
                if (upload && state.uploadEntity) {
                    _this.addSelected($select, state.uploadEntity)
                } else if (upload == false && state.entity) {
                    _this.addSelected($select, state.entity)
                }
            },
            searchExperiments(state, params, action) {
                var ExperimentSearchCriteria = require("as/dto/experiment/search/ExperimentSearchCriteria")
                var searchCriteria = new ExperimentSearchCriteria().withOrOperator()
                searchCriteria.withCode().thatContains(params.data.q)
                searchCriteria.withProperty("$NAME").thatContains(params.data.q)
                var ExperimentFetchOptions = require("as/dto/experiment/fetchoptions/ExperimentFetchOptions")
                var fetchOptions = new ExperimentFetchOptions()
                fetchOptions.withProperties()
                state.openbisService.searchExperiments(searchCriteria, fetchOptions).done(action)
            },
            searchSamples(state, params, action) {
                var SampleSearchCriteria = require("as/dto/sample/search/SampleSearchCriteria")
                var searchCriteria = new SampleSearchCriteria().withOrOperator()
                searchCriteria.withCode().thatContains(params.data.q)
                searchCriteria.withProperty("$NAME").thatContains(params.data.q)
                var SampleFetchOptions = require("as/dto/sample/fetchoptions/SampleFetchOptions")
                var fetchOptions = new SampleFetchOptions()
                fetchOptions.withProperties()
                state.openbisService.searchSamples(searchCriteria, fetchOptions).done(action)
            },
            getDisplayName(entity) {
                var text = ""
                var propertyReplacingCode = "$NAME"
                if (entity.identifier && entity.identifier.identifier) {
                    text = entity.identifier.identifier
                }
                if (entity.properties && entity.properties[propertyReplacingCode]) {
                    text += " (" + entity.properties[propertyReplacingCode] + ")"
                }
                return text
            },
            getSelected($select) {
                var selected = $select.select2('data')
                var entities = []
                for (var eIdx = 0; eIdx < selected.length; eIdx++) {
                    if (selected[eIdx].data) {
                        entities.push(selected[eIdx].data.data)
                    }
                    if (selected[eIdx].element.data) {
                        entities.push(selected[eIdx].element.data.data)
                    }
                }
                return entities
            },
            addSelected($select, v3entity) {
                var text = this.getDisplayName(v3entity)
                var id = null
                if (v3entity.permId && v3entity.permId.permId) { //Only v3 objects supported
                    id = v3entity.permId.permId
                } else {
                    throw {
                        name: "NonV3ObjectException",
                        message: "Object without v3 permId",
                        toString: function() {
                            return this.name + ": " + this.message
                        }
                    }
                }
                
                var data = {
                        id : id,
                        text : text,
                        data : v3entity
                }
                
                var newOption = new Option(text, id, true, true)
                newOption.data = data
                $select.append(newOption).trigger('change')
            }
        }
    }
)
