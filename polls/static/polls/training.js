/**
 * Created by kevin on 9/23/16.
 */


var number_id;


$(document).ready(function () {
    $('#start_btn').click(function () {
        $.ajax({
            type: "get",
            url: "startguess/",
            data: {},
            success: function(returnValue){
                values = JSON.parse(returnValue);
                $('.playing_btn_grp').show();
                $('#lol_text').hide();
                $('#lol_text').text('LOL');
                $('#number').text(values[1]);
                number_id = values[0];
            },
            error: function(jq, status, errorMessage){
                alert('error');
            }
        });
    });

    $('#number_big_btn').click(function () {
        $.ajax({
            type: "post",
            url: "guess/",
            data: {'number_id': number_id, 'response': 'big', 'last_number': $('#number').text()},
            success: function(returnValue){
                values = JSON.parse(returnValue);
                console.log(values[0]);
                if (values[0] == 'bad'){
                    $('.playing_btn_grp').hide();
                    $('#lol_text').show();
                    $('#lol_text').text('YOU CHEATER');
                    $('#number').text('');
                }
                else
                    $('#number').text(values[0]);
            },
            error: function(jq, status, errorMessage){
                alert('error');
            }
        });
    });

    $('#number_small_btn').click(function () {
        $.ajax({
            type: "post",
            url: "guess/",
            data: {'number_id': number_id, 'response': 'small', 'last_number': $('#number').text()},
            success: function(returnValue){
                values = JSON.parse(returnValue);
                console.log(values[0]);
                if (values[0] == 'bad'){
                    $('.playing_btn_grp').hide();
                    $('#lol_text').show();
                    $('#lol_text').text('YOU CHEATER');
                    $('#number').text('');
                }
                else
                    $('#number').text(values[0]);
            },
            error: function(jq, status, errorMessage){
                alert('error');
            }
        });
    });

    $('#correct_btn').click(function () {
        $('.playing_btn_grp').hide();
        $('#lol_text').show();
        $('#number').text('');
    });
});
