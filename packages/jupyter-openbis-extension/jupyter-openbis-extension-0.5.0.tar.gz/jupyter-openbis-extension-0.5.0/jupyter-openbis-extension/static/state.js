define([],
    function () {
        // noinspection JSAnnotator
        return {
            // connection dialog
            connection: {
                name: null,
                dto: null,
                candidateName: null,
                candidateDTO: null
            },
            working_dir: null,
            working_dir_element: null,
            download_dir: null,

            // upload dialog
            uploadDataSetType: null,
            uploadDataSetTypes: {},
            uploadEntity: null,
            datasetCheckboxes: [],
            fileCheckboxes: [],
            selectedFiles: [],
            unselectedDatasets: [],

            // download dialog
            selectedDatasets: new Set([]),
            entity: null,

            // openBIS v3 connection
            openbisService : null,

            //runtime environment (e.g. Python version) and requirements (package list)

            requirements_list : null,
            requirements_filename : null,
            runtime_filename : null,
            runtime : null

        }
    }
)