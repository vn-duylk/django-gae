define([
	"dojo/_base/declare",
	"dijit/_TemplatedMixin",
	"dijit/_WidgetBase",
	"widgets/GreetingContainer",
	"dojo/text!./App.html"
], function (declare, _TemplatedMixin, _WidgetBase, GreetingContainer, template) {
	return declare("App", [_WidgetBase, _TemplatedMixin], {
		templateString: template
	});
});
