$(function () {
  "use strict";
  /*Activate default tab contents*/
  var leftPos, newWidth, $magicLine, defaultActive;

  defaultActive = $(".tabs li.active a").attr("href");
  $(defaultActive).show();

  $(".tabs").append("<li id='magic-line'></li>");
  $magicLine = $("#magic-line");
  $magicLine
    .width($(".active").width())
    .css("left", $(".active a").position().left)
    .data("origLeft", $magicLine.position().left)
    .data("origWidth", $magicLine.width());

  $(".tabs li a").click(function () {
    var $this, tabId, leftVal, $tabContent;
    $this = $(this);
    $tabContent = $(".tabContent");
    $this.parent().addClass("active").siblings().removeClass("active");
    tabId = $this.attr("href");

    leftVal = $($tabContent).index($(tabId)) * $tabContent.width() * -1;
    $(".tabWrapper").stop().animate({ left: leftVal });

    $magicLine
      .data("origLeft", $this.position().left)
      .data("origWidth", $this.parent() + 40);
    return false;
  });

  /*Magicline hover animation*/
  $(".tabs li")
    .find("a")
    .hover(
      function () {
        var $thisBar = $(this);
        leftPos = $thisBar.position().left;
        newWidth = $thisBar.width().width();
        $magicLine.stop().animate({ left: leftPos, width: newWidth });
      },
      function () {
        $magicLine.stop().animate({
          left: $magicLine.data("origLeft"),
          width: $magicLine.data("origWidth"),
        });
      }
    );
});
