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
