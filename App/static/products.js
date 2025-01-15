document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.productClass').forEach((product) => {
        product.addEventListener('click', () => { 
            window.location.replace(`/product/${product.id}`);
        })
    })
})