function MockDropzone(category, temp_ending) {
    Dropzone.options.myDropzone = {
        init: function () {
            let myDropzone = this;

            // Create the mock file:
            let mockFile = {name: "static/uploads/" + category + "/_temp." + temp_ending, size: 217447};
            myDropzone.displayExistingFile(mockFile, "../static/uploads/" + category + "/_temp." + temp_ending);
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
