(function() {

  var dateListRequest = {
    requestList: function(url) {
      $.ajax({
        "type": "GET",
        "dataType": "json",
        "url": url,
        context: this,
        success: $.proxy(this.onRequestSuccess, this),
        error: $.proxy(this.onRequestFailed, this),
      });
    },
    onRequestSuccess: function(data, textStatus, jqXHR) {
      DatesListController.renderList(data);
    },
    onRequestFailed: function(id, xhr, textStatus, error) {
      if (xhr.status == 400) {} else if (xhr.status == 500) {}
      console.log(error);
    },
  }

  var dateListUtils = (function() {

    function renderListItem (dateItem) {
      var dateItemUrl = DatesListController.dateListFilteringUrl + dateItem['published_parsed_date']
      var dateItemListContent = dateItem['published_parsed_date'] + "<span class=\"badge\">" + dateItem['dates_count'] + "</span>"

      var itemHtml = ['<a class=\"', "list-group-item", "\" href=\"", dateItemUrl, "\">", dateItemListContent, "</a>"];
      if (DatesListController.dateFilteredBy.length !== 0 &&
        DatesListController.dateFilteredBy === dateItem['published_parsed_date']
      ) {
        itemHtml[1] += " active"; // highlight the filtered by date
      }

      return itemHtml.join('')
    }

    function renderListGroup (dateList) {
      // Having the array of objects, render it into the list-group
      var items = [];

      var firstItemHtml = ['<a class=\"', "list-group-item", "\" href=\"", DatesListController.dateListNoFilteringUrl, "\"> Show All Dates </a>"];
      if (DatesListController.dateFilteredBy.length === 0)
        firstItemHtml[1] += " active"; // highlight the 'Show All Dates'
      items.push(firstItemHtml.join(''));

      $.each(dateList, function(index, dateItem) {
        var itemHtml = renderListItem(dateItem);
        items.push(itemHtml);
      });
      var html = items.join('');
      return html;
    }

    return {
      renderListGroup: renderListGroup,
    }
  })();

  var DatesListController = {
    datesListUrl: $('#date-list-url').data('url'),
    datesListPlaceholderSelector: '#date-list',
    dateListNoFilteringUrl: $('#date-list-filtering-url').data('url'),
    dateListFilteringUrl: null,
    dateFilteredBy: $('#filter_date_used').data('date'),

    init: function() {
      this.dateListFilteringUrl = this.dateListNoFilteringUrl + $('#date-list-filtering-url').data('filter-param')
      dateListRequest.requestList(this.datesListUrl);
    },
    renderList: function(dateList, error) {
      if (error !== undefined) {
        $(this.datesListPlaceholderSelector).text("Error during loading of dates list.");
        return;
      }
      var html = dateListUtils.renderListGroup(dateList);
      $(this.datesListPlaceholderSelector).html(html);
    },
  }

  DatesListController.init();
})();
