function build_filter(genome) {
    var selectObj = $('<select>', {
        class: 'form-control',
        name: 'filter_select',
        id: 'genome_select'
    }).append($('<option/>', {
        key: '',
        value: '-- select filter --',
    }).text('-- select filter --'));
    var optionString = '';
    $.get('/get_filter_options', {
        genome: genome,
        type: 'GET',
    },
    function(data, status){
        console.log("Data: " + data.filters + "\nStatus: " + status);
        options = data.filters;
        $.each(options, function(key, value) {
            console.log('each - key: ' + key + ' value: ' + value);
            selectObj.append($('<option/>', {
                value: value,
                text: value,
            }));
        });
        $('#filter_select_container').html(selectObj);
    });
};

$(document).ready(function() {
    $('select[name=genome_select]').change(function() {
        var cboxes = $('#bw_checkboxes');
        var genome = $(this).val();
        console.log('Selected genome: ' + genome);
    });

    if ($('select[name=genome_select]')) {
        build_filter($('select[name=genome_select]').val());
        $('')
    };

    $('#checkAll').click(function() {
        $(".check").prop('checked', $(this).prop('checked'));
    });

    $('#genLinkOut').click(function() {
        console.log("Clicked the linkOut button");
        var selected = [];
        $('#bigwigs input:checked').each(function (){
            selected.push($(this).attr('value'));
        });
        trackString = selected.join();
        console.log(trackString);

        // new link-out button to appear on click
        selected_genome = $('#genome_select option:selected').text();
        var linkButton = $('<button/>', {
            class: 'btn btn-success',
            text: 'I want to go to there ',
            click: function () {
                $.get('/update_trackDB', {
                    selected_genome: selected_genome,
                    tracks: trackString
                }).done(function () {
                    console.log("Success!");
                });
            },
        }).append($('<span></span>').addClass('fa').addClass('fa-external-link-square'));
        $('#linkOutDiv').html(linkButton);


        <!--var newButt = $('<button class="btn btn-success" type="submit" id="goToLink">'+-->
                         <!--'<span class="fa fa-external-link-square">&nbspI want to go to there</span>');-->
        <!--$('#linkOutDiv').html(newButt);-->
    });


});