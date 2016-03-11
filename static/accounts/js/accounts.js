$(function() {
	// Updater
	function update_bucket(widget, count) {
		console.log(widget);
		start_time = new Date();

		$('.b-loader').show();

		var url = '/bucket/update/';

		var data = {
			'csrfmiddlewaretoken': widget.data('csrf'),
			'content_type': widget.data('content_type'),
			'object_id': widget.data('object_id'),
			'count': count
		};

		console.log(data);

		$.post(url, data).done(function(response) {
			console.log(response);
			if (response.status == 'ok') {
				widget.data('count', response.item_count);
				widget.find('.b-bucket-widget__count').text(response.item_count);
				widget.find('.b-bucket-widget__total_price').text(response.item_total_price);

				$('.b-bucket_total_count').text(response.bucket_total_count);
				$('.b-bucket_item_count').text(response.bucket_item_count);
				$('.b-bucket_total_retail_price').text(response.bucket_total_retail_price);
				$('.b-promo_discount').text(response.promo_discount);

				$('.b-order_price').text(response.order_price);

				if (response.item_count) {
					widget.addClass('m-in-bucket_True');
					if (typeof(add_to_bucket) == 'function') {
						create = true;
						$('.b-bucket tbody .b-bucket-item').each(function( index, element ) {
							if (widget.data('object_id') == $(element).data('object_id')) {
								create = false;
							}
						});
						add_to_bucket(widget, create);
					}
				} else {
					widget.removeClass('m-in-bucket_True');
					if (typeof(restore_on_relative) == 'function') {
						restore_on_relative(widget);
					}
				}

				if (response.bucket_total_count == '0') {
					$('.m-template_bucket').addClass('m-bucket_empty');
				} else {
					$('.m-template_bucket').removeClass('m-bucket_empty');
				}
			} else {
				alert('Ajax error!');
			}

			$('.b-loader').hide();
			stop_time = new Date();
			console.log(stop_time.getTime() - start_time.getTime());

		}); // end ajax

	}


	// Add, Up
	$(document).on('click', '.b-bucket-widget__add, .b-bucket-widget__up', function(e) {
		$this = $(this);
		var widget = $('.m-widget-' + $this.data('widget'));
		console.log(widget);
		var count = parseInt(widget.data('count'), 10) + 1;
		update_bucket(widget, count);

		e.preventDefault();
	}); // end on click

	// Down
	$(document).on('click', '.b-bucket-widget__down', function(e) {
		$this = $(this);
		var widget = $('.m-widget-' + $this.data('widget'));
		var count = widget.data('count') - 1;
		update_bucket(widget, count);

		e.preventDefault();
	}); // end on click

	$(document).on('click', '.b-bucket-widget__delete', function(e) {
		$this = $(this);
		var widget = $('.m-widget-' + $this.data('widget'));
		update_bucket(widget, 0);

		e.preventDefault();
	}); // end on click


	$('.b-bucket-widget__count').on('keypress', function(e) {
		$this = $(this);

		if ([48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 13, 37, 39].indexOf(e.keyCode) == -1) {
			return false;
		}

		if (e.which != 8 && $this.text().length >= 2) {
			e.preventDefault();
		}

		if (e.keyCode == 13) {
			$this.blur();
			var widget = $('.m-widget-' + $this.data('widget'));
			update_bucket(widget, $this.text());
		}
	});

});