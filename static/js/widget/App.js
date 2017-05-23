define([
	"dojo/request/xhr",
	"dojo/_base/array",
	"dojo/dom",
	"widgets/GreetingWidget"
	], function(xhr, arrayUtil, dom, GreetingWidget){
		return function () {
				xhr.get("api/v1/default_guestbook/greetings/", {
					handleAs: "json",
					query: {limit: 5}
				}).then(function (data) {
					var greetingContainer = dom.byId("greetingContainer");
					arrayUtil.forEach(data.greetings, function (greeting) {
						var widget = new GreetingWidget(greeting).placeAt(greetingContainer);
					});
				});
			}
});
