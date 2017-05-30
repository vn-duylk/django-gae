define([
	"dojo/_base/declare",
	"dojo/_base/array",
	"dojo/dom",
	"dojo/dom-construct",
	'dojo/request/xhr',
	"dijit/_TemplatedMixin",
	"dijit/_WidgetBase",
	"widgets/GreetingWidget",
], function (declare, arrayUtil, dom, domConstruct, xhr, _TemplatedMixin, _WidgetBase, GreetingWidget) {
	return declare("GreetingContainer", [_TemplatedMixin, _WidgetBase], {

		postCreate: function () {
			this.inherited(arguments);
			this.loadGreeting();
		},

		loadGreeting: function () {
			xhr.get("api/v1/default_guestbook/greetings/", {
				handleAs: "json",
				query: {limit: 5}
			}).then(function (data) {
				var greetingContainer = dom.byId("greetingContainer");
				arrayUtil.forEach(data.greetings, function (greeting) {
					var widget = new GreetingWidget(greeting).placeAt(greetingContainer);
					widget.startup();
				});
			});
		},
	});
});
