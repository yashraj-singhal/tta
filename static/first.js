var resp_val = -1
var resp_val_2 = -1

$(document).ready(function() {
    $(".button").click(function() {
        $(".dropdown a").removeClass("clicked");
        $(".dropdown a").children("span").removeClass("clicked");
        $(".dropdown").toggleClass("open");
    });

    $(".dropdown a").click(function() {
        $(".dropdown a").removeClass("clicked");
        $(".dropdown a").children("span").removeClass("clicked");
        $(this).toggleClass("clicked");
        $(this).children("span").toggleClass("clicked");
    });
});

function getval(val) {
    for (let i = 0; i <= 5; i++) {
        $("#bt" + i).addClass("blurry");
    }
    for (let i = 0; i <= val; i++) {
        $("#bt" + i).removeClass("blurry");
    }
    resp_val = val;
}

function getval2(val) {
    for (let i = 0; i <= 5; i++) {
        $("#btt" + i).addClass("blurry");
    }
    for (let i = 0; i <= val; i++) {
        $("#btt" + i).removeClass("blurry");
    }
    resp_val_2 = val;
}

function apicall(myHeaders, data, url, message = "") {
    var requestOptions = {
        method: 'POST',
        headers: myHeaders,
        body: data,
        // redirect: 'follow'
    };
    fetch(url, requestOptions)
        .then(res => {
            if (res.ok) {
                // console.log(res);
                console.log(message)
                return res.json();
            } else {
                alert("Wrong Doing");
            }
        })
        .then(jRes => {
            console.log(jRes);
            return jRes;
        })
        .then(function() {
            window.location.reload();
        })
}



function submit(val, Sno) {
    console.log("recipe val was : ", val);
    console.log("1=GENERATED and 2=REAL");
    console.log("user selected button ", resp_val);

    if (resp_val == -1) {
        alert("Select a rating (0/1/2/3/4/5) from the rating scale below, before submitting.");
    } else if (resp_val_2 == -1) {
        alert("Select a rating (0/1) from the rating scale below, before submitting.");
    } else {
        var myHeaders = new Headers();
        myHeaders.append("Content-Type", "application/json");
        var raw = JSON.stringify({
            "image_val": val, //replaced recp_val -> image_val
            "button_val": resp_val,
            "button_2_val": resp_val_2
        });
        console.log(raw);
        var ret = apicall(myHeaders, raw, "/ttp/sbt", "submit clicked"); //changed from ttc -> ttp
        console.log(ret);

        // need hai?
        // window.location.reload();
    }
}

function skip(val) {
    console.log("recipe val was : ", val);
    console.log("1=GENERATED and 2=REAL");
    console.log("skip clicked");
    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    var raw = JSON.stringify({
        "image_val": val //replaced recp_val -> image_val
    });

    var ret = apicall(myHeaders, raw, "/ttp/skip", "submit clicked");
    console.log(ret);
    // window.location.reload();

}

$(document).ready(function() {
    $("#lo").on('click', function() {
        $.ajax({
            type: "POST",
            url: "logout",
            data: {},
            success: function() {
                console.log("success");
            }
        });
    });
});

window.onbeforeunload = function() {
    window.scrollTo(0, 0);
}