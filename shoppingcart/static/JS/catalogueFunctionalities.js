document.addEventListener('DOMContentLoaded', function () {
    const urlParams = new URLSearchParams(window.location.search);
    
    if (urlParams.has('added_to_cart')) {
        const cartModal = new bootstrap.Modal(document.getElementById('cartModal'));
        cartModal.show();
    }

    document.querySelectorAll('.add-to-cart-form').forEach(form => {
        form.addEventListener('submit', function () {
            setTimeout(() => {
                window.location.href = window.location.pathname + '?added_to_cart=true';
            }, 500);
        });
    });
});