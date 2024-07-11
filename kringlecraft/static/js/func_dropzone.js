function MockDropzone(mock_file) {
    Dropzone.options.myDropzone = {
        init: function () {
            let myDropzone = this;

            // Create the mock file:
            let mockFile = {name: "static/uploads/" + mock_file, size: 217447};
            myDropzone.displayExistingFile(mockFile, "../static/uploads/" + mock_file);
        }
    };
}

function QueueDropzone(csrf_token, action_url, input_name) {
    Dropzone.options.myDropzone = {
        headers: {
            'X-CSRF-TOKEN': csrf_token
        },
        init: function () {
            this.on("queuecomplete", function (file) {
                // Get the content of the textarea
                var challengeContent = easyMDE.value();

                // Create a form and submit it
                var form = document.createElement('form');
                form.method = 'POST';
                form.action = action_url;

                var input = document.createElement('input');
                input.type = 'hidden';
                input.name = input_name;
                input.value = challengeContent;

                var csrfInput = document.createElement('input');
                csrfInput.type = 'hidden';
                csrfInput.name = 'csrf_token';
                csrfInput.value = csrf_token;

                form.appendChild(input);
                form.appendChild(csrfInput);
                document.body.appendChild(form);
                form.submit();
            });
        }
    };
}

function QueueDropzone_World(csrf_token, action_url) {
    Dropzone.options.myDropzone = {
        headers: {
            'X-CSRF-TOKEN': csrf_token
        },
        init: function () {
            this.on("queuecomplete", function (file) {
                // Create a form and submit it
                let form = document.createElement('form');
                form.method = 'POST';
                form.action = action_url;

                let input_name = document.createElement('input');
                input_name.type = 'hidden';
                input_name.name = 'name';
                input_name.value = document.getElementById('name').value;

                let input_description = document.createElement('input');
                input_description.type = 'hidden';
                input_description.name = 'description';
                input_description.value = document.getElementById('description').value;

                let input_visible = document.createElement('input');
                input_visible.type = 'hidden';
                input_visible.name = 'visible';
                input_visible.value = document.getElementById('visible').value;

                let input_url = document.createElement('input');
                input_url.type = 'hidden';
                input_url.name = 'url';
                input_url.value = document.getElementById('url').value;

                let input_archived = document.createElement('input');
                input_archived.type = 'hidden';
                input_archived.name = 'archived';
                input_archived.value = document.getElementById('archived').value;

                let input_csrf = document.createElement('input');
                input_csrf.type = 'hidden';
                input_csrf.name = 'csrf_token';
                input_csrf.value = document.getElementById('csrf_token').value;

                form.appendChild(input_name);
                form.appendChild(input_description);
                form.appendChild(input_visible);
                form.appendChild(input_url);
                form.appendChild(input_archived);
                form.appendChild(input_csrf);
                document.body.appendChild(form);
                form.submit();
            });
        }
    };
}

function QueueDropzone_Room(csrf_token, action_url) {
    Dropzone.options.myDropzone = {
        headers: {
            'X-CSRF-TOKEN': csrf_token
        },
        init: function () {
            this.on("queuecomplete", function (file) {
                // Create a form and submit it
                let form = document.createElement('form');
                form.method = 'POST';
                form.action = action_url;

                let input_name = document.createElement('input');
                input_name.type = 'hidden';
                input_name.name = 'name';
                input_name.value = document.getElementById('name').value;

                let input_description = document.createElement('input');
                input_description.type = 'hidden';
                input_description.name = 'description';
                input_description.value = document.getElementById('description').value;

                let input_world = document.createElement('input');
                input_world.type = 'hidden';
                input_world.name = 'world';
                input_world.value = document.getElementById('world').value;

                let input_csrf = document.createElement('input');
                input_csrf.type = 'hidden';
                input_csrf.name = 'csrf_token';
                input_csrf.value = document.getElementById('csrf_token').value;

                form.appendChild(input_name);
                form.appendChild(input_description);
                form.appendChild(input_world);
                form.appendChild(input_csrf);
                document.body.appendChild(form);
                form.submit();
            });
        }
    };
}

function QueueDropzone_Objective(csrf_token, action_url) {
    Dropzone.options.myDropzone = {
        headers: {
            'X-CSRF-TOKEN': csrf_token
        },
        init: function () {
            this.on("queuecomplete", function (file) {
                // Create a form and submit it
                let form = document.createElement('form');
                form.method = 'POST';
                form.action = action_url;

                let input_name = document.createElement('input');
                input_name.type = 'hidden';
                input_name.name = 'name';
                input_name.value = document.getElementById('name').value;

                let input_description = document.createElement('input');
                input_description.type = 'hidden';
                input_description.name = 'description';
                input_description.value = document.getElementById('description').value;

                let input_difficulty = document.createElement('input');
                input_difficulty.type = 'hidden';
                input_difficulty.name = 'difficulty';
                input_difficulty.value = document.getElementById('difficulty').value;

                let input_visible = document.createElement('input');
                input_visible.type = 'hidden';
                input_visible.name = 'visible';
                input_visible.value = document.getElementById('visible').value;

                let input_type = document.createElement('input');
                input_type.type = 'hidden';
                input_type.name = 'type';
                input_type.value = document.getElementById('type').value;

                let input_room = document.createElement('input');
                input_room.type = 'hidden';
                input_room.name = 'room';
                input_room.value = document.getElementById('room').value;

                let input_csrf = document.createElement('input');
                input_csrf.type = 'hidden';
                input_csrf.name = 'csrf_token';
                input_csrf.value = document.getElementById('csrf_token').value;

                form.appendChild(input_name);
                form.appendChild(input_description);
                form.appendChild(input_difficulty);
                form.appendChild(input_visible);
                form.appendChild(input_type);
                form.appendChild(input_room);
                form.appendChild(input_csrf);
                document.body.appendChild(form);
                form.submit();
            });
        }
    };
}
