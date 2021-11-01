window.addEventListener("load", () => {
    $('.basket_list').on('click', 'input[type="number"]', (e) => {
        let href = e.target;
        console.log(href.name);
        console.log(href.value);

        $.ajax({
            url: '/baskets/edit/'+href.name+'/'+href.value+'/',
            success: function (data){
                $('.basket_list').html(data.result)
            },
        });
        e.preventDefault()
    });


    $('.product_items').on('click', 'button[type="submit"]', (e) => {
        let href = e.target;
        console.log(href.name);

        $.ajax({
            url: '/baskets/add/'+href.name+'/',
        // //     // headers: {'X-CSRFToken': csrftoken},
        // //     // method: 'POST',
            success: function (data){
                $('.product_items').html(data.result)
            },
        });
        e.preventDefault()
    });

});