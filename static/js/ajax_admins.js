window.onload = function () {
    $('.button_delete').on('click', 'button[type="submit"]', (e) => {
        $(document).on('click', '.button_delete', (e) => {
            let href = e.target;
            console.log(href.name);
            let csrf_token = $('meta[name="csrf-token"]').attr('content');
            console.log(csrf_token);

            $.ajax({
                type: 'POST',
                headers: {"X-CSRFToken": csrf_token},
                url: '/admins/category-delete/' + href.name + '/',
                success: (data) => {
                    if (data) {
                        $('.admin_category_is_active').html(data.result)
                    }
                },
            });
            e.preventDefault()
        });
    });
};