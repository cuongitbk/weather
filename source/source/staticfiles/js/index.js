$(document).ready(function () {
    $('.select_location').on('change', function () {
        window.location = '?id=' + $(this).val();
    });
});