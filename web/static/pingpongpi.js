$(function() {
    $('#mode-rainbow').on('click', function (e) {
	$.post("/mode/rainbow");
    });
    $('#mode-gif').on('click', function (e) {
	$.post("/mode/gif");
    });
    $('#mode-text').on('click', function (e) {
	$.post("/mode/text?val=" + $("#text_value").val());
    });
    $('#mode-game-of-life').on('click', function (e) {
	$.post("/mode/game-of-life");
    });
    $('#mode-plasma').on('click', function (e) {
	$.post("/mode/plasma");
    });
    $('#mode-fire').on('click', function (e) {
	$.post("/mode/fire");
    });
    $('#mode-off').on('click', function (e) {
	$.post("/mode/off");
    });
});
