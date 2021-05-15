const csrftoken = getCookie('csrftoken');
const updatebtn = document.getElementsByClassName('update-cart')

// Update secret page ajax
const secretForm = document.getElementById('secret-form')
const secretBox = document.getElementById('secret-box')
const secretText = document.getElementById('secret-text')

function getCookie(name) {
	let cookieValue = null;
	if (document.cookie && document.cookie !== '') {
		const cookies = document.cookie.split(';');
		for (let i = 0; i < cookies.length; i++) {
			const cookie = cookies[i].trim();
			if (cookie.substring(0, name.length + 1) === (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}

for(var i=0; i<updatebtn.length; i++) {
	updatebtn[i].addEventListener('click', function() {
		var product_id = this.dataset.product;
		var action = this.dataset.action;
		if('{{request.user}}' !== "AnonymousUser"){
			updateCart(product_id, action)
		}
	})
}

function updateCart(product_id, action) {
	$.ajax({
		type:'POST',
		url:'/updateCart/',
		headers:{
			'X-CSRFToken':csrftoken,
		},
		data:{
			'product_id':product_id,
			'action':action,
		},
		success: function(response){
			action = response['action'];
			product_id = response['product_id'];
			quantity = response['quantity'];
			itemTotal = response['itemTotal'];
			orderTotal = response['orderTotal'];
			orderCount = response['orderCount'];
			// add operation
			if(action == "add") {
				var productQuantity = document.getElementById(product_id+"-quantity");
				var productParent = document.getElementById(product_id+"-product");
				var productTotalCount = document.getElementById(product_id+"-cart-count");
				// product page ajax for add
				if(productQuantity != null && productParent != null) {
					productQuantity.textContent = "In Cart:"+quantity;
				}
				else if(productQuantity == null && productParent != null) {
					var obj = document.createElement('div');
					obj.setAttribute('id', product_id+"-quantity");
					obj.textContent = "In Cart:"+quantity;
					productParent.appendChild(obj);
				}
				// cart page ajax for add 
				if(productTotalCount != null) {
					productTotalCount.textContent = quantity;
					var itotal = document.getElementById(product_id+"-cart-total");
					itotal.textContent = "$"+itemTotal;
					var ototal = document.getElementById('order-total');
					ototal.textContent = "$"+orderTotal;
					var ocount = document.getElementById('order-count');
					ocount.textContent = orderCount;
				}
			}
			// remove operation
			else if(action == "remove") {
				var productTotalCount = document.getElementById(product_id+"-cart-count");
				// cart page ajax remove
				if(productTotalCount != null) {
					productTotalCount.textContent = quantity;
					var itotal = document.getElementById(product_id+"-cart-total");
					itotal.textContent = "$"+itemTotal;
					if(quantity == 0) {
						var itemRow = document.getElementById(product_id+"-row");
						itemRow.remove();
					}
					var ototal = document.getElementById('order-total');
					ototal.textContent = "$"+orderTotal;
					var ocount = document.getElementById('order-count');
					ocount.textContent = orderCount;
				}
			}
			// delete operation
			else if(action == 'delete') {
				var itemRow = document.getElementById(product_id+"-row");
				itemRow.remove();
				var ototal = document.getElementById('order-total');
				ototal.textContent = "$"+orderTotal;
				var ocount = document.getElementById('order-count');
				ocount.textContent = orderCount;
			}
		},
		error: function(error){
			alert(error);
		},
	})
}

if (secretForm != null) {
	secretForm.addEventListener('submit', e=>{
		e.preventDefault()
		$.ajax({
			type:'POST',
			url:'/update/',
			headers:{
				'X-CSRFToken':csrftoken,
			},
			data:{
			},
			success: function(response){
				var secretText = document.getElementById('secret-text')
				secretText.remove();
				const obj = document.createElement('div')
				obj.setAttribute('id', 'secret-text')
				obj.textContent = response['secret_key']
				secretBox.appendChild(obj)
			},
			error: function(error){
				alert(error);
			},
		})
	})
}