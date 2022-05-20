window.onload = function () {
    let quantity, price, orderItemNum, deltaQuantity, orderItemQuantity, deltaCost;

    const orderTotalCostSelector = $('.order_total_cost');
    const orderTotalQuantitySelector = $('.order_total_quantity');
    const orderFormSelector = $('.order_form');

    let quantityArray = [];
    let priceArray = [];

    let totalForms = parseInt($('input[name=orderitems-TOTAL_FORMS]').val())

    let orderTotalCost = parseInt(orderTotalCostSelector.text().replace(',', '.')) || 0; // либо текст, либо 0
    let orderTotalQuantity = parseInt(orderTotalQuantitySelector.text()) || 0

    for (let i = 0; i < totalForms; i++) {
        quantity = parseInt($(`input[name=id_ordertems-${i}-quantity]`).val());
        price = parseInt($(`.orderitems-${i}-price`).text().replace(',', '.'));
        quantityArray[i] = quantity;
        if (price) {
            priceArray[i] = price;
        } else {
            priceArray[i] = null;
        }
    }

    console.log(totalForms, orderTotalCost, orderTotalQuantity);  // отладка
    console.info('QUANTITY', quantityArray);  // отладка
    console.info('PRICE', priceArray);  // отладка

    // 1 method обновления суммы и количества при инкременте
    orderFormSelector.on('click', 'input[type=number]', function () { // при клике на блок с формой
        let target = event.target; // input элемент
        console.log(target);
        orderItemNum = parseInt(target.name.replace('orderitems-', '').replace('-quantity', ''));
        if (priceArray[orderItemNum]) {
            orderItemQuantity = parseInt(target.value);
            deltaQuantity = orderItemQuantity - quantityArray[orderItemNum];
            quantityArray[orderItemNum] = orderItemQuantity;
            orderSummaryUpdate(priceArray[orderItemNum], deltaQuantity);
        }
    })

    // 2 method - при удалении
    orderFormSelector.on('click', 'input[type=checkbox]', function () { // при клике на место для галочки
        let target = event.target; // input элемент
        console.log(target);
        orderItemNum = parseInt(target.name.replace('orderitems-', '').replace('-DELETE', ''));
        if (target.checked) {
            deltaQuantity = -quantityArray[orderItemNum]
        } else {
            deltaQuantity = quantityArray[orderItemNum]
        }
    })


    function orderSummaryUpdate(orderItemPrice, deltaQuantity) {
        deltaCost = orderItemPrice * deltaQuantity;
        orderTotalCost = Number((orderTotalCost + deltaCost).toFixed(2));
        orderTotalQuantity += deltaQuantity;
        $('.order_total_cost').html(orderTotalCost.toString());
        $('.order_total_quantity').html(orderTotalQuantity.toString() + ',00');

    }

    $('.formset-row').formset({
        addText: 'Add product',
        deleteText: 'Delete product',
        prefix: 'orderItems',
        removed: deleteOrderItem
    })

    function deleteOrderItem(row) {
        let targetName = row[0].querySelector('input[type=nubmer]').name;
        console.log(targetName);
        orderItemNum = parseInt(targetName.replace('orderitems-', '').replace('-quantity', ''));
        deltaQuantity = -quantityArray[orderItemNum];
        orderSummaryUpdate(priceArray[orderItemNum], deltaQuantity);

    }

    $(document).on('change','.order_form select',function (){
    // $('.order_form select').change(function () {

        let target = event.target
        orderItemNum = parseInt(target.name.replace('orderitems-', '').replace('-product', ''));
        console.log(target)
        let orderItemProductPK = target.options[target.selectedIndex].value;

        if (orderItemProductPK) {
            $.ajax({
                url: '/orderapp/product/' + orderItemProductPK + '/price/',
                success: function (data) {
                    let price_html = '<span class="orderitems-' + orderItemNum + '-price">'
                        + data.price.toString().replace('.', ',') + '</span> руб';

                    let current_tr = $('.order_form table').find('tr:eq('+(orderItemNum+1)+')');
                    current_tr.find('td:eq(2)').html(price_html)
                }
            })
        }


    })
};