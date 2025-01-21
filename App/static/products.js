document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.imgClass').forEach((product) => {
        product.addEventListener('click', () => { 
            window.location.replace(`/product/${product.id}`);
        })
    })
})