window.onload = function(){
    $('.basket_list').on('click', 'input[type="number"]',function (){
        let href = event.target;
        console.log(href.name);
        console.log(href.value);

        $.ajax({
            url: '/baskets/edit/'+href.name+'/'+href.value+'/',
            success: function (data){
                $('.basket_list').html(data.result)
            },
        });
        event.preventDefault()
    });
};