// disable Devtools
// const disableDevtools = callback => {
// 	const original = Object.getPrototypeOf;
// 	Object.getPrototypeOf = (...args) => {
//         if (Error().stack.includes("getCompletions")) callback();
//         return original(...args);
// 	};
// };
// disableDevtools(() => {
// 	console.error("devtools has been disabled");
// 	while (1);
// });

// reverse string
function reverseString(str) { return str.split('').reverse().join(''); }

// jQuery parser after doument loads
$(function () {
    // dialog
    if ($('#item').length > 0) {
        $('#item').on('show.bs.modal', function (event) {
            // Button that triggered the modal
            var button = $(event.relatedTarget);
            // Extract info from data-* attributes
            var cat = button.data('catagory'),
                item = button.data('item'),
                modal = $(this);
            // initiate an AJAX request
            // ` and then do the updating in a callback.
            $.get(
                // get dynamic data from api
                '/api/json/category/'+ cat +'/item/'+ item +'/',
                function( data ) {
                    // Update the modal's content on success
                    modal.find('#itemTitle').html(data.name +
                        ' <sub class="text-muted">('
                        + data.catagory + ')</sub>');
                    modal.find('.modal-body').text(data.description);
                    modal.find('#l_update').text(data.last_update.pdate);
                    modal.find('#iEdit').attr('href',
                        '/edit/'+ cat +'/item/'+ item +'/');
                    modal.find('#iDelete').attr('href',
                        '/delete/'+ cat +'/item/'+ item +'/');
            });
        })
    }

    if ($('#Catagory').length > 0) {
        $('#Catagory').on('show.bs.modal', function (event) {
            // Button that triggered the modal
            var button = $(event.relatedTarget);
            // Extract info from data-* attributes
            var cat = button.data('name'),
                id = button.data('id'),
                exec = button.data('exec'),
                modal = $(this);
            modal.find('#cat_name').val(cat);
            modal.find('#cat_id').val(id);
            modal.find('#form_catagory').attr('action', exec);
        })
    }

    if ($('#hide-this')) {
        interval = setInterval(() => {
            var div = $('#hide-this'),
                chide = div.find('#hide-counter'),
                count = parseInt(chide.text()) - 1;
            chide.text(count);
            if (count <= 0) {
                div.fadeOut(1500);
                clearInterval(interval);
            }
        }, 1000);
    }

    if ($('.new-Catagory')) {
        $('.new-Catagory').click(() => {
            setTimeout(() => { $('#cat_name').focus(); }, 500);
        })
    }

});
