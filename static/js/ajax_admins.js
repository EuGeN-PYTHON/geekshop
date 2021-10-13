window.onload = function() {
    $('.button_delete').on('click', 'button[type="submit"]', (e) => {
        let href = e.target;
        console.log(href.name);
        let csrf = $('meta[name="csrf_token"]').attr('content');

        $.ajax({
            type: 'DELETE',
            headers: {"X-CSRFToken": csrf},
            url: '/admins/category-delete/'+href.name +'/',
            success: (data) => {
                if (data) {
                    $('.admin_category_is_active').html(data.result)
                }
            },
        });
        e.preventDefault()
    });
};