(function() {
  var ratingListRequest = {
    sendRating: function(url, data) {
      $.ajax({
        "type": "PATCH",
        "dataType": "json",
        "url": url,
        data: data,
        context: this,
        success: $.proxy(this.onRequestSuccess, this),
        error: $.proxy(this.onRequestFailed, this),
      });
    },
    onRequestSuccess: function(data, textStatus, jqXHR) {
      console.log(data);
    },
    onRequestFailed: function(xhr, textStatus, error) {
      if (xhr.status == 400) {} else if (xhr.status == 500) {}
      console.log(error);
    },
  }

  var RatingsController = {
    ratingsUrl: $('#rating-url').data('url'),

    onAnyRatingButtonClick: function(event) {
      var $button = $(event.target);
      var notificationId = $(this).data('notification-id');
      var ratingValue = $button.data('action');
      var ratingData = {
        "id": notificationId,
        "rating": ratingValue,
      }
      ratingListRequest.sendRating(RatingsController.ratingsUrl, ratingData);
    },

    init: function() {
      $('.rating-buttons').on('click', RatingsController.onAnyRatingButtonClick);
    }
  }

  RatingsController.init();
})();
