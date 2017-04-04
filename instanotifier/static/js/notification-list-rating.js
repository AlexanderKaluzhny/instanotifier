(function() {
  var ratingListRequest = {
    sendRating: function(url, data) {
      $.ajax({
        "type": "PATCH",
        "dataType": "json",
        "url": url,
        "data": data,
        context: this,
        success: $.proxy(this.onRequestSuccess, this),
        error: $.proxy(this.onRequestFailed, this),
      });
    },
    onRequestSuccess: function(data, textStatus, jqXHR) {
      RatingsController.onNotificationRatedResponse(data);
    },
    onRequestFailed: function(xhr, textStatus, error) {
      if (xhr.status == 400) {} else if (xhr.status == 500) {}
      console.log(error);
    },
  }

  var RatingsController = {
    ratingsUrl: $('#rating-url').data('url'),
    ratingButtonsIconClasses: {
      'upvote': 'fa fa-thumbs-o-up',
      'upvoted': 'fa fa-thumbs-up',
      'downvote': 'fa fa-thumbs-o-down',
      'downvoted': 'fa fa-thumbs-down'
    },

    getNotificationById: function(id) {
      var $notification = $(".notification-list-item[data-id=\"" + id.toString() + "\"]");
      return $notification;
    },

    getRatingButtonIconHtml: function(buttonAction) {
      var ratingButtonHtmlTemplate = ['<i class="', 'fa fa-thumbs-o-up', '"aria-hidden="true"></i>'];
      ratingButtonHtmlTemplate[1] = RatingsController.ratingButtonsIconClasses[buttonAction];
      return ratingButtonHtmlTemplate.join('');
    },

    adjustRatingButtonTitles: function(id, currentRating) {
      var $notification = this.getNotificationById(id);
      var $upvoteButton = $notification.find('#upvote-button');
      var $downvoteButton = $notification.find('#downvote-button');

      if (currentRating === 0) {
        $upvoteButton.html(RatingsController.getRatingButtonIconHtml('upvote'));
        $downvoteButton.html(RatingsController.getRatingButtonIconHtml('downvote'));
      } else if (currentRating === 1) {
        $upvoteButton.html(RatingsController.getRatingButtonIconHtml('upvoted'));
        $downvoteButton.html(RatingsController.getRatingButtonIconHtml('downvote'));
      } else if (currentRating === -1) {
        $upvoteButton.html(RatingsController.getRatingButtonIconHtml('upvote'));
        $downvoteButton.html(RatingsController.getRatingButtonIconHtml('downvoted'));
      }
    },

    getNextRatingAction: function(notificationCurrentRating, ratingClicked) {
      var ratingAction = ratingClicked;
      var ratingActionInt = 0; // rating is "default"

      if (ratingAction === "upvoted") {
        ratingActionInt = 1;
      } else if (ratingAction === "downvoted") {
        ratingActionInt = -1;
      }

      // TODO: change the ratingAction to be in readable string format.
      if (notificationCurrentRating === ratingActionInt) {
        // set rating to default if user clicked the same rating button at second time;
        ratingAction = "default";
        ratingActionInt = 0;
      }
      return ratingAction;
    },

    onAnyRatingButtonClick: function(event) {
      var $button = $(event.currentTarget);
      var $currentNotificationItem = $(this).parents(".notification-list-item");
      var notificationId = $currentNotificationItem.data('id');
      var notificationCurrentRating = $currentNotificationItem.data('rating');
      var ratingAction = RatingsController.getNextRatingAction(notificationCurrentRating,
        $button.data('action'));

      var ratingData = {
        "id": notificationId,
        "rating": ratingAction,
      }
      ratingListRequest.sendRating(RatingsController.ratingsUrl, ratingData);
    },

    onNotificationRatedResponse: function(notificationData) {
      var notificationId = notificationData.id;
      var newRating = notificationData.rating;
      var $notification = this.getNotificationById(notificationId);

      $notification.data('rating', newRating);
      $notification.attr('data-rating', newRating);
      RatingsController.adjustRatingButtonTitles(notificationId, newRating);
    },

    init: function() {
      $('.rating-buttons').on('click', '.submit', RatingsController.onAnyRatingButtonClick);

      // traverse all the notifications and highlight the current rating
      $(".notification-list-item").each(function(idx, notificationElem){
        var notificationId = $(notificationElem).data('id');
        var rating = $(notificationElem).data('rating');
        RatingsController.adjustRatingButtonTitles(notificationId, rating);
      });
    }
  }

  RatingsController.init();
})();
