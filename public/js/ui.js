const PostNum = 2;
const PageSize = 10;

$(function () {
  let startIdx = 1;
  $("#post-nav-next").click(function () {
    if (startIdx + PageSize > PostNum) { return }
    startIdx += PageSize;
    console.log($(".post-row"));
    $(".post-row").css({
      "display": "none"
    })
    $(".post-row:nth-child(-n+" + Math.min(PostNum, startIdx + PageSize - 1) + ")").css({
      "display": "block"
    })
    /* 괄호 쳐야되네???!?? */
    $(".post-row:nth-child(-n+" + (startIdx - 1) + ")").css({
      "display": "none"
    })
  })
  $("#post-nav-prev").click(function () {
    if (startIdx - PageSize < 1) { return }
    startIdx -= PageSize;
    $(".post-row").css({
      "display": "none"
    })
    $(".post-row:nth-child(-n+" + Math.max(0, startIdx + PageSize - 1) + ")").css({
      "display": "block"
    })
    /* 괄호 쳐야되네???!?? */

    $(".post-row:nth-child(-n+" + Math.max(0, startIdx - 1) + ")").css({
      "display": "none"
    })
  })
})
