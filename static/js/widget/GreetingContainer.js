define([
	"dojo/_base/declare",
	"dojo/_base/array",
	"dojo/_base/lang",
	'dojo/request/xhr',
	"dijit/_WidgetBase",
	"dijit/_TemplatedMixin",
	"widgets/GreetingWidget",
	"dojo/text!./templates/GreetingContainer.html"
], function (declare, arrayUtil, lang, xhr, _WidgetBase, _TemplatedMixin, GreetingWidget, template) {
	return declare("My.GreetingContainer", [_WidgetBase, _TemplatedMixin], {
		templateString: template,

		startup: function () {
			this.inherited(arguments);
			this.loadGreeting();
		},

		loadGreeting: function () {
			xhr.get("api/v1/default_guestbook/greetings/", {
				handleAs: "json",
				query: {limit: 5}
			}).then(lang.hitch(this, function (data) {
				var greetingContainer = this.containerNode;
				arrayUtil.forEach(data.greetings, function (greeting) {
					var widget = new GreetingWidget(greeting).placeAt(greetingContainer);
					widget.startup();
				});
			}));
		},
	});
});
