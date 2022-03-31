$('.contact-form').on('submit', function (event) {

    event.stopPropagation();
    event.preventDefault();

    let form = this,

        data = new FormData()



    $('.submit', form).val('Отправка...');
    $('#loading').addClass("d-block");
    $('input, textarea', form).attr('disabled','');

    data.append( 'Имя', 		$('[name="name"]', form).val() );
    data.append( 'Телефон', 		$('[name="phone"]', form).val() );
    data.append( 'email', 		$('[name="email"]', form).val() );
    data.append( 'Город', 		$('[name="city"]', form).val() );
    data.append( 'Сообщение', 		$('[name="text"]', form).val() );





    $.ajax({
        url: 'ajax.php',
        type: 'POST',
        data: data,
        cache: false,
        dataType: 'json',
        processData: false,
        contentType: false,

        error: function( jqXHR, textStatus ) {
              // $('#error-message').addClass("d-block");
              // $('#error-message').text(textStatus);
        },
        complete: function() {
          $('#loading').removeClass("d-block");
            $('#sent-message').addClass("d-block");
            console.log('Complete')
            form.reset()
        }
    });

    return false;
});
