$(document).ready(function () {

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

    // $('.addTo').click(function (e) {
    //     e.preventDefault();

    //     var inc_value = $(this).closest('.cart-single-list').find('.qty-input').val();
    //     var value = parseInt(inc_value, 10);
    //     value = isNaN(value) ? 0 : value;
    //     if(value < 10){
    //         value++;
    //         $(this).closest('.cart-single-list').find('.qty-input').val(value);
    //     }
    // });

    // $('.rmfrom').click(function (e) {
    //     e.preventDefault();

    //     var dec_value = $(this).closest('.cart-single-list').find('.qty-input').val();
    //     var value = parseInt(dec_value, 10);
    //     value = isNaN(value) ? 0 : value;
    //     if(value > 1){
    //         value--;
    //         $(this).closest('.cart-single-list').find('.qty-input').val(value);
    //     }
    // });

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
        var availableStock = parseFloat(row.querySelector('.stock').value); // Get the available stock
    
        if (!isNaN(price) && !isNaN(quantity)) {
            var lastKnownQuantity = parseFloat(qtyInput.dataset.lastQuantity); // Get the last known quantity
    
            // Calculate and display the total price based on the last known quantity
            var total = price * lastKnownQuantity;
            totalCell.textContent = 'NGN ' + total.toLocaleString();
    
            if (quantity > availableStock) {
            // Quantity exceeds available stock, reset the quantity to the last known quantity
            qtyInput.value = lastKnownQuantity;
            } else {
            // Update the last known quantity
            qtyInput.dataset.lastQuantity = quantity;
            // Calculate and display the total price based on the updated quantity
            total = price * quantity;
            totalCell.textContent = 'NGN ' + total.toLocaleString();
            }
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
  
    // Function to calculate the subtotal and update the total in real-time
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
        var pay = document.querySelector('.pay');
        var input = document.querySelector('.pay-input');
        if (subtotalElement) {
            var formattedSubtotal = 'NGN ' + subtotal.toLocaleString(); // Formatted subtotal
            subtotalElement.textContent = formattedSubtotal; // Display the formatted subtotal
            pay.textContent = formattedSubtotal; // Assign the same formatted subtotal to the element with class "pay"

            // Update the value in the input element
            var cleanValue = pay.textContent.replace('NGN ', '').replace(/,/g, '');
            input.value = cleanValue;
        }
    }
    
    // Initial calculation
    calculateSubtotal();
    
    // Add event listeners to input fields to update the subtotal in real-time
    var qtyInputs = document.querySelectorAll('.qty-input');
    qtyInputs.forEach(function (input) {
        input.addEventListener('input', calculateSubtotal);
    });
    
    $(document).ready(function() {
        $('.applyCoupon').click(function() {
            var couponCode = $('#coupon').val();
            var token = $('input[name=csrfmiddlewaretoken]').val();
    
            $.ajax({
                type: 'POST',
                url: '/validate_coupon',
                data: { coupon: couponCode,
                    csrfmiddlewaretoken: token
                },
                success: function(data) {
                    if (data.error) {
                        alert(data.error);
                    } else {
                        var discount = parseFloat(data.discount) / 100;
                        var subtotalElement = $('.subtotal');
                        var subtotal = parseFloat(subtotalElement.text().replace('NGN', '').replace(/,/g, ''));
    
                        if (!isNaN(discount) && !isNaN(subtotal)) {
                            var discountAmount = discount * subtotal;
                            var newTotal = subtotal - discountAmount;
                            
                            // Calculate savings
                            var saved = subtotal - newTotal;
    
                            // Display the discount and savings
                            $('#discountApplied').text('Discount: NGN ' + discountAmount.toFixed(2));
                            $('#discountApplied').show();
                            $('.saved').text('Saved: NGN ' + saved.toLocaleString());

                            // Update the total price to pay in .badge-light and .pay-value
                            var formattedTotal = 'NGN ' + newTotal.toLocaleString();
                            $('.badge-light').text(formattedTotal);
                            $('#pay-input').val(formattedTotal.replace('NGN', '').replace(/,/g, ''));
                        }
                    }
                },
                error: function() {
                    alert('An error occurred while applying the coupon.');
                }
            });
        });
    });

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
                }, 100);

                // alertify.success(response.status);
                // $('.content').load(location.href + " .content");
            }
        })
    });

    // $('.addToWish').click(function (e) {
    //     e.preventDefault();

    //     var product_id = $(this).closest('.bottom-content').find('.prod_id').val();
    //     var token = $('input[name = csrfmiddlewaretoken]').val();

    //     $.ajax({
    //         method: "POST",
    //         url: "/add-to-wishlist",
    //         data : {
    //             'product_id' : product_id,
    //             csrfmiddlewaretoken : token
    //         },
    //         success : function (response) {
    //             alert(response.status)
    //             // alertify.success(response.status)
    //             $('.shopping-cart').load(location.href + " .shopping-cart");
    //         }
    //     })
    // });

    // $(document).on('click', '.deletewish', function (e) {
    //     e.preventDefault();

    //     var product_id = $(this).closest('.cart-single-list').find('.prod_id').val();
    //     var token = $('input[name = csrfmiddlewaretoken]').val();

    //     $.ajax({
    //         method: "POST",
    //         url: "/deletewish",
    //         data : {
    //             'product_id' : product_id,
    //             csrfmiddlewaretoken : token
    //         },
    //         success : function (response) {
    //             alert(response.status)
    //             // alertify.success(response.status)
    //             $('.shopping-cart').load(location.href + " .shopping-cart");
    //             $('.middle-right-area').load(location.href + " .middle-right-area");

    //         }
    //     })
    // });

});
