$(function() {
    $('#mode-rainbow').on('click', function (e) {
	$.post("/mode/rainbow");
    });
    $('#mode-gif').on('click', function (e) {
	$.post("/mode/gif");
    });
    $('#mode-text').on('click', function (e) {
	$.post("/mode/text");
    });
    $('#mode-off').on('click', function (e) {
	$.post("/mode/off");
    });
});
