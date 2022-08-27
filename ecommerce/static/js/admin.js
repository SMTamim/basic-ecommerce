page = window.location.href.split('/')
if (page[page.length - 1] === 'admin') {
    btnElm = document.getElementById('addAProduct');

    btnElm.addEventListener('click', () => {
        fromElm = document.getElementById('product-input-form');
        fromElm.classList.remove('hideForm');
        btnElm.classList.add('hideForm');
    })
}