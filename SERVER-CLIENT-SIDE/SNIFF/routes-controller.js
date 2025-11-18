var controller = "";
var method = "";
var update = false;

$("img").mousedown(function() {
    return false;
});




$(document).ready(function() {
    $(".active-navbar").removeClass("bg-danger");
    $(".navbar-" + controller.toLowerCase()).addClass("bg-danger");
})


$(".select-class").change(function() {
    // alert($(this).val());
    var methods = $(this).val();
    methods = methods.toLowerCase(); //.toLowerCase()

    if (methods == "all") {
        window.location.href = window.location.origin + "/ranking/";
    } else {
        window.location.href = window.location.origin + "/ranking/" + methods;
    }

});

function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}


$(document).ready(function() {


    controller = controller.toLowerCase();
    currentMethod = method;

    if (controller == "ranking") {
        if (currentMethod == "index") {
            $("rank-tabs").removeClass("active");
            $(".rank-tabs-overall").addClass("active");
            return;
        }

        if (currentMethod == "human") {
            $("rank-tabs").removeClass("active");
            $(".rank-tabs-human").addClass("active");
            return;
        }
        if (currentMethod == "akkan") {
            $("rank-tabs").removeClass("active");
            $(".rank-tabs-akkan").addClass("active");
        } else {
            if (method == "runeofc") {
                $("#class-rank").val("RuneOfc");
                return
            }

            if (method == "lifeofc") {
                $("#class-rank").val("LifeOfc");
                return
            }

            if (method == "shadowofc") {
                $("#class-rank").val("ShadowOfc");
                return
            }
            //alert(capitalizeFirstLetter(currentMethod));
            $("#class-rank").val(capitalizeFirstLetter(currentMethod));
        }
    }
})

$(document).ready(function() {
    $(".profile-tooltip").hover(function() {
        $(this).tooltip("show");
    })

});

$(document).ready(function() {
    $(".item-tooltip").hover(function() {
        $(this).tooltip("show");
    })

});


function NoUpdateFound() {
    $(".progress-bar1").animate({
        width: "100%",
    }, 500);

    $(".progress-bar2").animate({
        width: "100%",
    }, 500);
}



function NoUpdate() {
    $(document).ready(function() {
        if (update == false) {
            $(".progress-bar1").animate({
                width: "100%",
            }, 500);

            $(".progress-bar2").animate({
                width: "100%",
            }, 500);
        }
        $("#launch-btn").removeAttr('disabled');
        $(".download-dlg").hide();
    })
}

function UpdateFalse() {
    update = false;
}

function UpdateTrue() {
    $(".my-nav-item").addClass("nav-disable")
    update = true;
}

function formatBytes(bytes, decimals = 2) {
    if (!+bytes) return '0 Bytes'

    const k = 1024
    const dm = decimals < 0 ? 0 : decimals
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']

    const i = Math.floor(Math.log(bytes) / Math.log(k))

    return `${parseFloat((bytes / Math.pow(k, i)).toFixed(dm))} ${sizes[i]}`
}

function ByteRecevied(byte) {
    //alert(byte);
    if ($("#downloaded")[0]) {
        $("#downloaded").text(formatBytes(byte));
    }

}

function ByteToRecevied(byte) {
    //alert(byte);
    if ($("#download-size")[0]) {
        $("#download-size").text(formatBytes(byte));
    }
}

function ProgressBar1(percent) {
    if ($(".progress-bar1")[0]) {
        $(".progress-bar1").css("width", "" + percent + "%");
    }
}

function ProgressBar2(percent) {
    if ($(".progress-bar2")[0]) {
        $(".progress-bar2").css("width", "" + percent + "%");
    }
}

function DownloadNum(currentdownload, available) {
    $("#downloaded-patch").text(currentdownload);
    $("#available-patch").text(available);
}

$(document).ready(function() {
    $(".my-nav-item").click(function(event) {
        if (update == true) {
            event.preventDefault();
        }
    });


});

function UpdateComplete() {
    update = false;
    $("#launch-btn").removeAttr('disabled');
    $(".download-dlg").hide();
    $(".my-nav-item").removeClass("nav-disable")
}

function ExtractFile(filename) {
    $(document).ready(function() {
        $(".download-dlg").text("extracting " + filename);
    });
}

function fireEvent(name, data) {
    var event = new MessageEvent(name, { 'view': window, 'bubbles': false, 'cancelable': true, 'data': data });
    document.dispatchEvent(event);
}

function PlayBtn() {
    fireEvent("EventCmd", "1");
}

function logOut() {
    fireEvent("EventCmd", "4");
}


$(".soc-btn").click(function(event) {
    event.preventDefault();
})

$(document).ready(function() {
    if (controller == "user") {

        if (method == "index") {
            $(".side-bar-home").addClass("sidebar-active");
        }
        if (method == "purchase") {
            $(".side-bar-purchase").addClass("sidebar-active");
        }
        if (method == "topup") {
            $(".side-bar-topup").addClass("sidebar-active");
        }
        if (method == "voucher") {
            $(".side-bar-voucher").addClass("sidebar-active");
        }
        if (method == "history") {
            $(".side-bar-history").addClass("sidebar-active");
        }
        if (method == "inventory") {
            $(".side-bar-inventory").addClass("sidebar-active");
        }
    }
});


$('#is-limited').change(function() {
    if ($(this).prop('checked')) {
        $("#stock").show();
    } else {
        $("#stock").hide();
    }
})

$('#is-bundle').change(function() {
    if ($(this).prop('checked')) {
        $(".not-bundle").hide();
    } else {
        $(".not-bundle").show();
    }
})


function UploadMainImage() {
    $('#product-image').trigger('click');
}

function UploadImageList() {
    $('#product-image-list').trigger('click');
}

$("#product-image").change(function() {
    $("#main-image").hide();
    $("#cancelUpload1").show();
    $(".select-image1").hide();
    $(".upload-detail").show();

    $("#filename").text(this.files[0].name)
    $("#filesize").text(formatBytes(this.files[0].size));

});

$("#product-image-list").change(function() {
    $(".main-image-list").hide();
    $("#cancelUpload2").show();
    $(".choose-file-2").hide();
    $(".upload-detail-2").show();

    $("#filename").text(this.files[0].name)
    $("#filesize").text(formatBytes(this.files[0].size));

});

$("#bundle-upload").change(function() {
    $("#bundle-image-name").text(this.files[0].name);
});

function CancelUpload1() {
    $("#main-image").show();
    $("#cancelUpload1").hide();
    $(".select-image1").show();
    $(".upload-detail").hide();
}

function CancelUpload2() {
    $(".main-image-list").show();
    $("#cancelUpload2").hide();
    $(".choose-file-2").show();
    $(".upload-detail-2").hide();
}

function formatBytes(bytes, decimals = 2) {
    if (!+bytes) return '0 Bytes'

    const k = 1024
    const dm = decimals < 0 ? 0 : decimals
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']

    const i = Math.floor(Math.log(bytes) / Math.log(k))

    return `${parseFloat((bytes / Math.pow(k, i)).toFixed(dm))} ${sizes[i]}`
}

$(document).ready(function() {
    if (controller = "panel") {

        if (method == "index") {
            $(".nav-link").removeClass("active")
            $(".p-serverinfo").addClass("active");
        }

        if (method == "product") {
            $(".nav-link").removeClass("active")
            $(".p-productlist").addClass("active");
        }

        if (method == "addproduct") {
            $(".nav-link").removeClass("active")
            $(".p-addproduct").addClass("active");
        }
    }

});


$(".product-image-select").click(function() {
    $(".product-image-select").removeClass("active");
    $(this).addClass("active");
    var images = $(this).attr('src');
    $("#product-image-main").attr("src", images);
})


function process_payment() {
    setTimeout(function() {
        $(".submit-payment").attr('disabled', 'disabled');
    }, 100);

}

function gameLogin() {


    $("#launch-btn").attr('disabled', 'disabled');

    setTimeout(function() {
        $("#launch-btn").removeAttr('disabled');
    }, 5000);

    $.post(
        "/login/game_login", {},
        function(data, status) {
            //alert();
            fireEvent("gamelogin", data);
        });

}


$(".btn1").click(function() {
    $(".btn1").removeClass("tpp-active");
    $(this).addClass("tpp-active");

    $("input[type='radio']").click(function() {
        var radioValue = $("input[name='radio']:checked").val();
        $("#topup-amount").val(radioValue);
    });
})

$("#topup-amount").change(function() {
    $(".btn1").removeClass("tpp-active");

    var value = $(this).val();

    if (value < 10 && value != "") {
        $(this).addClass("is-invalid");
        $(".invalid-amount").text("Please insert minumum value with RM10")
        return;
    } else {
        $(this).removeClass("is-invalid");
    }

    if (value > 30000) {
        $(this).addClass("is-invalid");
        $(".invalid-amount").text("Only maximum RM30,000.00 per transaction allowed")
    }

});


var regexp = /^(?:\d+(?:\.\d{1,2})?|\.\d{1,2})$/


function payNow() {
    window.open('http://google.com', 'popup', 'width=600,height=600');
}


// FOR RUN BILL

function submit_payment() {
    // var newWindow = window.open();
    // newWindow.document.write("ohai");
    $.post(
        "/user/submit_topup", {},
        function(data, status) {
            var payment = window.open('http://google.com', 'popup', 'width=700,height=700');;
            payment.document.write(data);
        })

}

function submit_payment2() {

    var banks = $("#bankcode").val();
    var amounts = $("#topup-amount").val();



    // AMOUNT VALIDATION
    if (amounts < 10 || amounts == "") {
        $("#topup-amount").addClass("is-invalid");
        $(".invalid-amount").text("Please insert minumum value with RM10")
        return;
    } else {
        $("#topup-amount").removeClass("is-invalid");
    }

    if (amounts > 30000) {
        $("#topup-amount").addClass("is-invalid");
        $(".invalid-amount").text("Only maximum RM30,000.00 per transaction allowed")
        return;
    }
    // VALIDATION END


    $(".payment-spinner").show();

    if (banks == "" || banks == 0) {
        $("#bankcode").addClass("is-invalid");
        $(".process-payment").removeAttr('disabled');
        $(".payment-spinner").hide();
        return;
    }
    $("#bankcode").removeClass("is-invalid");

    //return;

    $.post(
        "/user/submit_topup", {
            bankcode: banks,
            amount: amounts
        },
        function(data, status) {;
            //alert(data);
            const response = JSON.parse(data);
            var payment = window.open(response.url, 'popup', 'width=900,height=700');;

            setTimeout(function() {
                $(".process-payment").removeAttr('disabled');
                $(".payment-spinner").hide();
            }, 10000);

        })
}


function AdminLogin() {

    $.post(
        "/login/admin_request", {},
        function(data, status) {;
            const response = JSON.parse(data);

            if (response.auth == true) {
                fireEvent("adminLogin", response.token);
            } else {
                alert('admin login failed')
            }
        })
}

function facebook() {
    fireEvent("socmed", "1");
}

function discord() {
    fireEvent("socmed", "2");
}


function clientsetup() {
    fireEvent("clientsetup", "1");
}
