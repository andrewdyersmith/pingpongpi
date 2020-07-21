$(function() {
    $('#mode-rainbow').on('click', function (e) {
	$.post("/mode/rainbow");
    });
    $('#mode-gif').on('click', function (e) {
	$.post("/mode/gif");
    });
});
