class ScrollBlock {
    constructor(startH, fadingH, endH, appearAnim, disappearAnim, moveLen=1) {
        this.startH = startH;
        this.fadingH = fadingH;
        this.endH = endH;
        this.animation = function (height, target) {
            let ret;
            if (height <= fadingH) {
                ret = appearAnim(height, target);
            } else {
                ret = disappearAnim(height, target);
            }

            function defaultMove(height) {
                // return (height-startH)/200;
                return easeInOut(startH, endH, height, 0, moveLen);
            }
            if (ret.hasOwnProperty("padding-bottom")) {
                ret["padding-bottom"] = ret["padding-bottom"] + defaultMove(height)
            } else {
                ret["padding-bottom"] = defaultMove(height)
            }
            for (let key in ret) {
                if (key == "padding-bottom" || key == "padding-top") {
                    ret[key] += "rem";
                }
            }
            target.css(ret)
        }
    }
}

function easeInOut(startH, endH, curH, startVal, endVal) {
    if (curH < startH) { return startVal }
    else if (endH < curH) { return endVal }
    const p = Math.min(1, (curH - startH) / (endH - startH))

    function easeInOutQuart(x) {
        return x < 0.5 ? 8 * x * x * x * x : 1 - Math.pow(-2 * x + 2, 4) / 2;
    }
    return startVal + (endVal - startVal) * easeInOutQuart(p)
}


function frontPageTitleObject(startH, endH, bottomPadding=0) {
    return new ScrollBlock(startH, endH - 400, endH,
        function (height) {
            popPadding = easeInOut(startH, startH + 300, height, 0, 2.5)
            newOpacity = easeInOut(startH, startH + 300, height, 0, 1)
            return {
                "padding-bottom": (popPadding + bottomPadding),
                "opacity": newOpacity
            }
        },
        function (height) {
            newOpacity = easeInOut(endH - 400, endH, height, 1, 0)
            return {
                "padding-bottom": (2.5 + bottomPadding),
                "opacity": newOpacity
            }
        },
        false
    )
}

/* 앱 */

function frontPageNoPopup(startH, topPadding=0, bottomPadding=0, move=true) {
    return new ScrollBlock(startH, startH + 300, startH + 600,
        function (height) {
            newOpacity = easeInOut(startH, startH + 300, height, 0, 1)
            return {
                "padding-top": topPadding,
                "padding-bottom": bottomPadding,
                "opacity": newOpacity
            }
        },
        function (height) {
            newOpacity = easeInOut(startH + 300, startH + 600, height, 1, 0)
            return {
                "padding-top": topPadding,
                "padding-bottom": bottomPadding,
                "opacity": newOpacity
            }
        },
        move
    )
}

const hello = new ScrollBlock(100, 2900, 3200,
    function (height) {
        popPadding = easeInOut(500, 800, height, 0, 5)
        newOpacity = easeInOut(100, 400, height, 0, 1)
        return {
            "padding-bottom": popPadding,
            "opacity": newOpacity
        }
    },
    function (height) {
        newOpacity = easeInOut(2900, 3200, height, 1, 0)
        return {
            "padding-bottom": 5,
            "opacity": newOpacity
        }
    },
    false
)
const iamSY = new ScrollBlock(500, 2900, 3200,
    function (height) {
        newOpacity = easeInOut(500, 800, height, 0, 1)
        if (height < 800) {
            return {
                "opacity": newOpacity
            }
        } else if (height < 2600) {
            return {
                "opacity": 100,
                "padding-top": easeInOut(800, 1100, height, 0, 5)
            }
        } else {
            return {
                "opacity": 100,
                "padding-top": 5 - easeInOut(2600, 2900, height, 0, 5)
            }
        }
    },
    function (height) {
        newOpacity = easeInOut(2900, 3200, height, 1, 0)
        return {
            "opacity": newOpacity
        }
    },
    false
)

const firstIntro = frontPageNoPopup(1000, 0.15, undefined, 0.3);
const secondIntro = frontPageNoPopup(1600, 0.15, undefined, 0.3);
const thirdIntro = frontPageNoPopup(2100, 0.15, undefined, 0.3);

/* 앱 소개 */
const iOSStudying = frontPageTitleObject(3000, 4600, 5)
const snuyum = frontPageNoPopup(3200, 0, 2)
const scrollBlockFive = frontPageNoPopup(3200, 5, 0)
const scrollBlock6 = frontPageNoPopup(3800, 0, 2)
const scrollBlock7 = frontPageNoPopup(3800, 5, 0)
/* 프론트엔드 */
const scrollBlock8 = frontPageTitleObject(4400, 5200, 4)
const scrollBlock9 = frontPageNoPopup(4400, 2 , 0)
/* 마무리 */
const scrollBlock10 = new ScrollBlock(5200, 100000, 100000,
    function (height) {
        newOpacity = easeInOut(5200, 5500, height, 0.3, 1)
        return {
            "opacity": newOpacity
        }
    },
    function (height) { },
    false
)

const scrollBlocks = [hello, iamSY, firstIntro, secondIntro, thirdIntro, iOSStudying, snuyum, scrollBlockFive, scrollBlock6, scrollBlock7, scrollBlock8, scrollBlock9, scrollBlock10]

function update() {
    let height = Math.max(0, document.documentElement.scrollTop);
    for (let i = 0; i < scrollBlocks.length; i++) {
        const element = scrollBlocks[i];
        if (element.startH <= height && height <= element.endH) {
            target = $(".front-page__object:nth-child(" + (i + 1) + ")")
            target.css({
                "display": "inline-block"
            })
            element.animation(height, $(".front-page__object:nth-child(" + (i + 1) + ")"))
        } else {
            $(".front-page__object:nth-child(" + (i + 1) + ")").css({
                "display": "none"
            })
        }
    }
}

$(update)
document.addEventListener('scroll', function () {
    update()
});