$(document).ready(function () {

    $('.increment-btn').click(function (e) {
        e.preventDefault();

        var inc_value = $(this).closest('.bottom-content').find('.qty-input').val();
        var value = parseInt(inc_value, 10);
        value = isNaN(value) ? 0 : value;

        // Get the maximum quantity available from the data attribute
        var maxQuantity = parseInt($(this).closest('.bottom-content').find('.max-quantity').val());

        if(value < maxQuantity){
            value++;
            $(this).closest('.bottom-content').find('.qty-input').val(value);
        }
    });

    $('.decrement-btn').click(function (e) {
        e.preventDefault();

        var dec_value = $(this).closest('.bottom-content').find('.qty-input').val();
        var value = parseInt(dec_value, 10);
        value = isNaN(value) ? 0 : value;
        if(value > 1){
            value--;
            $(this).closest('.bottom-content').find('.qty-input').val(value);
        }
    });

    $('.addToCart').click(function (e) {
        e.preventDefault();

        var product_id = $(this).closest('.button').find('.prod_id').val();
        var product_qty = '1';
        var token = $('input[name = csrfmiddlewaretoken]').val();

        $.ajax({
            method: "POST",
            url: "/add-to-cart",
            data : {
                'product_id' : product_id,
                'product_qty' : product_qty,
                csrfmiddlewaretoken : token
            },
            success : function (response) {
                alert(response.status)
                // alertify.success(response.status)             
            }
        });
    });

    $('.addToCartBtn').click(function (e) {
        e.preventDefault();

        var product_id = $(this).closest('.bottom-content').find('.prod_id').val();
        var product_qty = $(this).closest('.bottom-content').find('.qty-input').val();
        var token = $('input[name = csrfmiddlewaretoken]').val();

        $.ajax({
            method: "POST",
            url: "/add-to-cart",
            data : {
                'product_id' : product_id,
                'product_qty' : product_qty,
                csrfmiddlewaretoken : token
            },
            success : function (response) {
                alert(response.status)
                // alertify.success(response.status)
            }
        });
    });

    $('.addTo').click(function (e) {
        e.preventDefault();

        var inc_value = $(this).closest('.cart-single-list').find('.qty-input').val();
        var value = parseInt(inc_value, 10);
        value = isNaN(value) ? 0 : value;
        if(value < 10){
            value++;
            $(this).closest('.cart-single-list').find('.qty-input').val(value);
        }
    });

    $('.rmfrom').click(function (e) {
        e.preventDefault();

        var dec_value = $(this).closest('.cart-single-list').find('.qty-input').val();
        var value = parseInt(dec_value, 10);
        value = isNaN(value) ? 0 : value;
        if(value > 1){
            value--;
            $(this).closest('.cart-single-list').find('.qty-input').val(value);
        }
    });

    $('.qty-input').change(function (e) {
        e.preventDefault();
    
        var inputField = $(this);
        var product_id = inputField.closest('tr').find('.prod_id').val();
        var product_qty = parseInt(inputField.val(), 10);
        var token = $('input[name=csrfmiddlewaretoken]').val();
    
        // Retrieve the available stock from the hidden input field with the class "stock"
        var availableStock = parseInt(inputField.closest('tr').find('.stock').val(), 10);
    
        if (product_qty > availableStock) {
            alert('Quantity exceeds available stock');
            // Reset the input field to the available stock value
            inputField.val(availableStock);
            return;
        }
    
        $.ajax({
            method: "POST",
            url: "/update-cart",
            data: {
                'product_id': product_id,
                'product_qty': product_qty,
                csrfmiddlewaretoken: token
            },
            success: function (response) {
                // Show an alert to the user
                alert('Quantity updated successfully');
    
                // Update the quantity in the HTML page
                inputField.closest('tr').find('.quantity').val(product_qty);
            },
            error: function (error) {
                alert('Error updating quantity: ' + error.responseJSON.message);
                // You may want to reset the input field to the previous value in case of an error
            }
        });
    });
    
    // Function to update the total price when input field values change
    function updateTotalPrice() {
        var rows = document.querySelectorAll('.content');
        rows.forEach(function (row) {
        var priceElement = row.querySelector('.price');
        var qtyInput = row.querySelector('.qty-input');
        var totalCell = row.querySelector('.total');
        
        var price = parseFloat(priceElement.value); // Get the price from the "price" input
        var quantity = parseFloat(qtyInput.value); // Get the quantity from the "qty-input" input
        
        if (!isNaN(price) && !isNaN(quantity)) {
            var total = price * quantity; // Calculate the total price
            totalCell.textContent = 'NGN ' + total.toLocaleString(); // Update the total cell with formatted total
        }
        });
    }

    // Add event listeners to input fields to update the total price in real-time
    var qtyInputs = document.querySelectorAll('.qty-input');
    qtyInputs.forEach(function (input) {
        input.addEventListener('input', updateTotalPrice);
    });

    // Initial calculation
    updateTotalPrice();
    
    // Function to calculate the subtotal
    function calculateSubtotal() {
        var rows = document.querySelectorAll('.content');
        var subtotal = 0;

        rows.forEach(function (row) {
        var totalCell = row.querySelector('.total');
        var total = parseFloat(totalCell.textContent.replace('NGN ', '').replace(/,/g, ''));

        if (!isNaN(total)) {
            subtotal += total; // Add the total for this row to the subtotal
        }
        });

        var subtotalElement = document.querySelector('.subtotal');
        if (subtotalElement) {
        subtotalElement.textContent = 'NGN ' + subtotal.toLocaleString(); // Display the formatted subtotal
        }
    }

    // Initial calculation
    calculateSubtotal();

    $(document).on('click', '.remove-item', function (e) {
        e.preventDefault();

        var productRow = $(this).closest('tr');
        var product_id = productRow.find('.prod_id').val();
        var token = $('input[name = csrfmiddlewaretoken]').val();

        $.ajax({
            method: "POST",
            url: "/delete-cart-item",
            data : {
                'product_id' : product_id,
                csrfmiddlewaretoken : token
            },
            success : function (response) {
                alert(response.status)

                setTimeout(function () {
                    location.reload();
                }, 1000);

                // alertify.success(response.status);
                // $('.content').load(location.href + " .content");
            }
        })
    });

    $('.addToWish').click(function (e) {
        e.preventDefault();

        var product_id = $(this).closest('.bottom-content').find('.prod_id').val();
        var token = $('input[name = csrfmiddlewaretoken]').val();

        $.ajax({
            method: "POST",
            url: "/add-to-wishlist",
            data : {
                'product_id' : product_id,
                csrfmiddlewaretoken : token
            },
            success : function (response) {
                alert(response.status)
                // alertify.success(response.status)
                $('.shopping-cart').load(location.href + " .shopping-cart");
            }
        })
    });

    $(document).on('click', '.deletewish', function (e) {
        e.preventDefault();

        var product_id = $(this).closest('.cart-single-list').find('.prod_id').val();
        var token = $('input[name = csrfmiddlewaretoken]').val();

        $.ajax({
            method: "POST",
            url: "/deletewish",
            data : {
                'product_id' : product_id,
                csrfmiddlewaretoken : token
            },
            success : function (response) {
                alert(response.status)
                // alertify.success(response.status)
                $('.shopping-cart').load(location.href + " .shopping-cart");
                $('.middle-right-area').load(location.href + " .middle-right-area");

            }
        })
    });

});
