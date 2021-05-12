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
const csrftoken = getCookie('csrftoken');

const updatebtn = document.getElementsByClassName('update-cart')

for(var i=0; i<updatebtn.length; i++) {
	updatebtn[i].addEventListener('click', function() {
		var product_id = this.dataset.product;
		var action = this.dataset.action;
		updateCart(product_id, action)
	})
}

function updateCart(productID, action) {
	var url = '/updateCart/'

	fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			},
			body: JSON.stringify({'product_id':productID, 'action':action}),
		})
	.then((response)=>
		{
			return response.json();
		}		
	)
	.then((data) => {
		console.log(data)
	})
}

