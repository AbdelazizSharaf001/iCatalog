$(function () {
    if ($('#api_view').length > 0) {
        $('#api_view').on('show.bs.modal', function (event) {
            // Button that triggered the modal
            var button = $(event.relatedTarget);
            // Extract info from data-* attributes
            var text = button.text(),
                exec = button.data('exec'),
                lnk = exec,
                c_id = $('#c_id').val(),
                i_id = $('#i_id').val(),
                modal = $(this);

            // modify link if needed
            lnk = lnk.replace('/1/', '/' + c_id + '/');
            lnk = lnk.replace('/2/', '/' + i_id + '/');
            exec = exec.replace('/1/', '/CATAGORY_ID/');
            exec = exec.replace('/2/', '/ITEM_ID/');

            // reset model data
            modal.find('.modal-title').text('END_POINT_NAME');
            modal.find('.modal-body').text('...');
            modal.find('#api_l').text('...');
            modal.find('#api_s').text('...');

            // replacer
            replacer = (key, value) => {
                if (typeof value === 'Number') {
                    return str(value);
                }
                return value;
            }

            // initiate an AJAX request
            // ` and then do the updating in a callback.
            $.get(
                // get dynamic data from api
                lnk,
                function( data ) {
                    // Update the modal's content on success
                    modal.find('.modal-title').text(text);
                    modal.find('.modal-body').text(
                        JSON.stringify(data, replacer, 4)
                    );
                    modal.find('#api_l').text(lnk);
                    modal.find('#api_s').text(exec);
            });
        })
	}
});