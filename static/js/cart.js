
var $iDecrement = document.querySelector('.inumber-decrement')
var $updateBtns = document.getElementsByClassName('update-cart')
var $addCartBtn = document.querySelector('.add-cart')
var $fUpdateBtn = document.querySelector('.f-cart')
var $iIncrement = document.querySelector('.number-increment')


var $priceTotal = document.querySelector('.detail-price')
if ($priceTotal) {
    var $priceProduct = +document.querySelector('.detail-price').dataset.count
}

for (i = 0; i < $updateBtns.length; i++) {
    $updateBtns[i].addEventListener('click', function (event) {

        event.preventDefault()
        var productId = this.dataset.product
        var action = this.dataset.action

        if (user === 'AnonymousUser') {
            addCookieItem(productId, action)
        } else {
            updateUserOrder(productId, action)
        }

    })
}

if ($iDecrement != null) {
    $iDecrement.addEventListener('click', function(event) {
        console.log('Idecr')
        var $updateVariable = document.querySelector('.input-number')
        var quantity = +$updateVariable.value

        if (quantity <= 0) {
            $addCartBtn.classList.remove('show')
            $addCartBtn.classList.add('hide')

            $fUpdateBtn.classList.add('show')
            $fUpdateBtn.classList.remove('hide')
        }

        if ($priceTotal != null) {
            var $nextTotal = $priceProduct * quantity
            $priceTotal.textContent = `$${$nextTotal.toFixed(2)}`
        }


    })
}

if ($iIncrement != null) {
    $iIncrement.addEventListener('click', function (event) {
        console.log('Incr')
        var $updateVariable = document.querySelector('.input-number')
        var quantity = +$updateVariable.value


        if (quantity > 0) {
            $addCartBtn.classList.remove('hide')
            $addCartBtn.classList.add('show')

            $fUpdateBtn.classList.add('hide')
            $fUpdateBtn.classList.remove('show')
        }
        
        if ($priceTotal != null) {
            var $nextTotal = $priceProduct * quantity
            $priceTotal.textContent = `$${$nextTotal.toFixed(2)}`
        }
    })
}

function addCookieItem(productId, action) {

    var $updateVariable = document.querySelector('.input-number')

    if ($updateVariable != undefined) {
        var quantity = +$updateVariable.value
    } else {
        var quantity = 1
    }

    if (action == 'add'){
        if (cart[productId] === undefined){
            cart[productId] = {'quantity': quantity}
        }else {
            cart[productId]['quantity'] += quantity
        }
    }

    if (action == 'remove'){
        cart[productId]['quantity'] -= 1

        if(cart[productId]['quantity'] <= 0){
            console.log('Remove Item')
            delete cart[productId]
        }
    }

    document.cookie = 'CART=' + JSON.stringify(cart) + ";domain=;path=/"
    document.location.reload()
}


function updateUserOrder(productId, action) {
    console.log('User is logged in, sending data..')
    var $updateVariable = document.querySelector('.input-number')

    if ($updateVariable != undefined) {
        var quantity = +$updateVariable.value
    } else {
        var quantity = 1
    }

    var url = '/update_item/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'productId': productId, 'action': action, 'quantity': quantity})
    })
        .then((response) => {
            return response.json()
        })
        .then((data) => {
            document.location.reload()
        })
    }

