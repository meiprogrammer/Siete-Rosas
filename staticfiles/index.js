document.addEventListener('DOMContentLoaded', () => {

    function getImages() {
        let getI = parseInt(localStorage.getItem('i')) || 1;
        let newI = getI + 1;

        if (getI >= 9) {
            localStorage.setItem('i', 1);
            newI = localStorage.getItem('i');
        }
        
        document.querySelector('body').style.backgroundImage = `url('/static/images/Background/image${newI}.png')`;
        localStorage.setItem('i', newI)
    }

    getImages()
    setInterval(getImages, 5000);
})