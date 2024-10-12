$(document).ready(function() {
    // Funkce pro AJAX načítání stránek
    function loadAuctions(section, page) {
        $.ajax({
            url: window.location.pathname,  // URL bez parametrů
            data: {
                page: page,  // Číslo stránky
                section: section  // Sekce aukcí
            },
            success: function(data) {
                // Dynamicky nahradí obsah podle sekce
                if (section === 'buy-now') {
                    $('#buy-now-auctions').html($(data).find('#buy-now-auctions').html());
                    $('#buy-now-pagination').html($(data).find('#buy-now-pagination').html());
                } else if (section === 'promotion') {
                    $('#promotion-auctions').html($(data).find('#promotion-auctions').html());
                    $('#promotion-pagination').html($(data).find('#promotion-pagination').html());
                } else if (section === 'no-promotion') {
                    $('#no-promotion-auctions').html($(data).find('#no-promotion-auctions').html());
                    $('#no-promotion-pagination').html($(data).find('#no-promotion-pagination').html());
                }
            }
        });
    }

    // Kliknutí na stránkovací odkazy - Buy Now
    $(document).on('click', '.pagination-link-buy-now', function(e) {
        e.preventDefault();
        var page = $(this).data('page');  // Získání čísla stránky
        loadAuctions('buy-now', page);  // Načtení nové stránky pro 'Buy Now'
    });

    // Kliknutí na stránkovací odkazy - Promotion
    $(document).on('click', '.pagination-link-promotion', function(e) {
        e.preventDefault();
        var page = $(this).data('page');
        loadAuctions('promotion', page);
    });

    // Kliknutí na stránkovací odkazy - No Promotion
    $(document).on('click', '.pagination-link-no-promotion', function(e) {
        e.preventDefault();
        var page = $(this).data('page');
        loadAuctions('no-promotion', page);
    });
});
