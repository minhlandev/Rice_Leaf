document.getElementById('imageInput').addEventListener('change', function (event) {
    var input = event.target;
    var reader = new FileReader();

    reader.onload = function () {
        var dataURL = reader.result;
        var imagePreview = document.getElementById('imagePreview');
        imagePreview.src = dataURL;
        imagePreview.style.display = 'block';
        imagePreview.width = 224;
        imagePreview.height = 224;
    };
    reader.readAsDataURL(input.files[0]);
});

window.addEventListener('load', function () {
    const heading = document.getElementById('heading');
    heading.classList.add('loaded');
});


function resetButton(){
    console.log("Clicked");
    window.location.href='/';
}
