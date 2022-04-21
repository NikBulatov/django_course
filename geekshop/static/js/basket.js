window.onload = function (){ // перед загрузкой DOM
    // $ обращение к div ('.basket_list') при клике на объект input, e которого тип number
    $('.basket_list').on('click','input[type="number"]', function (){

        let t_href = event.target; // то, что выделили (нажали)
        console.log(t_href.name,t_href.value);  // вывести в консоль результат (ID, quantity)

        $.ajax(
            {
                // url из path          ID                     quantity
                url:"/basket/edit/" + t_href.name + "/" + t_href.value+ "/", //
                success: function (data){ // обработка при success
                    // данные с backend
                    $('.basket_list').html(data.result)  // data.result - это html код из basket/views render_to_string
                // error: function (data) { $(...)}
                }
            }
        )
    })

    $('.card_add_basket').on('click','button[type="button"]', function (){

        let t_href = event.target.value; // id объекта
        console.log(t_href);

        $.ajax(
            {
                url:"/basket/add/" + t_href + "/",
                success: function (data){
                    $('.card_add_basket').html(data.result)
                }
            }
        )

    })
}