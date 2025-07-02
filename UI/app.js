let base64Image;

Dropzone.autoDiscover = false;

$(function () {
    $("#error").hide();
    $("#divClassTable").hide();

    let prettyNameMap = {
        "akshay": "Akshay Kumar",
        "kohli": "Virat Kohli",
        "messi": "Lionel Messi",
        "nora": "Nora Fatehi",
        "urvashi": "Urvashi Rautela"
    };

    $("#dropzone").dropzone({
        maxFiles: 1,
        url: "/",
        autoProcessQueue: false,
        addRemoveLinks: true,
        init: function () {
            this.on("addedfile", function (file) {
                $("#error").hide();  // ✅ Hide error when new image is added
                let reader = new FileReader();
                reader.onload = function (e) {
                    base64Image = e.target.result;
                };
                reader.readAsDataURL(file);
            });
        }
    });

    $('#submitBtn').on('click', function () {
        if (!base64Image) {
            alert("Please upload an image first.");
            return;
        }

        $.post("http://127.0.0.1:5000/classify_image", {
            image_data: base64Image
        }, function (data, status) {
            if (!data || data.length === 0) {
                $('#error').show();
                $('#resultHolder').html('');
                $("#divClassTable").hide();
                $("#predictedCardContainer").html('');
                return;
            }

            let result = data[0];
            let predictedClass = result.class.toLowerCase();
            let displayName = prettyNameMap[predictedClass] || predictedClass;

            // ✅ Extract the HTML of the predicted card and place it
            let predictedCardHtml = $(`.card-wrapper[Celebrity='${predictedClass}']`).prop('outerHTML');
            $("#predictedCardContainer").html(predictedCardHtml);

            // ✅ Show prediction name
            $("#resultHolder").html(`<h4 class='text-success text-center mt-3'>Prediction: ${displayName}</h4>`);

            // ✅ Show score table
            $("#divClassTable").show();

            for (let class_name in result.class_dictionary) {
                let scoreId = "#score_" + class_name.toLowerCase();
                let index = result.class_dictionary[class_name];
                let prob = result.class_probability[index] || 0;
                $(scoreId).html(prob + "%");
            }
        }).fail(function () {
            $('#error').show();
            $('#resultHolder').empty();
            $("#divClassTable").hide();
            $("#predictedCardContainer").html('');
        });
    });
});
