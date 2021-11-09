$(document).ready(function(){
    $('#addUserModal').on('show.bs.modal', function (event) {
        $('#cancel_button').on('click', function (e) {
            $('#addUserModal').modal('toggle');
            return false;
        });
        $('#addRegister_button').on('click', function (e){
            // Create Applicant
            let params = {};
            $.each($('#register_employee').serializeArray(), function (index, value) {
                params[value.name] = params[value.name] ? params[value.name] || value.value : value.value;
            });
            let form_data = new FormData();
            for(let key in params){
                form_data.append(key, params[key]);
            }
            form_data.append('resume', $("#resume")[0].files[0]);
            console.log(form_data)
            $.ajax({
                type: 'post',
                url: "create",
                data: form_data,
                processData: false,
                contentType: false,
                cache: false,
                success: function (response) {
                    console.log(response);
                    if(response.status_code){
                        window.location.href = response.url;
                    }
                }
            });
            e.preventDefault();
        });

    });

});
