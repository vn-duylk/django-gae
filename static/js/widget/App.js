define([
	"dojo/_base/declare",
	"dojo/request",
	"dojo/_base/array",
	"dojo/dom",
	"widgets/GreetingWidget"
	], function(declare, request, arrayUtil, dom, GreetingWidget){
		return function () {
				request("api/v1/default_guestbook/greetings/", {
					handleAs: "json"
				}).then(function (data) {
					var greetingContainer = dom.byId("greetingContainer");
					arrayUtil.forEach(data.greetings, function (greeting) {
						var widget = new GreetingWidget(greeting).placeAt(greetingContainer);
					});
				});
			}
});
