var things = ["lowering the voting age", "improving political literacy", "reducing voter discrimination", "increasing transparency", "eliminating gerrymandering", "simplifying voting", "Teens for Teens"];
var index = -1;
$(function() {
    setInterval(function() {
        index += 1;
        var el = $("#what-we-are");
        if(index < things.length) {
            el.fadeOut(500, function() {
                el.html(things[index] + ".");
                el.fadeIn(500);
            });
        }
        else {
            el.html("Teens for Teens.");
            el.show();
        }
    }, 4000);
});
